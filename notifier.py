import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from config import GMAIL_USER, GMAIL_APP_PASSWORD, ALERT_EMAIL

def send_job_alert_email(new_jobs):
    if not new_jobs:
        logging.info("No new jobs to notify.")
        return False

    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        logging.warning("GMAIL_USER or GMAIL_APP_PASSWORD not set. Skipping email dispatch.")
        return False

    subject = f"🚀 [Job Alert] {len(new_jobs)} New Fresher/Intern Openings Found!"
    
    # HTML Email Template
    html_items = ""
    plain_items = ""
    for idx, job in enumerate(new_jobs, 1):
        html_items += f"""
        <div style="background: #f9f9fb; border-left: 4px solid #2563eb; padding: 14px; margin-bottom: 14px; border-radius: 4px;">
            <h3 style="margin: 0 0 6px 0; color: #1e293b;">{idx}. {job['title']}</h3>
            <p style="margin: 4px 0; color: #475569;"><strong>Company:</strong> {job['company']}</p>
            <p style="margin: 4px 0; color: #475569;"><strong>Location:</strong> {job['location']}</p>
            <p style="margin: 4px 0; color: #475569;"><strong>Source:</strong> {job['source']}</p>
            <p style="margin: 10px 0 0 0;">
                <a href="{job['url']}" style="display: inline-block; background: #2563eb; color: #ffffff; text-decoration: none; padding: 7px 14px; border-radius: 4px; font-weight: 500;" target="_blank">
                    Apply Directly &rarr;
                </a>
            </p>
        </div>
        """
        plain_items += f"{idx}. {job['title']} at {job['company']}\nLocation: {job['location']}\nLink: {job['url']}\n\n"

    html_content = f"""
    <html>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #334155; line-height: 1.5; padding: 20px;">
        <h2 style="color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">
            🎯 Fresh Job & Internship Opportunities
        </h2>
        <p>Your 24/7 Cloud Job Radar identified <strong>{len(new_jobs)}</strong> new verified opening(s) matching your profile:</p>
        {html_items}
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin-top: 24px;" />
        <p style="font-size: 12px; color: #94a3b8;">
            Automated notification delivered via GitHub Actions Cloud Scheduler.
        </p>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Job Radar <{GMAIL_USER}>"
    msg["To"] = ALERT_EMAIL

    msg.attach(MIMEText(plain_items, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, [ALERT_EMAIL], msg.as_string())
        logging.info(f"Alert email sent successfully to {ALERT_EMAIL} with {len(new_jobs)} jobs.")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False
