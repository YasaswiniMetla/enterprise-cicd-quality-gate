def calculate_release_score(test_passed: bool, coverage: float, smoke_passed: bool) -> str:
    if not test_passed or not smoke_passed:
        return "BLOCKED"

    if coverage < 80:
        return "BLOCKED"

    return "READY"
