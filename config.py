import os

# Recipient Email
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "Atulchavan0020@gmail.com")

# Gmail SMTP Credentials (loaded from GitHub Secrets in the cloud)
GMAIL_USER = os.getenv("GMAIL_USER", "Atulchavan0020@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

# Search Target Roles & Keywords
TARGET_ROLES = [
    "data analyst",
    "data science",
    "data engineer",
    "software engineer",
    "software developer",
    "frontend developer",
    "backend developer",
    "intern",
    "internship",
    "fresher",
    "trainee",
    "graduate trainee"
]

# Positive Keywords (Must contain at least one)
ROLE_KEYWORDS = ["analyst", "science", "software", "developer", "engineer", "data"]
LEVEL_KEYWORDS = ["intern", "internship", "fresher", "trainee", "graduate", "junior", "associate", "entry level", "2026", "2027"]

# Negative / Exclude Keywords (Senior or irrelevant roles)
EXCLUDE_KEYWORDS = ["senior", "lead", "staff", "principal", "manager", "director", "5+ years", "6+ years", "7+ years"]

# Target Companies / Sample Portals for Greenhouse & Lever
GREENHOUSE_BOARDS = [
    {"name": "Agoda", "token": "agoda"},
    {"name": "Coinbase", "token": "coinbase"},
    {"name": "Figma", "token": "figma"},
    {"name": "GitLab", "token": "gitlab"},
    {"name": "Instacart", "token": "instacart"},
    {"name": "Pinterest", "token": "pinterest"},
    {"name": "Razorpay", "token": "razorpay"},
    {"name": "Stripe", "token": "stripe"},
    {"name": "Twitch", "token": "twitch"}
]

LEVER_BOARDS = [
    {"name": "Postman", "site": "postman"},
    {"name": "BrowserStack", "site": "browserstack"},
    {"name": "CleverTap", "site": "clevertap"}
]
