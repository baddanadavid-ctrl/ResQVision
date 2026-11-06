
def generate_recovery_plan(incidents):

    recovery_plans = []

    for incident in incidents:

        severity = incident["severity"]

        people = incident["affected_people"]

        disaster_type = incident["disaster_type"]

        # Determine inspection priority

        if severity == "Critical":

            priority = "Immediate"

            inspection = "Immediate field inspection"

            medical = "High"

            rescue = "High"

            supplies = "High"

        elif severity == "High":

            priority = "Urgent"

            inspection = "Urgent inspection required"

            medical = "Medium"

            rescue = "High"

            supplies = "High"

        elif severity == "Moderate":

            priority = "Scheduled"

            inspection = "Schedule field inspection"

            medical = "Medium"

            rescue = "Medium"

            supplies = "Medium"

        else:

            priority = "Routine"

            inspection = "Routine monitoring"

            medical = "Low"

            rescue = "Low"

            supplies = "Low"

        # Additional recommendations by disaster type

        if disaster_type == "Flood":

            action = "Assess water levels, evacuation needs and drinking water."

        elif disaster_type == "Earthquake":

            action = "Inspect structural damage and identify unsafe buildings."

        elif disaster_type == "Fire":

            action = "Assess fire containment, smoke exposure and evacuation."

        elif disaster_type == "Landslide":

            action = "Inspect slope stability and identify blocked roads."

        elif disaster_type == "Cyclone":

            action = "Assess wind damage, damaged infrastructure and shelter needs."

        else:

            action = "Conduct field assessment and identify recovery requirements."

        # Population-based planning estimate

        if people >= 500:

            resource_level = "Large-scale support"

        elif people >= 100:

            resource_level = "Medium-scale support"

        else:

            resource_level = "Basic support"

        recovery_plans.append({

            "id": incident["id"],

            "location": incident["location"],

            "disaster_type": disaster_type,

            "severity": severity,

            "affected_people": people,

            "priority": priority,

            "inspection": inspection,

            "medical": medical,

            "rescue": rescue,

            "supplies": supplies,

            "resource_level": resource_level,

            "action": action

        })

    # Sort urgent incidents first

    priority_order = {

        "Immediate": 1,

        "Urgent": 2,

        "Scheduled": 3,

        "Routine": 4

    }

    recovery_plans.sort(

        key=lambda x: (
            priority_order[x["priority"]],
            -x["affected_people"]
        )

    )

    return recovery_plans
