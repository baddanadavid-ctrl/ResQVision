from resource_simulator import simulate_allocation
from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
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
    update_incident_status,
    add_rescue_team,
    get_rescue_teams,
    update_team_status,
    assign_rescue_team,
    get_rescue_assignments,
    update_rescue_assignment
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
        "Recovery Planning",
        "Rescue Gap Detector",
        "What-If Resource Simulator"
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
    st.write("Prioritized recovery recommendations based on registered incidents.")

    from recovery import generate_recovery_plan

    incidents = get_incidents()
    recovery_plans = generate_recovery_plan(incidents)

    if not recovery_plans:
        st.info("No incidents available. Register an incident first.")
    else:
        st.subheader("Recovery Priority Overview")

        for plan in recovery_plans:
            with st.expander(
                f"{plan['priority']} - {plan['location']} "
                f"({plan['disaster_type']})"
            ):
                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Severity:**", plan["severity"])
                    st.write("**Affected People:**", plan["affected_people"])
                    st.write("**Inspection:**", plan["inspection"])
                    st.write("**Recommended Action:**", plan["action"])

                with col2:
                    st.write("**Resource Level:**", plan["resource_level"])
                    st.write("**Medical Support:**", plan["medical"])
                    st.write("**Rescue Support:**", plan["rescue"])
                    st.write("**Supplies:**", plan["supplies"])

        st.success("Recovery plans generated successfully.")
        report = pd.DataFrame(recovery_plans)

        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=landscape(A3),
            rightMargin=25,
            leftMargin=25,
            topMargin=25,
            bottomMargin=25
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph("ResQVision - Disaster Recovery Report", styles["Title"])
        )
        elements.append(Spacer(1, 15))

        headers = [
            "ID", "Location", "Disaster", "Severity",
            "People", "Priority", "Inspection",
            "Medical", "Rescue", "Supplies",
            "Resource Level", "Recommended Action"
        ]

        data = [[Paragraph("<b>" + h + "</b>", styles["BodyText"]) for h in headers]]

        for plan in recovery_plans:
            values = [
                plan["id"],
                plan["location"],
                plan["disaster_type"],
                plan["severity"],
                plan["affected_people"],
                plan["priority"],
                plan["inspection"],
                plan["medical"],
                plan["rescue"],
                plan["supplies"],
                plan["resource_level"],
                plan["action"]
            ]

            data.append([
                Paragraph(escape(str(value)), styles["BodyText"])
                for value in values
            ])

        table = Table(
    data,
    colWidths=[
        30, 75, 65, 55, 45, 60,
        90, 50, 50, 50, 95, 145
    ],
    repeatRows=1
)

        table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#142B52")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B8C2CC")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("LEADING", (0, 0), (-1, -1), 10),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
     [colors.whitesmoke, colors.HexColor("#EAF0F6")]),
    ("PADDING", (0, 0), (-1, -1), 7)
]))
        elements.append(table)

        doc.build(elements)

        st.download_button(
            label="Download Recovery Report (PDF)",
            data=pdf_buffer.getvalue(),
            file_name="ResQVision_Recovery_Report.pdf",
            mime="application/pdf"
        )
        
