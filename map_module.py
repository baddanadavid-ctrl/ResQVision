
import folium
import html


def create_damage_map(incidents):

    # Create map centred on Mangalore
    damage_map = folium.Map(
        location=[12.9141, 74.8560],
        zoom_start=12,
        tiles="OpenStreetMap"
    )

    # Severity colours
    colors = {
        "Critical": "red",
        "High": "orange",
        "Moderate": "beige",
        "Low": "green"
    }

    valid_locations = []

    for incident in incidents:

        latitude = incident.get("latitude")
        longitude = incident.get("longitude")

        # Skip incidents without coordinates
        if latitude is None or longitude is None:
            continue

        latitude = float(latitude)
        longitude = float(longitude)

        # Validate coordinates
        if not (-90 <= latitude <= 90):
            continue

        if not (-180 <= longitude <= 180):
            continue

        severity = incident["severity"]

        color = colors.get(severity, "gray")

        # Safely format incident details
        title = html.escape(str(incident["title"]))
        location = html.escape(str(incident["location"]))
        disaster_type = html.escape(str(incident["disaster_type"]))
        status = html.escape(str(incident["status"]))

        popup_text = f"""
        <b>Incident:</b> {title}<br>
        <b>Type:</b> {disaster_type}<br>
        <b>Location:</b> {location}<br>
        <b>Severity:</b> {html.escape(str(severity))}<br>
        <b>Affected People:</b> {incident['affected_people']}<br>
        <b>Status:</b> {status}
        """

        # Add incident marker
        folium.Marker(
            location=[latitude, longitude],

            popup=folium.Popup(
                popup_text,
                max_width=300
            ),

            tooltip=title,

            icon=folium.Icon(
                color=color,
                icon="info-sign"
            )

        ).add_to(damage_map)

        valid_locations.append(
            [latitude, longitude]
        )

    # Automatically adjust map position
    if len(valid_locations) == 1:

        damage_map.location = valid_locations[0]
        damage_map.zoom_start = 14

    elif len(valid_locations) > 1:

        damage_map.fit_bounds(valid_locations)

    return damage_map
