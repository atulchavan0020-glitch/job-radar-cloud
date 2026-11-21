# 🛰️ Cloud Job & Internship Radar (24/7 Automated Alert Bot)

An automated, serverless intelligence bot that runs **24/7 entirely in the cloud** via GitHub Actions. It monitors live Applicant Tracking Systems (Greenhouse, Lever, Workday) and career portals for authentic **Data Analyst, Data Science, and Software Engineering** internships and fresher roles—dispatching rich email alerts the moment a matching opening appears.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A[⏰ GitHub Actions Cloud Cron Schedule] -->|Triggers Every 2 Hours| B[Job Scanner Engine]
    B -->|API Fetch| C[Greenhouse Boards]
    B -->|API Fetch| D[Lever Boards]
    B -->|Scrape / Query| E[MNC / GCC Career Portals]
    C & D & E --> F{Filter & Deduplicate}
    F -->|Match Target Roles + Level| G[Check jobs_history.json]
    G -->|Already Notified| H[Skip]
    G -->|New Opening Found| I[Notifier Service]
    I -->|MIME / HTML Template| J[Gmail SMTP Server]
    J -->|Instant Notification| K[📬 Your Email Inbox]
    I -->|Update State| L[Commit Updated jobs_history.json to Repo]
```

---

## ✨ Features

- **24/7 Headless Cloud Execution**: Runs entirely on GitHub Actions runners—zero local computer resources required, operates seamlessly even when you are offline or sleeping.
- **Direct ATS API Integration**: Directly consumes structured REST APIs from Greenhouse and Lever, avoiding bot-blocking and ensuring 100% genuine postings.
- **Strict Role & Experience Filtering**:
  - Focuses on: *Data Analyst, Data Science, Software Engineer, Intern, Fresher*.
  - Automatically filters out: Senior roles (e.g., *Lead, Staff, Principal, 5+ yrs*).
  - Geolocation filtering: *India (Remote prioritized, Hybrid hubs)*.
- **Stateful Deduplication**: Maintains an immutable persistent history of job IDs (`jobs_history.json`) to guarantee zero duplicate alerts.
- **Responsive HTML Email Alerts**: Dispatches clean, mobile-friendly cards with direct application links.

