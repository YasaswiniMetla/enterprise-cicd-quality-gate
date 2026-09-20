from app.service import calculate_release_score

result = calculate_release_score(True, 100, True)

if result != "READY":
    raise SystemExit("Deployment smoke validation failed")

print("Deployment smoke validation passed")
