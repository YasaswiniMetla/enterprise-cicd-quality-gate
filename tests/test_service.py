from app.service import calculate_release_score


def test_release_ready():
    assert calculate_release_score(True, 95, True) == "READY"


def test_release_blocked_when_tests_fail():
    assert calculate_release_score(False, 95, True) == "BLOCKED"


def test_release_blocked_when_coverage_is_low():
    assert calculate_release_score(True, 70, True) == "BLOCKED"


def test_release_blocked_when_smoke_test_fails():
    assert calculate_release_score(True, 95, False) == "BLOCKED"
