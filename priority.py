
def calculate_priority(
    change_percentage,
    affected_people,
    infrastructure_affected
):
    """
    Rule-based disaster response priority estimation.
    Score ranges from 0 to 100.
    """

    # Visual change contribution: maximum 50 points
    visual_score = min(
        max(change_percentage, 0) / 50 * 50,
        50
    )

    # Affected population contribution: maximum 30 points
    population_score = min(
        max(affected_people, 0) / 500 * 30,
        30
    )

    # Critical infrastructure contribution: 20 points
    infrastructure_score = (
        20 if infrastructure_affected else 0
    )

    # Calculate total priority score
    total_score = round(
        visual_score
        + population_score
        + infrastructure_score
    )

    # Classify incident
    if total_score >= 70:
        priority = "CRITICAL"
        recommendation = (
            "Immediate field inspection and emergency response assessment."
        )

    elif total_score >= 45:
        priority = "HIGH"
        recommendation = (
            "Urgent inspection and resource allocation recommended."
        )

    elif total_score >= 20:
        priority = "MODERATE"
        recommendation = (
            "Schedule inspection and monitor the affected location."
        )

    else:
        priority = "LOW"
        recommendation = (
            "Routine monitoring and further verification recommended."
        )

    return {
        "score": total_score,
        "priority": priority,
        "recommendation": recommendation,
        "visual_score": round(visual_score, 2),
        "population_score": round(population_score, 2),
        "infrastructure_score": infrastructure_score
    }
