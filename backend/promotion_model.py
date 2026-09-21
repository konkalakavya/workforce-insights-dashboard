def _number(payload, *names, default=0):
    for name in names:
        value = payload.get(name)
        if value is not None:
            try:
                return float(value)
            except (TypeError, ValueError):
                pass
    return default


def predict_promotion(payload):
    """
    Transparent promotion-readiness heuristic.

    The standard IBM HR Attrition dataset does not contain a validated
    promotion target, so this endpoint does NOT claim to be a supervised
    promotion classifier.
    """
    performance = _number(payload, "PerformanceRating", "Performance")
    level = _number(payload, "JobLevel", "Job_Level")
    current_role_years = _number(
        payload, "YearsInCurrentRole", "Years_In_Current_Role"
    )
    since_promotion = _number(
        payload, "YearsSinceLastPromotion", "Years_Since_Last_Promotion"
    )
    total_years = _number(payload, "TotalWorkingYears", "Total_Working_Years")
    training = _number(payload, "TrainingTimesLastYear", "Training")

    score = 0

    if performance >= 4:
        score += 30
    elif performance >= 3:
        score += 20
    else:
        score += 10

    score += min(level * 8, 20)
    score += min(current_role_years * 2, 15)
    score += min(since_promotion * 3, 15)
    score += min(total_years * 0.5, 10)
    score += min(training * 2, 10)

    score = min(score, 100)

    return {
        "promotion_readiness_percentage": round(score, 2),
        "method": "transparent heuristic",
        "note": (
            "This is a readiness score, not a supervised promotion prediction, "
            "because the standard dataset does not provide a validated promotion target."
        )
    }
