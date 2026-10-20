# Factory Inspection and Quality Control System

A Django-based application for managing factory inspections, gauge calibration checks, measurement tolerances, and supervisor review workflows.

## Features

- **Gauge calibration:** Detects expired gauges and blocks their use with an `Expired Tool Calibration` validation error.
- **Measurement validation:** Checks dimensional measurements against inclusive lower and upper tolerance limits.
- **CTQ failure handling:** Freezes an inspection when a Critical-to-Quality (CTQ) measurement fails.
- **Inspection workflow:** Supports in-progress, pending review, approved, rejected, and frozen inspection states.
- **Supervisor review:** Supports approval and rejection of inspections pending review.
- **Audit fields:** Records inspection creation time, entry creation time, inspector, reviewer, and review timestamp fields.
- **Automated tests:** Covers calibration expiry, tolerance boundaries, CTQ freezing, review transitions, and preventing entries after submission.

## Tech Stack

- Python
- Django
- SQLite
- Django Test Framework

## Setup

1. Clone or download the repository.
2. Create and activate a virtual environment.
3. Install Django:

   ```bash
   pip install django
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Open `http://127.0.0.1:8000/` in your browser.

## Run Tests

Run the app's tests with:

```bash
python manage.py test practice
```

## Current Scope and Future Improvements

Further work can include authenticated role-based supervisor permissions, defect photo uploads with a two-photo minimum, conditional concessions with justification and reason codes, immutable audit logs, and a complete user interface for inspection submission and review.
