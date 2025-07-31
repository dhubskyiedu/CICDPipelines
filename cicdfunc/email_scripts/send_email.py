import os
import smtplib
from email.message import EmailMessage

# reading envs passed from GitHub Actions
# credentials
smtp_user = os.environ.get("SMTP_USER") # message bot's email
smtp_pass = os.environ.get("SMTP_PASS") # message bot's password
to_email = os.environ.get("TO_EMAIL") # project owner's/manager's email
# statuses
deps_status = os.environ.get("DEPS_STATUS", "unknown") # dependencies
build_status = os.environ.get("BUILD_STATUS", "unknown") # build status
test_status = os.environ.get("TEST_STATUS", "unknown") # test status

# Email subject and body
status_emojis = {
    "success": "✅",
    "failure": "❌"
}

if deps_status == "success" and build_status == "success" and test_status == "success":
    subject = "CI/CD Pipeline Succeeded ✅"
else:
    subject = "CI/CD Pipeline Issues Detected ❌"
body = f"""
Hello, dear Denys Hubskyi!
Here is the CI/CD pipeline status for your latest commit:
🔧 Dependency Installation: {deps_status+" "+status_emojis.get(deps_status, "❓")}
🛠️ Build: {build_status+" "+status_emojis.get(build_status, "❓")}
🧪 Tests: {test_status+" "+status_emojis.get(test_status, "❓")}
Best regards,  
GitHub Actions Bot
"""

# preparing the email
msg = EmailMessage()
msg["Subject"] = subject
msg["From"] = smtp_user
msg["To"] = to_email
msg.set_content(body)

# Send the email
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")