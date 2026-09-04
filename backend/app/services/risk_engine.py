# File: backend/app/services/risk_engine.py
def calculate_final_risk(email_risk: float, url_risks: list[float]) -> tuple[float, str]:
    if not url_risks:
        final_risk = email_risk
    else:
        max_url_risk = max(url_risks)
        final_risk = (email_risk * 0.5) + (max_url_risk * 0.5)

    if final_risk < 0.30:
        classification = "NORMAL"
    elif final_risk < 0.70:
        classification = "SUSPICIOUS"
    else:
        classification = "PHISHING"
        
    return round(final_risk, 2), classification