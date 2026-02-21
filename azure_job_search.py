import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# ========================
# CONFIGURATION
# ========================

APP_ID = "44fd0e97"
APP_KEY = "6ed353356a3ae9456f6c89f28a7886a4"

EMAIL_SENDER = "inapakollakishore76@gmail.com"
EMAIL_PASSWORD = "dhgrnzdnqzupyzug"
EMAIL_RECEIVER = "inapakollakishore76@gmail.com"

SEARCH_TERMS = """
Azure Data Engineer
Azure Data Factory
Azure Databricks
PySpark
Azure Synapse
SQL
Data Modeling
6+ years
"""

LOCATIONS = ["India", "Remote"]

# ========================
# JOB SEARCH FUNCTION
# ========================

def search_jobs():
    results = []

    for location in LOCATIONS:
        url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": 20,
            "what": SEARCH_TERMS,
            "where": location,
            "content-type": "application/json",
        }

        response = requests.get(url, params=params)
        jobs = response.json().get("results", [])

        for job in jobs:
            description = job.get("description", "").lower()

            # Experience filter
            if not ("6+" in description or "6 years" in description):
                continue

            # Skill filters
            required_skills = [
                "azure data factory",
                "azure databricks",
                "pyspark",
                "azure synapse",
                "sql",
                "python",
                "microsoft fabric",
                "data modeling",
                "medallion architecture"
            ]

            if all(skill in description for skill in required_skills):
                results.append({
                    "title": job.get("title"),
                    "company": job.get("company", {}).get("display_name"),
                    "location": job.get("location", {}).get("display_name"),
                    "link": job.get("redirect_url")
                })

    return results

# ========================
# FORMAT EMAIL
# ========================

def format_email(jobs):
    if not jobs:
        return f"No matching Azure Data Engineer jobs found.\n\nRun Time: {datetime.now()}"

    body = f"Azure Data Engineer Job Search Results\n"
    body += f"Run Time: {datetime.now()}\n\n"

    for i, job in enumerate(jobs, 1):
        body += f"""
{i}) Job Title: {job['title']}
Company: {job['company']}
Location: {job['location']}
Required Skills: ADF, ADB, PySpark, Synapse, SQL, Data Modeling, python, microsoft fabric, data modelling, medallion architecture
Link: {job['link']}

"""

    return body

# ========================
# SEND EMAIL
# ========================

def send_email(body):
    msg = MIMEText(body)
    msg["Subject"] = "Azure Data Engineer Jobs (6+ Years) – Auto Search"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

# ========================
# MAIN
# ========================

if __name__ == "__main__":
    jobs = search_jobs()
    email_body = format_email(jobs)
    send_email(email_body)
