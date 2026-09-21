import pandas as pd


def _col(df, *names):
    for name in names:
        if name in df.columns:
            return name
    return None


def _mean(df, *names):
    col = _col(df, *names)
    if not col:
        return 0
    return round(pd.to_numeric(df[col], errors="coerce").mean(), 2)


def summary(df):
    if df is None or df.empty:
        return {}

    attrition = _col(df, "Attrition")
    salary = _col(df, "MonthlyIncome", "Salary")
    performance = _col(df, "PerformanceRating", "Performance")
    satisfaction = _col(df, "JobSatisfaction", "Satisfaction")
    training = _col(df, "TrainingTimesLastYear", "Training")
    tenure = _col(df, "YearsAtCompany", "Tenure")
    total_work = _col(df, "TotalWorkingYears")

    total = len(df)

    if attrition:
        attr = df[attrition].astype(str).str.lower().eq("yes").mean() * 100
    else:
        attr = 0

    return {
        "total_employees": int(total),
        "active_employees": int(total - round(total * attr / 100)),
        "attrition_rate": round(attr, 2),
        "average_salary": _mean(df, salary) if salary else 0,
        "average_performance": _mean(df, performance) if performance else 0,
        "average_job_satisfaction": _mean(df, satisfaction) if satisfaction else 0,
        "average_training": _mean(df, training) if training else 0,
        "average_tenure": _mean(df, tenure) if tenure else 0,
        "average_total_working_years": _mean(df, total_work) if total_work else 0
    }


def department_stats(df):
    col = _col(df, "Department")
    if not col:
        return []

    attr = _col(df, "Attrition")
    result = []

    for department, group in df.groupby(col, dropna=False):
        row = {
            "department": str(department),
            "employees": int(len(group))
        }

        if attr:
            row["attrition_rate"] = round(
                group[attr].astype(str).str.lower().eq("yes").mean() * 100, 2
            )

        result.append(row)

    return result


def performance_stats(df):
    col = _col(df, "PerformanceRating", "Performance")
    if not col:
        return []

    series = pd.to_numeric(df[col], errors="coerce").dropna()
    return [
        {"rating": float(value), "employees": int((series == value).sum())}
        for value in sorted(series.unique())
    ]


def salary_stats(df):
    col = _col(df, "MonthlyIncome", "Salary")
    if not col:
        return []

    series = pd.to_numeric(df[col], errors="coerce").dropna()
    if series.empty:
        return []

    return {
        "average": round(series.mean(), 2),
        "minimum": round(series.min(), 2),
        "maximum": round(series.max(), 2),
        "median": round(series.median(), 2)
    }


def attrition_stats(df):
    attr = _col(df, "Attrition")
    if not attr:
        return {}

    yes = int(df[attr].astype(str).str.lower().eq("yes").sum())
    no = int(df[attr].astype(str).str.lower().eq("no").sum())

    result = {
        "yes": yes,
        "no": no,
        "rate": round((yes / len(df)) * 100, 2) if len(df) else 0
    }

    dept = _col(df, "Department")
    role = _col(df, "JobRole")

    if dept:
        result["by_department"] = department_stats(df)

    if role:
        rows = []
        for value, group in df.groupby(role, dropna=False):
            rows.append({
                "job_role": str(value),
                "employees": int(len(group)),
                "attrition_rate": round(
                    group[attr].astype(str).str.lower().eq("yes").mean() * 100, 2
                )
            })
        result["by_job_role"] = rows

    return result


def workforce_health(df):
    # Descriptive workforce analytics only; this is not a medical diagnosis.
    if df is None or df.empty:
        return {}

    performance = _mean(df, "PerformanceRating", "Performance")
    satisfaction = _mean(df, "JobSatisfaction", "Satisfaction")
    worklife = _mean(df, "WorkLifeBalance", "Work_Life_Balance")
    attrition = summary(df).get("attrition_rate", 0)

    components = [performance, satisfaction, worklife]
    normalized = []

    for value in components:
        if value:
            normalized.append(min(value / 4, 1) * 100)

    positive = sum(normalized) / len(normalized) if normalized else 0
    score = round((positive * 0.75) + ((100 - attrition) * 0.25), 2)

    return {
        "score": score,
        "performance_component": round(performance, 2),
        "satisfaction_component": round(satisfaction, 2),
        "work_life_balance_component": round(worklife, 2),
        "attrition_rate": attrition
    }
