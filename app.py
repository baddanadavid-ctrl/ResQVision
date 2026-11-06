
import streamlit as st
import pandas as pd
import plotly.express as px
import cv2
from image_analysis import analyze_images

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

    st.title("🛰️ Disaster Image Analysis")

    st.write(
        "Upload pre-disaster and post-disaster images "
        "to identify visual changes."
    )

    st.divider()

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

    if st.button(
        "🔍 Analyze Disaster Images",
        use_container_width=True
    ):

        if before is not None and after is not None:

            try:

                with st.spinner("Analyzing images..."):

                    score, original, overlay, mask = (
                        analyze_images(before, after)
                    )

                st.success("Image comparison completed!")

                st.subheader("Visual Change Analysis")

                st.metric(
                    "Visual Change Percentage",
                    f"{score:.2f}%"
                )

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
                    caption="White regions indicate detected visual differences",
                    use_container_width=True
                )

                st.warning(
                    "This result represents visual differences, "
                    "not confirmed structural damage. "
                    "Human inspection is required."
                )

            except Exception as e:

                st.error(f"Image analysis failed: {e}")

        else:

            st.warning(
                "Please upload both before and after images."
            )

elif page == "Incident Reports":
    st.title("Incident Reporting")
    st.info("Disaster incident reporting will be implemented here.")

elif page == "Damage Map":
    st.title("Geographic Damage Map")
    st.info("Interactive disaster location mapping will be implemented here.")

elif page == "Recovery Planning":
    st.title("Recovery Planning")
    st.info("Recovery recommendations will be implemented here.")
