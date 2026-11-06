# 🌍 ResQVision – AI-Based Disaster Damage Assessment and Recovery Planning System

## 📌 About the Project

ResQVision is a disaster management prototype designed to help emergency response teams assess damage, prioritize incidents, manage rescue teams, and plan resource allocation.

The system combines image processing, incident management, interactive mapping, and recovery planning into one centralized dashboard.

## 🎯 Problem Statement

During natural disasters, emergency response teams face challenges in assessing damage, identifying high-priority areas, coordinating rescue teams, and distributing limited resources efficiently.

ResQVision aims to simplify these activities through a centralized digital platform.

## ✨ Key Features

- **Disaster Image Analysis:** Uses OpenCV to compare before-and-after images and identify visual changes.
- **Incident Management:** Register and manage disaster incidents using an SQLite database.
- **Priority Assessment:** Assign priority levels to incidents using a scoring-based approach.
- **Interactive Disaster Map:** Visualize incident locations on an interactive map.
- **Recovery Planning:** Generate recovery recommendations and prioritize incidents.
- **PDF Recovery Reports:** Generate downloadable recovery reports.
- **Rescue Gap Detector:** Identify unassigned incidents, register rescue teams, suggest suitable teams, and track assignments.
- **What-If Resource Simulator:** Simulate resource distribution and manually adjust resource allocations.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| OpenCV | Image processing |
| Pandas | Data handling |
| NumPy | Numerical operations |
| Plotly | Data visualization |
| Folium | Interactive maps |
| SQLite | Database management |
| ReportLab | PDF report generation |

## 📂 Project Structure

```text
ResQVision/
│
├── app.py
├── database.py
├── image_analysis.py
├── map_module.py
├── priority.py
├── recovery.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/baddanadavid-ctrl/ResQVision.git
```

### 2. Open the Project Folder

```bash
cd ResQVision
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment (Windows PowerShell)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your web browser.

## 🎯 Project Objective

The main objective of ResQVision is to demonstrate how software technologies can support disaster response operations by improving incident visibility, rescue team coordination, and resource planning.

## 🔮 Future Enhancements

- Integration of advanced AI models for automated damage classification.
- Satellite and drone image analysis.
- Real-time disaster alerts.
- GPS-based rescue team tracking.
- More advanced resource optimization algorithms.
- Integration with external emergency response systems.

## 👨‍💻 Original Developers

- **Akshith**
- **David**
- **Neeraj**
- **Pranav**

## 📌 Project Status

Hackathon Prototype – Under Development.

---

**GitHub Repository:** [ResQVision](https://github.com/baddanadavid-ctrl/ResQVision)

## 🌐 Live Demo

Experience ResQVision here:

[🚀 Launch ResQVision Web App](https://resqvision-ksdz6fcerzj4rqk7nhs2hq.streamlit.app/)