elif page == "Rescue Gap Detector":
    st.title("🚨 Rescue Gap Detector")
    st.write("Manage rescue teams and monitor their availability.")

    st.subheader("Register a Rescue Team")

    with st.form("rescue_team_form"):
        team_name = st.text_input("Rescue Team Name")

        specialization = st.selectbox(
            "Team Specialization",
            ["Flood", "Fire", "Medical", "Mountain", "General"]
        )

        members = st.number_input(
            "Number of Team Members",
            min_value=1,
            max_value=500,
            value=5,
            step=1
        )

        submitted = st.form_submit_button("Register Rescue Team")

        if submitted:
            if team_name.strip():
                add_rescue_team(
                    team_name.strip(),
                    specialization,
                    int(members)
                )
                st.success("Rescue team registered successfully!")
                st.rerun()
            else:
                st.error("Please enter a team name.")

    st.divider()

    st.subheader("Registered Rescue Teams")

    teams = get_rescue_teams()

    if teams:
        st.dataframe(
            pd.DataFrame(teams),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No rescue teams registered yet.")
        
    st.divider()
                
    st.divider()

    st.subheader("📊 Rescue Operations Overview")

    all_teams = get_rescue_teams()
    all_incidents = get_incidents()
    all_assignments = get_rescue_assignments()

    total_teams = len(all_teams)

    available_count = sum(
        1 for team in all_teams
        if team["status"] == "Available"
    )

    assigned_count = sum(
        1 for team in all_teams
        if team["status"] == "Assigned"
    )

    assigned_ids = {
        item["incident_id"] for item in all_assignments
    }

    unassigned_high_priority = sum(
        1 for incident in all_incidents
        if incident["severity"] in ["Critical", "High"]
        and incident["id"] not in assigned_ids
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Teams", total_teams)
    col2.metric("Available Teams", available_count)
    col3.metric("Assigned Teams", assigned_count)
    col4.metric("Unassigned High-Priority", unassigned_high_priority)
    
    st.subheader("🚨 Rescue Gap Detection")

    incidents = get_incidents()
    assignments = get_rescue_assignments()
    teams = get_rescue_teams()

    assigned_incident_ids = {
        item["incident_id"] for item in assignments
    }

    unassigned_incidents = [
        incident for incident in incidents
        if incident["id"] not in assigned_incident_ids
    ]

    if not unassigned_incidents:
        st.success("All registered incidents have a rescue team assignment.")
    else:
        st.warning(
            f"{len(unassigned_incidents)} incident(s) "
            "are waiting for rescue team assignment."
        )

        available_teams = [
            team for team in teams
            if team["status"] == "Available"
        ]

        specialization_match = {
            "Flood": "Flood",
            "Fire": "Fire",
            "Earthquake": "Mountain",
            "Landslide": "Mountain",
            "Cyclone": "General"
        }

        for incident in unassigned_incidents:
            with st.expander(
                f"{incident['severity']} - "
                f"{incident['location']} ({incident['disaster_type']})"
            ):
                st.write("**Incident:**", incident["title"])
                st.write("**Affected people:**", incident["affected_people"])
                st.write("**Severity:**", incident["severity"])

                required = specialization_match.get(
                    incident["disaster_type"], "General"
                )

                recommended = [
                    team for team in available_teams
                    if team["specialization"] == required
                ]

                if not recommended:
                    recommended = [
                        team for team in available_teams
                        if team["specialization"] == "General"
                    ]

                if recommended:
                    suggested_team = recommended[0]

                    st.info(
                        f"Suggested team: {suggested_team['team_name']} "
                        f"({suggested_team['specialization']})"
                    )

                    team_options = {
                        f"{team['team_name']} - {team['specialization']} "
                        f"({team['members']} members)": team["id"]
                        for team in available_teams
                    }

                    option_labels = list(team_options.keys())

                    selected_label = st.selectbox(
                        "Select rescue team",
                        option_labels,
                        key=f"team_select_{incident['id']}"
                    )

                    if st.button(
                        "Assign Rescue Team",
                        key=f"assign_{incident['id']}"
                    ):
                        assign_rescue_team(
                            incident["id"],
                            team_options[selected_label]
                        )

                        st.success("Rescue team assigned successfully!")
                        st.rerun()

                else:
                    st.error(
                        "No available rescue team. "
                        "Register or make a team available first."
                    )
                
    st.divider()

    st.subheader("📋 Rescue Assignment Tracking")

    assignments = get_rescue_assignments()

    if not assignments:
        st.info("No rescue assignments have been made yet.")

    else:
        total_assigned = len(assignments)
        in_progress = sum(
            1 for item in assignments
            if item["status"] == "In Progress"
        )
        completed = sum(
            1 for item in assignments
            if item["status"] == "Completed"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Assignments", total_assigned)
        col2.metric("In Progress", in_progress)
        col3.metric("Completed", completed)

        for item in assignments:
            with st.expander(
                f"{item['team_name']} - {item['location']} "
                f"({item['status']})"
            ):
                st.write("**Incident:**", item["title"])
                st.write("**Location:**", item["location"])
                st.write("**Severity:**", item["severity"])
                st.write("**Rescue Team:**", item["team_name"])
                st.write("**Specialization:**", item["specialization"])

                new_status = st.selectbox(
                    "Update Assignment Status",
                    ["Assigned", "In Progress", "Completed"],
                    index=[
                        "Assigned",
                        "In Progress",
                        "Completed"
                    ].index(item["status"]),
                    key=f"assignment_status_{item['id']}"
                )

                if st.button(
                    "Update Status",
                    key=f"update_assignment_{item['id']}"
                ):
                    update_rescue_assignment(
                        item["id"],
                        new_status
                    )

                    st.success("Assignment status updated!")
                    st.rerun()


elif page == "What-If Resource Simulator":
    st.title("📊 What-If Resource Simulator")

    st.write(
        "Experiment with limited emergency resources "
        "and compare suggested allocations."
    )

    st.subheader("Available Emergency Resources")

    col1, col2, col3 = st.columns(3)

    with col1:
        rescue_teams = st.number_input(
            "Available Rescue Teams",
            min_value=0,
            max_value=500,
            value=5
        )

    with col2:
        medical_kits = st.number_input(
            "Available Medical Kits",
            min_value=0,
            max_value=10000,
            value=20
        )

    with col3:
        food_packages = st.number_input(
            "Available Food Packages",
            min_value=0,
            max_value=100000,
            value=100
        )

    st.divider()

    st.subheader("Resource Allocation Simulation")

    if st.button("Run Resource Simulation"):
        incidents = get_incidents()

        if not incidents:
            st.warning("No incidents registered. Add incidents first.")

        else:
            allocations = simulate_allocation(
                incidents,
                int(rescue_teams),
                int(medical_kits),
                int(food_packages)
            )

            st.success("Resource allocation simulation completed!")

            st.subheader("Suggested Resource Allocation")

            allocation_df = pd.DataFrame(allocations)

            st.dataframe(
                allocation_df,
                use_container_width=True,
                hide_index=True
            )
            
            st.divider()

            st.subheader("📊 Automatic Resource Allocation Summary")

            total_teams = int(allocation_df["rescue_teams"].sum())
            total_medical = int(allocation_df["medical_kits"].sum())
            total_food = int(allocation_df["food_packages"].sum())

            col1, col2, col3 = st.columns(3)

            col1.metric("Rescue Teams Allocated", total_teams)
            col2.metric("Medical Kits Allocated", total_medical)
            col3.metric("Food Packages Allocated", total_food)

            st.subheader("Resource Distribution by Location")

            allocation_df["area_label"] = allocation_df.apply(
                lambda row: f"{row['location']} - Incident {row['incident_id']}",
                axis=1
            )

            chart_df = allocation_df.set_index("area_label")[
                ["rescue_teams", "medical_kits", "food_packages"]
            ]

            st.bar_chart(chart_df)


