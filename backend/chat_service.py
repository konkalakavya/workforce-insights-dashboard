from services.analytics_service import summary, department_stats, attrition_stats


def answer(question, df):
    q = str(question).lower().strip()

    if not q:
        return {"answer": "Please enter a workforce analytics question."}

    if any(word in q for word in ["attrition", "turnover", "leave", "exit"]):
        data = attrition_stats(df)
        return {
            "answer": (
                f"The current dataset has an attrition rate of "
                f"{data.get('rate', 0)}%, with {data.get('yes', 0)} employees "
                f"marked as having left."
            ),
            "data": data
        }

    if "department" in q:
        data = department_stats(df)
        return {
            "answer": "Here is the department-level workforce summary.",
            "data": data
        }

    if any(word in q for word in ["salary", "income", "compensation"]):
        data = summary(df)
        return {
            "answer": f"The average monthly income in the dataset is {data.get('average_salary', 0)}.",
            "data": {"average_salary": data.get("average_salary", 0)}
        }

    if any(word in q for word in ["performance", "rating"]):
        data = summary(df)
        return {
            "answer": f"The average performance rating is {data.get('average_performance', 0)}.",
            "data": {"average_performance": data.get("average_performance", 0)}
        }

    if any(word in q for word in ["employee", "workforce", "overview", "total"]):
        data = summary(df)
        return {
            "answer": f"The dataset contains {data.get('total_employees', 0)} employees.",
            "data": data
        }

    return {
        "answer": (
            "I can answer questions about workforce overview, departments, "
            "salary, performance, and attrition."
        )
    }
