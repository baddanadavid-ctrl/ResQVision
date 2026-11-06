from streamlit_folium import st_folium
from map_module import create_damage_map
import streamlit as st
import pandas as pd
import plotly.express as px
import cv2

from image_analysis import analyze_images
from priority import calculate_priority

from database import (
    add_incident,
    get_incidents,
    update_incident_status
)

# PAGE CONFIGURATION
st.set_page_config(
    page_title="ResQVision",
    page_icon="🚨",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: white;
}

[data-testid="stMetric"] {
    background-color: #172238;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #263650;
}

h1, h2, h3 {
    color: #ffffff;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("🚨 ResQVision")
st.sidebar.caption("Disaster Intelligence Platform")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Image Analysis",
        "Incident Reports",
        "Damage Map",
        "Recovery Planning"
    ]
)

st.sidebar.divider()
st.sidebar.info("AI-Based Disaster Damage Assessment")

# DASHBOARD
if page == "Dashboard":

    st.title("Disaster Assessment Dashboard")

    st.caption(
        "AI-powered disaster monitoring and recovery planning"
    )

    st.divider()

    # STATISTICS
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Incidents", "25", "+5")
    col2.metric("Critical Priority", "5", "+2")
    col3.metric("High Priority", "8", "+3")
    col4.metric("Pending Inspection", "12")

    st.divider()

    # CHARTS
    left, right = st.columns(2)

    with left:

        st.subheader("Damage Severity Distribution")

        data = pd.DataFrame({
            "Severity": [
                "Critical",
                "High",
                "Moderate",
                "Low"
            ],
            "Count": [5, 8, 7, 5]
        })

        fig = px.pie(
            data,
            names="Severity",
            values="Count",
            hole=0.45,
            color="Severity",
            color_discrete_map={
                "Critical": "#ef4444",
                "High": "#f97316",
                "Moderate": "#eab308",
                "Low": "#22c55e"
            }
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#0b1120"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("Incident Overview")

        chart_data = pd.DataFrame({
            "Location": [
                "Zone A",
                "Zone B",
                "Zone C",
                "Zone D",
                "Zone E"
            ],
            "Incidents": [8, 5, 7, 3, 2]
        })

        fig2 = px.bar(
            chart_data,
            x="Location",
            y="Incidents",
            color="Incidents",
            color_continuous_scale="Oranges"
        )

        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#0b1120"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # RECENT INCIDENTS
    st.divider()

    st.subheader("Recent Disaster Reports")

    incidents = pd.DataFrame({
        "Location": [
            "Zone A",
            "Zone B",
            "Zone C",
            "Zone D"
        ],
        "Disaster Type": [
            "Flood",
            "Earthquake",
            "Storm",
            "Flood"
        ],
        "Priority": [
            "Critical",
            "High",
            "Moderate",
            "Low"
        ],
        "Status": [
            "Pending",
            "Under Review",
            "Pending",
            "Reviewed"
        ]
    })

    st.dataframe(
        incidents,
        use_container_width=True,
        hide_index=True
    )

# OTHER PAGES
elif page == "Image Analysis":

    st.title("Disaster Image Analysis")

    st.write(
        "Upload pre-disaster and post-disaster images "
        "to identify visual changes."
    )

    st.divider()

    # INCIDENT INFORMATION

    st.subheader("Incident Information")

    affected_people = st.number_input(
        "Estimated affected population",
        min_value=0,
        max_value=100000,
        value=50,
        step=10
    )

    infrastructure_affected = st.checkbox(
        "Critical infrastructure affected"
    )

    st.divider()

    # IMAGE UPLOAD

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Before Disaster")

        before = st.file_uploader(
            "Upload Before Image",
            type=["jpg", "jpeg", "png"],
            key="before_image"
        )

        if before:
            st.image(
                before,
                caption="Pre-disaster image",
                use_container_width=True
            )

    with col2:

        st.subheader("After Disaster")

        after = st.file_uploader(
            "Upload After Image",
            type=["jpg", "jpeg", "png"],
            key="after_image"
        )

        if after:
            st.image(
                after,
                caption="Post-disaster image",
                use_container_width=True
            )

    st.divider()

    # IMAGE ANALYSIS

    if st.button(
        "Analyze Disaster Images",
        use_container_width=True
    ):

        if before is not None and after is not None:

            try:

                with st.spinner("Analyzing images..."):

                    score, original, overlay, mask = (
                        analyze_images(before, after)
                    )

                st.success("Image comparison completed!")

                st.metric(
                    "Visual Change Percentage",
                    f"{score:.2f}%"
                )

                # PRIORITY CALCULATION

                result = calculate_priority(
                    score,
                    affected_people,
                    infrastructure_affected
                )

                st.divider()

                st.subheader("Disaster Priority Assessment")

                col3, col4 = st.columns(2)

                with col3:
                    st.metric(
                        "Priority Score",
                        f"{result['score']}/100"
                    )

                with col4:
                    st.metric(
                        "Incident Priority",
                        result["priority"]
                    )

                st.subheader("Score Breakdown")

                st.write(
                    f"Visual Change Score: "
                    f"{result['visual_score']}/50"
                )

                st.write(
                    f"Population Score: "
                    f"{result['population_score']}/30"
                )

                st.write(
                    f"Infrastructure Score: "
                    f"{result['infrastructure_score']}/20"
                )

                st.info(
                    f"Recommended Action: "
                    f"{result['recommendation']}"
                )

                # DISPLAY RESULTS

                st.subheader("Visual Comparison")

                result1, result2 = st.columns(2)

                with result1:

                    st.image(
                        original,
                        caption="Post-disaster image",
                        use_container_width=True
                    )

                with result2:

                    st.image(
                        overlay,
                        caption="Highlighted visual changes",
                        use_container_width=True
                    )

                st.subheader("Detected Change Mask")

                st.image(
                    mask,
                    caption="White regions show visual differences",
                    use_container_width=True
                )

                st.warning(
                    "Visual differences do not confirm "
                    "structural damage. Human inspection "
                    "is required."
                )

            except Exception as e:

                st.error(f"Image analysis failed: {e}")

        else:

            st.warning(
                "Please upload both before and after images."
            )



elif page == "Incident Reports":

    st.title("🚨 Incident Reporting System")

    st.write(
        "Register, manage and monitor disaster incidents."
    )

    st.divider()

    # NEW INCIDENT FORM

    st.subheader("Register New Incident")

    with st.form("incident_form"):

        title = st.text_input(
            "Incident Title",
            placeholder="Example: Heavy flooding in residential area"
        )

        disaster_type = st.selectbox(
            "Disaster Type",
            [
                "Flood",
                "Earthquake",
                "Fire",
                "Landslide",
                "Cyclone",
                "Other"
            ]
        )

        location = st.text_input(
            "Affected Location",
            placeholder="Enter city, area or village"
        )
        
        latitude = st.number_input(
            "Latitude",
            min_value=-90.0,
            max_value=90.0,
            value=12.9141,
            format="%.6f"
        )

        longitude = st.number_input(
            "Longitude",
            min_value=-180.0,
            max_value=180.0,
            value=74.8560,
            format="%.6f"
        )

        description = st.text_area(
            "Incident Description",
            placeholder="Describe the disaster and its impact..."
        )

        affected_people = st.number_input(
            "Estimated Affected Population",
            min_value=0,
            max_value=100000,
            value=0,
            step=10
        )

        severity = st.selectbox(
            "Severity Level",
            [
                "Critical",
                "High",
                "Moderate",
                "Low"
            ]
        )

        submitted = st.form_submit_button(
            "Submit Incident Report",
            use_container_width=True
        )

        if submitted:

            if not title.strip() or not location.strip():

                st.error(
                    "Please enter both incident title and location."
                )

            else:

                try:

                    add_incident(
                        title,
                        disaster_type,
                        location,
                        description,
                        affected_people,
                        severity,
                        latitude,
                        longitude
                    )

                    st.success(
                        "Incident report submitted successfully!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(f"Database error: {e}")

    st.divider()

    # DISPLAY SAVED INCIDENTS

    st.subheader("Registered Incidents")

    incidents = get_incidents()

    if incidents:

        st.metric(
            "Total Registered Incidents",
            len(incidents)
        )

        for incident in incidents:

            with st.expander(
                f"#{incident['id']} - {incident['title']}"
            ):

                st.write(
                    f"**Disaster Type:** {incident['disaster_type']}"
                )

                st.write(
                    f"**Location:** {incident['location']}"
                )

                st.write(
                    f"**Description:** {incident['description']}"
                )

                st.write(
                    f"**Affected People:** {incident['affected_people']}"
                )

                st.write(
                    f"**Severity:** {incident['severity']}"
                )

                st.write(
                    f"**Reported On:** {incident['created_at']}"
                )

                st.write(
                    f"**Current Status:** {incident['status']}"
                )

                new_status = st.selectbox(
                    "Update Incident Status",
                    [
                        "Pending",
                        "Under Investigation",
                        "Resolved"
                    ],
                    index=[
                        "Pending",
                        "Under Investigation",
                        "Resolved"
                    ].index(incident["status"]),
                    key=f"status_{incident['id']}"
                )

                if st.button(
                    "Update Status",
                    key=f"update_{incident['id']}"
                ):

                    update_incident_status(
                        incident["id"],
                        new_status
                    )

                    st.success("Incident status updated!")

                    st.rerun()

    else:

        st.info(
            "No incidents registered yet. Submit your first report above."
        )


elif page == "Damage Map":

    st.title("🗺️ Geographic Disaster Damage Map")

    st.write(
        "Visualize reported disaster locations "
        "and their severity levels."
    )

    st.divider()

    # Retrieve incidents from SQLite

    incidents = get_incidents()

    if incidents:

        # Keep only incidents with coordinates

        mapped_incidents = [
            incident for incident in incidents
            if incident.get("latitude") is not None
            and incident.get("longitude") is not None
        ]

        # Dashboard statistics

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Reports",
            len(incidents)
        )

        col2.metric(
            "Mapped Locations",
            len(mapped_incidents)
        )

        col3.metric(
            "Awaiting Coordinates",
            len(incidents) - len(mapped_incidents)
        )

        st.divider()

        st.subheader("Incident Location Map")

        st.markdown(
            """
            🔴 Critical &nbsp;&nbsp;
            🟠 High &nbsp;&nbsp;
            🟡 Moderate &nbsp;&nbsp;
            🟢 Low
            """
        )

        if mapped_incidents:

            damage_map = create_damage_map(
                mapped_incidents
            )

            st_folium(
                damage_map,
                width=None,
                height=600,
                key="disaster_map"
            )

        else:

            st.warning(
                "No incidents with coordinates found. "
                "Register a new incident with valid coordinates."
            )

        # Display incident details

        st.subheader("Incident Location Details")

        if mapped_incidents:

            map_data = pd.DataFrame(mapped_incidents)

            st.dataframe(
                map_data[
                    [
                        "title",
                        "location",
                        "severity",
                        "latitude",
                        "longitude",
                        "status"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

    else:

        st.info(
            "No incident reports found. "
            "Register an incident to populate the map."
        )

elif page == "Recovery Planning":
    st.title("Recovery Planning")
    st.info("Recovery recommendations will be implemented here.")
