
import os
from datetime import timedelta

import streamlit as st
import pandas as pd
import pymysql
from dotenv import load_dotenv


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

st.set_page_config(
    page_title="IoT Cloud Analytics",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# 2. CUSTOM DESIGN
# --------------------------------------------------

st.markdown(
    """
    <style>
        .stApp {
            background-color: #0b1220;
            color: #e5edf7;
        }

        [data-testid="stHeader"] {
            background-color: #0b1220;
        }

        [data-testid="stSidebar"] {
            background-color: #111c2e;
            border-right: 1px solid #263750;
        }

        [data-testid="stSidebar"] * {
            color: #e5edf7 !important;
        }

        h1, h2, h3 {
            color: #f0f6ff !important;
        }

        .main-title {
            font-size: 36px;
            font-weight: 800;
            color: #38bdf8;
            letter-spacing: 1px;
        }

        .subtitle {
            color: #94a9c3;
            font-size: 16px;
        }

        [data-testid="stMetric"] {
            background-color: #16243a;
            border: 1px solid #263b57;
            padding: 22px;
            border-radius: 14px;
        }

        [data-testid="stMetricValue"] {
            color: #38bdf8 !important;
        }

        .status-box {
            background-color: #123b36;
            border: 1px solid #168b72;
            color: #6ee7c0;
            padding: 15px;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 3. DATABASE CONNECTION
# --------------------------------------------------


def get_connection():
    return pymysql.connect(
        host=st.secrets["DB_HOST"],
        port=int(st.secrets["DB_PORT"]),
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"],
        connect_timeout=10
    )


@st.cache_data(ttl=60, show_spinner=False)
def fetch_data(query, params=()):
    connection = get_connection()

    try:
        return pd.read_sql_query(
            query,
            connection,
            params=params
        )
    finally:
        connection.close()


# --------------------------------------------------
# 4. SIDEBAR AND FILTERS
# --------------------------------------------------

st.sidebar.markdown("## 🌐 IoT Analytics")
st.sidebar.caption("AWS Cloud Monitoring Platform")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Sensor Analysis",
        "Light & Motion",
        "Recent Readings"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### 🔎 Data Filters")


try:

    # Database information
    db_info = fetch_data("""
        SELECT
            MIN(timestamp) AS min_date,
            MAX(timestamp) AS max_date
        FROM sensor_readings
    """)

    sensor_list = fetch_data("""
        SELECT DISTINCT sensor_id
        FROM sensor_readings
        ORDER BY sensor_id
    """)

    min_date = pd.to_datetime(
        db_info.iloc[0]["min_date"]
    ).date()

    max_date = pd.to_datetime(
        db_info.iloc[0]["max_date"]
    ).date()

    selected_dates = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    selected_sensor = st.sidebar.selectbox(
        "Select Sensor",
        ["All Sensors"] + sensor_list["sensor_id"].tolist()
    )

    if len(selected_dates) != 2:
        st.warning("Please select both start and end dates.")
        st.stop()

    start_date, end_date = selected_dates

    if start_date > end_date:
        st.error("Start date cannot be after end date.")
        st.stop()

    # SQL filter conditions
    conditions = [
        "timestamp >= %s",
        "timestamp < %s"
    ]

    params = [
        start_date,
        end_date + timedelta(days=1)
    ]

    if selected_sensor != "All Sensors":
        conditions.append("sensor_id = %s")
        params.append(selected_sensor)

    where_clause = " WHERE " + " AND ".join(conditions)
    params = tuple(params)

    st.sidebar.divider()
    st.sidebar.caption("Database: AWS RDS MySQL")
    st.sidebar.caption("Table: sensor_readings")


    # --------------------------------------------------
    # 5. HEADER
    # --------------------------------------------------

    st.markdown(
        '<div class="main-title">🌐 IoT CLOUD ANALYTICS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Cloud-based Sensor Monitoring '
        'and Database Analytics | Powered by AWS RDS</div>',
        unsafe_allow_html=True
    )

    st.caption(
        f"📅 Data Period: {start_date} to {end_date} "
        f" | Sensor: {selected_sensor}"
    )

    st.write("")
    st.divider()


    # --------------------------------------------------
    # 6. OVERALL STATISTICS
    # --------------------------------------------------

    summary = fetch_data(f"""
        SELECT
            COUNT(*) AS total_records,
            AVG(temperature) AS avg_temp,
            AVG(humidity) AS avg_humidity,
            AVG(co) AS avg_co,
            AVG(lpg) AS avg_lpg,
            AVG(smoke) AS avg_smoke
        FROM sensor_readings
        {where_clause}
    """, params)

    data = summary.iloc[0]

    if int(data["total_records"]) == 0:
        st.warning("No sensor readings found for these filters.")
        st.stop()

    st.markdown("## 📊 Overall Sensor Statistics")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Readings",
        f"{int(data['total_records']):,}"
    )

    c2.metric(
        "Average Temperature",
        f"{data['avg_temp']:.2f} °C"
    )

    c3.metric(
        "Average Humidity",
        f"{data['avg_humidity']:.2f} %"
    )

    c4, c5, c6 = st.columns(3)

    c4.metric("Average CO", f"{data['avg_co']:.6f}")
    c5.metric("Average LPG", f"{data['avg_lpg']:.6f}")
    c6.metric("Average Smoke", f"{data['avg_smoke']:.6f}")

    st.divider()


    # --------------------------------------------------
    # 7. PAGE: OVERVIEW
    # --------------------------------------------------

    if page == "Overview":

        st.markdown("## 📈 Hourly Temperature Trends")

        hourly = fetch_data(f"""
            SELECT
                HOUR(timestamp) AS hour,
                AVG(temperature) AS avg_temperature
            FROM sensor_readings
            {where_clause}
            GROUP BY HOUR(timestamp)
            ORDER BY hour
        """, params)

        st.line_chart(
            hourly.set_index("hour"),
            y="avg_temperature",
            color="#38bdf8"
        )

        st.caption(
            "Average temperature grouped by hour of day."
        )

        st.divider()

        st.markdown("## 📡 Sensor Overview")

        sensor_data = fetch_data(f"""
            SELECT
                sensor_id,
                AVG(temperature) AS avg_temperature,
                AVG(humidity) AS avg_humidity,
                COUNT(*) AS total_readings
            FROM sensor_readings
            {where_clause}
            GROUP BY sensor_id
            ORDER BY total_readings DESC
        """, params)

        # Create readable labels for charts
        chart_data = sensor_data.copy()

        chart_data["sensor_label"] = [
            f"Sensor {i+1} ({str(sensor_id)[-5:]})"
            for i, sensor_id in enumerate(chart_data["sensor_id"])
        ]

        chart_data = chart_data.set_index("sensor_label")

        left, right = st.columns(2)

        with left:
            st.markdown("**Average Temperature**")

            st.bar_chart(
                chart_data[["avg_temperature"]],
                color="#38bdf8"
            )

        with right:
            st.markdown("**Average Humidity**")

            st.bar_chart(
                chart_data[["avg_humidity"]],
                color="#a78bfa"
            )

        st.dataframe(
            sensor_data,
            width="stretch",
            hide_index=True
        )


    # --------------------------------------------------
    # 8. PAGE: SENSOR ANALYSIS
    # --------------------------------------------------

    elif page == "Sensor Analysis":

        st.markdown("## 📡 Detailed Sensor Analysis")

        sensor_data = fetch_data(f"""
            SELECT
                sensor_id,
                AVG(temperature) AS avg_temperature,
                MIN(temperature) AS min_temperature,
                MAX(temperature) AS max_temperature,
                AVG(humidity) AS avg_humidity,
                MIN(humidity) AS min_humidity,
                MAX(humidity) AS max_humidity,
                COUNT(*) AS total_readings
            FROM sensor_readings
            {where_clause}
            GROUP BY sensor_id
        """, params)

        st.markdown("### Temperature Comparison")

        st.bar_chart(
            sensor_data.set_index("sensor_id")[
                ["avg_temperature"]
            ],
            color="#38bdf8"
        )

        st.markdown("### Humidity Comparison")

        st.bar_chart(
            sensor_data.set_index("sensor_id")[
                ["avg_humidity"]
            ],
            color="#a78bfa"
        )

        st.markdown("### Sensor Statistics")

        st.dataframe(
            sensor_data,
            width="stretch",
            hide_index=True
        )


    # --------------------------------------------------
    # 9. PAGE: LIGHT AND MOTION
    # --------------------------------------------------

    elif page == "Light & Motion":

        st.markdown("## 💡 Light and Motion Detection")

        detection = fetch_data(f"""
            SELECT
                SUM(light = 1) AS light_on,
                SUM(light = 0) AS light_off,
                SUM(motion = 1) AS motion_detected,
                SUM(motion = 0) AS no_motion
            FROM sensor_readings
            {where_clause}
        """, params)

        d = detection.iloc[0]

        total_light = (
            (d["light_on"] or 0) +
            (d["light_off"] or 0)
        )

        total_motion = (
            (d["motion_detected"] or 0) +
            (d["no_motion"] or 0)
        )

        st.markdown("### Detection Summary")

        col1, col2 = st.columns(2)

        with col1:
            light_percentage = (
                (d["light_on"] or 0) / total_light * 100
                if total_light else 0
            )

            st.metric(
                "Light ON Percentage",
                f"{light_percentage:.2f}%"
            )

        with col2:
            motion_percentage = (
                (d["motion_detected"] or 0) / total_motion * 100
                if total_motion else 0
            )

            st.metric(
                "Motion Detection Percentage",
                f"{motion_percentage:.2f}%"
            )

        st.divider()

        a, b = st.columns(2)

        with a:
            st.markdown("### Light Detection")

            st.metric(
                "Light ON",
                f"{int(d['light_on'] or 0):,}"
            )

            st.metric(
                "Light OFF",
                f"{int(d['light_off'] or 0):,}"
            )

            st.bar_chart(
                pd.DataFrame(
                    {
                        "Readings": [
                            d["light_on"],
                            d["light_off"]
                        ]
                    },
                    index=["Light ON", "Light OFF"]
                ),
                color="#fbbf24"
            )

        with b:
            st.markdown("### Motion Detection")

            st.metric(
                "Motion Detected",
                f"{int(d['motion_detected'] or 0):,}"
            )

            st.metric(
                "No Motion",
                f"{int(d['no_motion'] or 0):,}"
            )

            st.bar_chart(
                pd.DataFrame(
                    {
                        "Readings": [
                            d["motion_detected"],
                            d["no_motion"]
                        ]
                    },
                    index=["Motion Detected", "No Motion"]
                ),
                color="#34d399"
            )


    # --------------------------------------------------
    # 10. PAGE: RECENT DATABASE READINGS
    # --------------------------------------------------

    elif page == "Recent Readings":

        st.markdown("## 📋 Recent Sensor Readings")

        recent = fetch_data(f"""
            SELECT
                timestamp,
                sensor_id,
                temperature,
                humidity,
                co,
                lpg,
                smoke,
                light,
                motion
            FROM sensor_readings
            {where_clause}
            ORDER BY timestamp DESC
            LIMIT 100
        """, params)

        st.caption(
            "Showing the latest 100 matching records."
        )

        st.dataframe(
            recent,
            width="stretch",
            hide_index=True
        )

        csv_data = recent.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download CSV Report",
            data=csv_data,
            file_name="iot_sensor_report.csv",
            mime="text/csv"
        )


    # --------------------------------------------------
    # 11. DATABASE STATUS
    # --------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="status-box">'
        '● Connected successfully to AWS RDS MySQL'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "IoT Cloud Analytics | Python | Streamlit | "
        "MySQL | AWS RDS"
    )

    if st.button("🔄 Refresh Dashboard"):
        st.cache_data.clear()
        st.rerun()


except Exception as e:

    st.error("Unable to load dashboard data.")

    st.exception(e)

    st.info(
        "Check your AWS RDS connection, security group, "
        "and .env configuration."
    )
