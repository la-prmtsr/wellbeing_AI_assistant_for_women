# 🌸 Wellbeing AI Assistant for Women

An AI-powered wellbeing assistant designed to support women's daily health and wellness through menstrual cycle tracking, mood analysis, personalized recommendations, and intelligent weekly planning.

The system combines user wellbeing data, menstrual cycle information, weather conditions, and generative AI to provide personalized insights and actionable recommendations.

---

## Project Goal

Many women experience fluctuations in mood, stress levels, energy, and wellbeing throughout their menstrual cycle. However, identifying patterns and receiving personalized guidance can be challenging.

This project aims to solve this problem through an AI Agent that:

* Tracks daily wellbeing metrics
* Analyzes menstrual cycle information
* Detects trends and patterns
* Generates personalized recommendations
* Creates weekly wellbeing plans
* Adapts suggestions according to weather conditions

---

## AI Agent Architecture

The application follows an AI Agent architecture composed of four main components:

### 1. Perception Layer

Collects user information such as:

* Mood level
* Stress level
* Sleep duration
* Menstrual cycle data
* User goals

### 2. Memory Layer

Stores and retrieves historical user information using JSON-based local storage.

### 3. Reasoning Layer

Analyzes user data and identifies:

* Emotional trends
* Cycle-related patterns
* Stress indicators
* Sleep-related wellbeing issues

### 4. Action Layer

Produces:

* Personalized recommendations
* Wellbeing insights
* Weekly action plans
* Context-aware suggestions

---

## Features

### Personalized Profile Management

* Username-based profiles
* Automatic profile loading
* Menstrual cycle configuration
* Editable profile settings

### Menstrual Cycle Tracking

* Current cycle day calculation
* Next period prediction
* Days until next cycle
* Personalized cycle estimation

### Daily Wellbeing Analysis

* Mood tracking
* Stress assessment
* Sleep monitoring
* AI-generated recommendations

### Weekly Dashboard

* Mood trends
* Stress trends
* Sleep statistics
* Historical wellbeing analysis

### AI Weekly Planner

* Personalized 7-day wellbeing plans
* Goal-oriented recommendations
* Planner history tracking
* Easy access to previous plans

### Weather-Aware Recommendations

* Current weather integration
* Context-sensitive suggestions
* Outdoor activity recommendations

---

## Technologies Used

| Technology        | Purpose                      |
| ----------------- | ---------------------------- |
| Python            | Core application             |
| Streamlit         | User Interface               |
| Google Gemini API | AI recommendation generation |
| JSON              | Local data storage           |
| Requests          | API communication            |

---

## Project Structure

```text
AIProject/
│
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
├── .env.example
├── .gitignore
├── config.py
├── requirements.txt
└── README.md
```

---

## Installation

### Prerequisites

* Python 3.10+
* Google Gemini API Key

### Clone the Repository

```bash
git clone <repository-url>
cd AIProject
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root directory:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

You can obtain a Gemini API key from Google AI Studio:

https://aistudio.google.com/app/apikey

---

## Running the Application

```bash
streamlit run ui/app.py
```

After launching, open:

```text
http://localhost:8501
```

---

## Usage

### Profile Setup

1. Create a profile.
2. Enter menstrual cycle information.
3. Configure cycle length and period length.

### Daily Analysis

1. Enter daily mood.
2. Enter stress level.
3. Enter sleep information.
4. Generate AI-powered recommendations.

### Weekly Planner

1. Define your wellbeing goals.
2. Generate a personalized weekly plan.
3. Review previous plans from planner history.

### Dashboard

Monitor trends and historical wellbeing data over time.

---

## Security Notes

* Never commit your `.env` file.
* Store API keys locally.
* Use `.env.example` for repository sharing.

---

## Academic Project

This project was developed as part of an AI-Supported Software Development course and demonstrates the application of AI Agent architecture for solving real-world wellbeing problems.
