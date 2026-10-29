"""
Lab 6 - Step 5: tests written to reach (at least) 90% LINE coverage
of course_registration.py.

Run:
    coverage run -m pytest CodeCoverageTest_course_registration.py
    coverage report -m
"""
import pytest
from course_registration import can_register, waitlist_position, late_fee


# ---------------- can_register ----------------
def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"


def test_unknown_status_raises():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("alumni", 10, 4, True)


def test_invalid_course_credits_raises():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)


def test_prerequisites_missing():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"


def test_credit_limit_exceeded():
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"


# ---------------- waitlist_position ----------------
def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0


def test_invalid_capacity_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, 0, 0)


def test_waitlist_full():
    assert waitlist_position(40, 40, 10) == -1


def test_waitlist_position_assigned():
    assert waitlist_position(40, 40, 3) == 4


# ---------------- late_fee ----------------
def test_not_late():
    assert late_fee(0, 18, False) == 0


def test_waiver_applied():
    assert late_fee(5, 18, True) == 0


def test_late_within_week_heavy_load():
    # 500 base + 250 for > 20 credits
    assert late_fee(3, 25, False) == 750


def test_late_beyond_week_fee_capped():
    # 500 + 23*100 + 250 = 3050 -> capped at 2000
    assert late_fee(30, 25, False) == 2000
