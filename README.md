# 🌸 Wellbeing AI Agent

An AI-powered wellbeing assistant designed for women. The application combines menstrual cycle tracking, daily wellbeing analysis, and personalized weekly planning to provide actionable health insights.

---

## Features

### Personalized Profile Setup
- Unique username-based profiles
- Automatic profile loading
- Editable menstrual cycle history
- Custom cycle length and period length settings

### Menstrual Cycle Tracking
- Current cycle day calculation
- Next period prediction
- Days remaining until next period
- Personalized cycle estimates

### Daily Wellbeing Analysis
- Mood tracking
- Stress assessment
- Sleep quality monitoring
- AI-generated recommendations

### Weekly Dashboard
- Average mood, stress, and sleep metrics
- Trend visualization
- Progress comparison with previous entries

### Weekly Goal Planner
- AI-generated 7-day wellbeing plans
- Personalized according to user goals
- Recent planner history
- One-click access to previous plans

### Weather Integration
- Current weather conditions
- Weather-aware recommendations and planning

---

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- JSON-based local data storage
- Requests

---

## Project Structure

```text
AIProject/
├── agent/
│   ├── action.py
│   ├── memory.py
│   ├── planner.py
│   └── reasoning.py
│
├── data/
│   ├── planner_history.json
│   ├── profiles.json
│   └── user_data.json
│
├── ui/
│   └── app.py
│
├── utils/
│   ├── analytics.py
│   ├── cycle_utils.py
│   ├── planner_history.py
│   ├── profile_utils.py
│   └── weather_utils.py
│
├── .env
├── .env.example
├── .gitignore
├── config.py
├── requirements.txt
└── README.md
```
---
## Installation Guide

### Prerequisites

Make sure the following are installed on your computer:

- Python 3.10 or newer
- Git (optional)
- Google Gemini API Key

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AIProject
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
#### Windows (Command Prompt)
```cmd
venv\Scripts\activate
```
#### Windows (PowerShell)
```cmd
venv\Scripts\Activate.ps1
```
#### macOS/Linux
```cmd
source venv/bin/activate
```
### 4. Install Required Packages

```bash
pip install -r requirements.txt
```


## Configure Gemini API Key

### open config.py and set your API key:

```bash
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```
You can create an API key at:
https://aistudio.google.com/app/apikey

## Run the Application
```bash
streamlit run ui/app.py
```
## Open in Browser
If the browser does not open automatically, go to:
```bash
http://localhost:8501
```
## Stop the Application
```bash
CTRL + C
```
## Virtual Environment Not Activated

Activate the venv folder before running the application.

## Kullanım Adımları

1. Profile Setup sekmesinde kullanıcı adı oluştur.
2. Son adet başlangıç tarihlerini gir.
3. Cycle Length ve Period Length bilgilerini kaydet.
4. Daily Analysis sekmesinden günlük verileri gir.
5. Yapay zekâ destekli önerileri görüntüle.
6. Weekly Planner ile haftalık hedef planı oluştur.
7. Dashboard üzerinden geçmiş verileri incele