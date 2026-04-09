import pickle

model = pickle.load(open('model.pkl','rb'))

def check_loan(income, credit, loan, age):

    reasons = []
    suggestions = []

    # 🔴 HARD RULES
    if age < 20:
        return {
            "status": "Rejected",
            "statement": "Rejected due to age below 20.",
            "reasons": ["Age is below minimum requirement."],
            "suggestions": ["Apply after age 20."]
        }

    if income < 30000:
        return {
            "status": "Rejected",
            "statement": "Rejected due to low income.",
            "reasons": ["Income is below ₹30,000."],
            "suggestions": ["Increase income."]
        }

    # 🤖 AI Prediction
    input_data = [[income, credit, loan, age]]
    prediction = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0][1]

    score = 0

    # CREDIT
    if credit >= 750:
        score += 2
        reasons.append("Strong credit score")
    elif credit >= 650:
        score += 1
        reasons.append("Average credit score")
    else:
        score -= 2
        reasons.append("Low credit score")
        suggestions.append("Improve credit score")

    # INCOME
    if income >= 60000:
        score += 2
        reasons.append("High income")
    elif income >= 40000:
        score += 1
        reasons.append("Stable income")
    else:
        reasons.append("Moderate income")

    # LOAN
    if loan <= income * 5:
        score += 2
        reasons.append("Loan within safe limit")
    elif loan <= income * 8:
        score += 1
        reasons.append("Loan slightly high")
    else:
        score -= 2
        reasons.append("Loan too high")
        suggestions.append("Reduce loan amount")

    # FINAL DECISION
    final = "Approved" if (score >= 2 and prediction == 1) else "Rejected"

    # FIX probability
    final_prob = prob*100 if final=="Approved" else (1-prob)*100

    # 🔥 BRIEF STATEMENT LOGIC
    if final == "Approved":
        brief = "Approved because of good income, credit score, and manageable loan amount."
    else:
        brief = "Rejected due to financial risk factors like low credit, income, or high loan."

    return {
        "status": final,
        "statement": f"{brief} (Confidence: {round(final_prob,2)}%)",
        "reasons": reasons,
        "suggestions": suggestions if suggestions else ["Maintain financial profile"]
    }