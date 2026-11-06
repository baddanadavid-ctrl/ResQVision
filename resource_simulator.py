
def simulate_allocation(incidents, rescue_teams, medical_kits, food_packages):
    if rescue_teams < 0 or medical_kits < 0 or food_packages < 0:
        raise ValueError("Resource quantities cannot be negative.")

    if not incidents:
        return []

    # Prioritize incidents by severity and affected population.
    severity_weight = {
        "Critical": 4,
        "High": 3,
        "Moderate": 2,
        "Low": 1
    }

    ordered = sorted(
        incidents,
        key=lambda incident: (
            severity_weight.get(incident["severity"], 0),
            int(incident["affected_people"] or 0)
        ),
        reverse=True
    )

    total_people = sum(
        max(0, int(item["affected_people"] or 0))
        for item in ordered
    )

    allocations = []

    remaining_teams = rescue_teams
    remaining_medical = medical_kits
    remaining_food = food_packages

    for incident in ordered:
        people = max(0, int(incident["affected_people"] or 0))

        if total_people > 0:
            medical_share = medical_kits * people / total_people
            food_share = food_packages * people / total_people
        else:
            medical_share = 0
            food_share = 0

        medical = min(
            remaining_medical,
            round(medical_share)
        )

        food = min(
            remaining_food,
            round(food_share)
        )

        remaining_medical -= medical
        remaining_food -= food

        teams = 0
        if remaining_teams > 0:
            teams = 1
            remaining_teams -= 1

        allocations.append({
            "incident_id": incident["id"],
            "location": incident["location"],
            "disaster_type": incident["disaster_type"],
            "severity": incident["severity"],
            "affected_people": people,
            "rescue_teams": teams,
            "medical_kits": medical,
            "food_packages": food
        })

    return allocations
