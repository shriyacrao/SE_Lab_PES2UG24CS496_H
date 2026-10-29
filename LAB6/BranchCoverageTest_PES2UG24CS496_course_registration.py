import pytest
from course_registration import can_register, waitlist_position, late_fee


# ---------- can_register ----------

def test_can_register_unknown_status():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("unknown", 10, 3, True)


def test_can_register_invalid_course_credits():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)


def test_can_register_prerequisites_missing():
    assert can_register("regular", 10, 3, False) == "prerequisites missing"


def test_can_register_credit_limit_exceeded():
    assert can_register("regular", 22, 3, True) == "credit limit exceeded"


def test_can_register_exact_credit_limit():
    assert can_register("regular", 20, 4, True) == "registered"


def test_can_register_one_over_limit():
    assert can_register("regular", 21, 4, True) == "credit limit exceeded"


def test_can_register_smallest_valid_course():
    assert can_register("regular", 10, 1, True) == "registered"


def test_can_register_probation_limit():
    assert can_register("probation", 12, 4, True) == "registered"


def test_can_register_honors_limit():
    assert can_register("honors", 24, 4, True) == "registered"


# ---------- waitlist_position ----------

def test_waitlist_invalid_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(5, 0, 2)


def test_waitlist_seat_available():
    assert waitlist_position(30, 40, 0) == 0


def test_waitlist_one_seat_left():
    assert waitlist_position(39, 40, 5) == 0


def test_waitlist_class_full():
    assert waitlist_position(40, 40, 0) == 1


def test_waitlist_position_assigned():
    assert waitlist_position(40, 40, 3) == 4


def test_waitlist_length_nine():
    assert waitlist_position(40, 40, 9) == 10


def test_waitlist_full():
    assert waitlist_position(40, 40, 10) == -1


def test_waitlist_beyond_limit():
    assert waitlist_position(40, 40, 15) == -1


# ---------- late_fee ----------

def test_late_fee_zero_days():
    assert late_fee(0, 18, False) == 0


def test_late_fee_negative_days():
    assert late_fee(-2, 18, False) == 0


def test_late_fee_with_waiver():
    assert late_fee(5, 18, True) == 0


def test_late_fee_one_day():
    assert late_fee(1, 18, False) == 500


def test_late_fee_seven_days():
    assert late_fee(7, 18, False) == 500


def test_late_fee_eight_days():
    assert late_fee(8, 18, False) == 600


def test_late_fee_ten_days():
    assert late_fee(10, 18, False) == 800


def test_late_fee_exactly_twenty_credits():
    assert late_fee(3, 20, False) == 500


def test_late_fee_over_twenty_credits():
    assert late_fee(3, 21, False) == 750


def test_late_fee_heavy_load_after_week():
    assert late_fee(8, 25, False) == 850


def test_late_fee_exactly_at_cap():
    assert late_fee(21, 20, False) == 1900


def test_late_fee_reaches_cap():
    assert late_fee(30, 20, False) == 2000


def test_late_fee_exceeds_cap_with_surcharge():
    assert late_fee(30, 25, False) == 2000