# 🌐 IoT Cloud Analytics
### Cloud-Based IoT Sensor Monitoring and Data Analytics Using AWS RDS

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.67-red?logo=streamlit)
![MySQL](https://img.shields.io/badge/Database-MySQL-4479A1?logo=mysql)
![AWS](https://img.shields.io/badge/Cloud-AWS%20RDS-orange?logo=amazonaws)
![Deployment](https://img.shields.io/badge/Deployment-Live-success)

## 📌 Project Overview

IoT Cloud Analytics is a cloud-based data monitoring and visualization platform developed to analyze IoT sensor readings stored in a cloud-hosted relational database.

The project integrates Python, MySQL, Amazon Web Services (AWS) RDS, and Streamlit to create an interactive analytics dashboard for monitoring environmental sensor parameters.

It enables users to explore sensor data, analyze temperature and humidity variations, monitor gas measurements, and examine light and motion detection patterns through interactive visualizations.

The application demonstrates the integration of Internet of Things (IoT), cloud computing, database management, and data analytics.

## 🎯 Project Objectives

- Store and manage IoT sensor readings using a relational database.
- Implement a cloud-hosted MySQL database using AWS RDS.
- Establish secure database connectivity using Python.
- Perform statistical analysis on sensor measurements.
- Develop interactive visualizations using Streamlit.
- Enable sensor-wise and date-wise data filtering.
- Deploy the analytics dashboard on Streamlit Community Cloud.

## ✨ Key Features

### 1. Overview Dashboard
- Total number of sensor readings.
- Average temperature and humidity.
- Average CO, LPG, and smoke measurements.
- Overall sensor statistics.

### 2. Sensor Analysis
- Sensor-wise temperature comparison.
- Sensor-wise humidity comparison.
- Individual sensor performance analysis.
- Graphical representation of sensor measurements.

### 3. Light and Motion Analysis
- Light ON and OFF statistics.
- Motion detection statistics.
- Motion detection percentage.
- Environmental activity monitoring.

### 4. Recent Readings
- Access to historical sensor records.
- Exploration of individual sensor readings.
- Database-driven data presentation.

### 5. Interactive Data Filters
- Date-range selection.
- Sensor-specific filtering.
- Dynamic dashboard updates based on selected filters.

## 🛠️ Technology Stack

| Technology | Application |
|---|---|
| Python | Backend programming |
| Streamlit | Interactive dashboard development |
| Pandas | Data processing and analysis |
| PyMySQL | Database connectivity |
| MySQL | Relational database |
| Amazon RDS | Cloud database hosting |
| AWS VPC / Security Groups | Network access configuration |
| GitHub | Version control and source code hosting |
| Streamlit Community Cloud | Application deployment |

## 🏗️ System Architecture

```text
       IoT Sensor Dataset
               |
               v
         MySQL Database
               |
               v
          AWS RDS Cloud
               |
               v
       PyMySQL Connector
               |
               v
        Python Application
               |
               v
         Pandas Processing
               |
               v
       Streamlit Dashboard
               |
               v
          End Users
```

### Workflow

1. **Data Storage:** IoT sensor readings are stored in a MySQL database.
2. **Cloud Integration:** The database is hosted on Amazon RDS.
3. **Database Connectivity:** PyMySQL connects the Python application to the cloud database.
4. **Data Processing:** Pandas performs data manipulation and statistical analysis.
5. **Visualization:** Streamlit displays the processed information through charts, metrics, and tables.
6. **Deployment:** The dashboard is hosted on Streamlit Community Cloud.

## 📂 Repository Structure

```text
IoT-Cloud-Analytics/
│
├── .streamlit/
│   └── secrets.toml
│
├── dashboard/
│   └── app.py
│
├── screenshots/
│   └── Dashboard screenshots
│
├── scripts/
│   └── Database and utility scripts
│
├── .gitignore
│
├── requirements.txt
│
└── README.md
```

*Note: The folder descriptions are indicative; refer to the actual files within each folder.*

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.10+
- MySQL
- AWS account
- Git

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

```bash
cd IoT-Cloud-Analytics
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database Credentials

Create a `.env` file in the project root:

```env
DB_HOST=your_aws_rds_endpoint
DB_PORT=3306
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_NAME=iot_analytics
```

For Streamlit Community Cloud, configure the corresponding credentials under the application's Secrets settings.

**Never upload database passwords or other sensitive credentials to GitHub.**

### 5. Run the Application

```bash
streamlit run dashboard/app.py
```

The dashboard will be accessible at:

`http://localhost:8501`

## ☁️ AWS Cloud Infrastructure

The project uses Amazon Relational Database Service (Amazon RDS) with MySQL.

| Configuration | Value |
|---|---|
| Cloud Provider | AWS |
| Database Engine | MySQL Community |
| Database Identifier | iot-analytics-db |
| Database Schema | iot_analytics |
| Main Table | sensor_readings |
| Port | 3306 |
| AWS Region | Asia Pacific (Mumbai) |

AWS security groups are configured to manage inbound database connectivity.

## 🚀 Live Deployment

The application is deployed using Streamlit Community Cloud.

**Live Dashboard:**  
https://iot-cloud-analytics.streamlit.app/

## 📸 Dashboard Preview

The `screenshots/` directory contains screenshots demonstrating the application's interface and analytics visualizations.

## 🔐 Security

- Database credentials are managed through Streamlit Secrets and environment variables.
- Sensitive files are excluded from version control.
- AWS security groups regulate database access.
- Database credentials are not hardcoded into application source code.

## 🔮 Future Scope

- Real-time sensor data streaming.
- Automated anomaly detection.
- Machine learning-based environmental predictions.
- Automated threshold alerts.
- Advanced time-series analysis.
- Downloadable analytical reports.
- Integration with MQTT-based IoT communication.

## 👩‍💻 Contributors

**Developed by:**

1. **Soumi Sarkar**
2. **Aheli Sau**
3. **Madhurima Sasmal**

## ⭐ Acknowledgements

This project explores the practical application of IoT data analytics, cloud database infrastructure, and interactive data visualization using modern development technologies.

---

**Project Domain:** Internet of Things | Cloud Computing | Database Management | Data Analytics

**Repository:** IoT-Cloud-Analytics
