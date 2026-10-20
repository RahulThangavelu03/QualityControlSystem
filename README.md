# Factory Inspection & Quality Control System

A Django-based backend for factory inspection workflows, focused on gauge calibration validation, dimensional tolerance checks, and critical-to-quality (CTQ) failure handling.

## Features

- **Gauge Calibration:** Tracks gauge serial numbers, types, and calibration expiry dates.
- **Inspection Templates:** Defines part numbers, operation steps, customer agreements, revisions, and approval status.
- **Inspection Fields:** Supports dimensional inspection fields, tolerance limits, and CTQ classification.
- **Tolerance Validation:** Determines whether dimensional measurements fall within the permitted range, including tolerance boundaries.
- **CTQ Failure Handling:** Freezes an inspection when a critical-to-quality measurement fails.
- **Inspection Review:** Supports submission for supervisor review, approval, and rejection through model methods.
- **Automated Tests:** Covers gauge expiry, tolerance boundaries, CTQ freezing, and inspection workflow rules.

## Tech Stack

- Python
- Django
- SQLite
- Django automated testing framework

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Factory_Assigment_Code
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the dependencies listed in the project's requirements file. If a `requirements.txt` file is not included, create one or document the required packages before submitting.

```powershell
pip install django
```

### 4. Apply database migrations

```powershell
python manage.py migrate
```

### 5. Run the development server

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Run Tests

Execute the inspection app's automated tests:

```powershell
python manage.py test practice
```

The tests cover gauge calibration expiry, dimensional tolerance boundaries, CTQ failure freezing, and inspection submission and review behaviour.

## Business Rules

- A gauge is considered valid through its calibration expiry date.
- Dimensional measurements pass when they are within the inclusive lower and upper tolerance limits.
- Expired gauges cannot be used for new inspection entries.
- A failed CTQ measurement freezes the associated inspection.
- Only inspections in the appropriate workflow state can be submitted, approved, or rejected through the implemented model methods.

## Walkthrough Video

[Watch the project walkthrough] (https://drive.google.com/file/d/1ToztSO66br6lSnmaWsFIqS1ZX76WeS3_/view?usp=sharing)

## Repository

[View the source code](https://github.com/RahulThangavelu03/QualityControlSystem)

## Scope and Future Improvements

This submission implements the core Django models and selected quality-control business rules. Further work could include a complete inspection UI, role-based supervisor authorization, defect-photo validation, conditional concessions, template revision approval, and quality-head notifications.
