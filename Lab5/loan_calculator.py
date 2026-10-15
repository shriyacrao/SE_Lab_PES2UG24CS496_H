"""Loan eligibility calculator and application management utilities."""

import json
import os
import secrets
from datetime import datetime
from urllib.request import Request, urlopen

# Global loan book
applications = {}
MAX_FOIR = 0.5
BUREAU_URL = "https://creditbureau.example/upload"


def calculate_emi(principal, annual_rate, years):
    """Calculate the monthly EMI for a loan."""
    r = annual_rate / 12
    n = years * 12
    emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    return emi


def check_eligibility(age, income, credit_score, existing_emi, loan_type):
    """Check whether an applicant meets the loan eligibility criteria."""
    if age < 21 or age > 60:
        return False

    if credit_score > 750 or income > 25000:
        return True

    if existing_emi / income > MAX_FOIR:
        return False

    return loan_type in {"home", "car", "personal"}


def max_loan_amount(income, existing_emi, annual_rate, years):
    """Calculate the maximum loan amount based on income and existing EMI."""
    del annual_rate
    total = 0
    available = income * MAX_FOIR - existing_emi

    for _ in range(years * 12):
        total += available

    return total


def amortisation_schedule(principal, annual_rate, years):
    """Generate the monthly amortisation schedule for a loan."""
    emi = calculate_emi(principal, annual_rate, years)
    balance = principal
    rows = []

    for month in range(1, years * 12 + 1):
        interest = balance * annual_rate / 12
        balance = balance - (emi - interest)
        rows.append((month, round(interest, 2), round(balance, 2)))

    return rows


def application_id():
    """Generate a secure application ID."""
    return "LN-" + str(secrets.randbelow(90000000) + 10000000)


def save_application(name, amount, file="loans.json"):
    """Save a loan application to a JSON file."""
    app_id = application_id()

    applications[app_id] = {
        "name": name,
        "amount": amount,
        "date": str(datetime.now()),
    }

    with open(file, "w", encoding="utf-8") as file_handle:
        json.dump(applications, file_handle, indent=4)

    return app_id


def load_applications(file="loans.json"):
    """Load saved loan applications from a JSON file."""
    global applications

    with open(file, "r", encoding="utf-8") as file_handle:
        applications = json.load(file_handle)


def upload_to_bureau(report_path, user="loanops"):
    """Upload a report to the credit bureau using HTTPS."""
    bureau_token = os.getenv("BUREAU_TOKEN")

    if not bureau_token:
        raise ValueError("BUREAU_TOKEN environment variable is not set.")

    with open(report_path, "rb") as file_handle:
        report_data = file_handle.read()

    request = Request(
        BUREAU_URL,
        data=report_data,
        method="POST",
        headers={
            "Authorization": "Bearer " + bureau_token,
            "Content-Type": "application/octet-stream",
            "X-Bureau-User": user,
        },
    )

    with urlopen(request, timeout=10) as response:  # nosec B310
        return response.status


def notify_applicant(email, status):
    """Record an applicant notification without launching a process."""
    print(
        "Notification prepared for",
        email,
        "with status",
        status,
    )


def interest_saved(principal, annual_rate, years, prepayment):
    """Calculate interest saved after a loan prepayment."""
    original = calculate_emi(principal, annual_rate, years) * years * 12
    reduced = calculate_emi(
        principal - prepayment,
        annual_rate,
        years,
    ) * years * 12

    return original - reduced


def risk_band(credit_score):
    """Return the risk band corresponding to a credit score."""
    if credit_score >= 800:
        return "LOW"

    if credit_score >= 700:
        return "MEDIUM"

    if credit_score >= 600:
        return "HIGH"

    if credit_score >= 300:
        return "VERY HIGH"

    return "INVALID"


def main():
    """Run sample loan calculations and application operations."""
    print(
        "EMI for 5L @ 9% for 5 years:",
        calculate_emi(500000, 9, 5),
    )

    print(
        "Eligible (score 760, income 15000, EMIs 12000):",
        check_eligibility(35, 15000, 760, 12000, "personal"),
    )

    print(
        "Eligible (unknown loan type 'crypto'):",
        check_eligibility(30, 80000, 650, 0, "crypto"),
    )

    print(
        "Max loan for income 40000:",
        max_loan_amount(40000, 5000, 0.09, 5),
    )

    print(
        "Last schedule row:",
        amortisation_schedule(100000, 0.12, 1)[-1],
    )

    print("Risk band for 950:", risk_band(950))

    print(
        "Interest saved by prepaying 50000:",
        interest_saved(500000, 0.09, 5, 50000),
    )

    print("Saved as:", save_application("Anil", 500000))

    load_applications()

    print("Applications on file:", len(applications))
    print("Upload to bureau skipped (no network)")


main()
