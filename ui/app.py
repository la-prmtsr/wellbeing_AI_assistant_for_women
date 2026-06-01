import streamlit as st
import sys
import os


# Ensure the root directory is in the path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.memory import create_entry, save_data, load_data
from agent.reasoning import analyze
from agent.action import generate 
from agent.planner import create_weekly_plan

from utils.analytics import (
    get_last_n_entries,
    calculate_summary,
    compare_with_previous
)

from utils.cycle_utils import get_cycle_info
from utils.profile_utils import (
    save_user_profile,
    load_user_profile
)
from utils.planner_history import (
    save_plan,
    get_recent_plans
)

from datetime import datetime

def format_display_date(date_str):
    """
    '2026-05-12' -> '12 May 2026'
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d %B %Y")
    except:
        return date_str
    
# ==========================================
# PAGE CONFIG & PREMIUM CUSTOM CSS
# ==========================================
st.set_page_config(page_title="Wellbeing AI Agent", page_icon="🌸", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* =====================================================
   GLOBAL THEME
===================================================== */
html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top right, rgba(236, 72, 153, 0.06), transparent 35%),
        radial-gradient(circle at top left, rgba(139, 92, 246, 0.06), transparent 35%),
        linear-gradient(180deg, #F8FAFC 0%, #EEF2FF 100%);
    color: #0F172A;
}

/* Main content spacing */
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 900px;
}

/* =====================================================
   HEADINGS
===================================================== */
h1 {
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.04em !important;
    line-height: 1.1 !important;
    background: linear-gradient(135deg, #7C3AED 0%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem !important;
}

h2, h3 {
    font-weight: 700 !important;
    color: #0F172A !important;
    letter-spacing: -0.02em;
}

h4, h5, h6 {
    font-weight: 600 !important;
    color: #1E293B !important;
}

/* Subtitle */
.subtitle {
    color: #64748B;
    font-size: 1.05rem;
    margin-top: -10px;
    margin-bottom: 24px;
}

/* =====================================================
   TABS
===================================================== */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: rgba(255, 255, 255, 0.72);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255, 255, 255, 0.85);
    border-radius: 18px;
    padding: 8px;
    box-shadow:
        0 10px 30px rgba(15, 23, 42, 0.06),
        inset 0 1px 0 rgba(255,255,255,0.8);
}

button[data-baseweb="tab"] {
    border-radius: 12px !important;
    padding: 12px 18px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: #64748B !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.25s ease;
}

button[data-baseweb="tab"]:hover {
    background: rgba(99, 102, 241, 0.06) !important;
    color: #4338CA !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    color: white !important;
    box-shadow: 0 8px 20px rgba(139, 92, 246, 0.25);
}

/* =====================================================
   CARDS
===================================================== */
.ai-box,
.cycle-card,
.stAlert,
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.78) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.9) !important;
    border-radius: 24px !important;
    box-shadow:
        0 10px 30px rgba(15, 23, 42, 0.06),
        0 1px 2px rgba(15, 23, 42, 0.05);
    padding: 24px !important;
    transition: all 0.3s ease;
}

.ai-box:hover,
.cycle-card:hover,
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow:
        0 18px 40px rgba(15, 23, 42, 0.08),
        0 2px 6px rgba(15, 23, 42, 0.05);
}

/* =====================================================
   METRICS
===================================================== */
[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #0F172A !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em;
}

/* =====================================================
   INPUTS
===================================================== */
.stTextInput > div > div > input,
.stTextArea textarea,
.stDateInput input,
.stNumberInput input {
    background: rgba(255, 255, 255, 0.92) !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 14px !important;
    color: #0F172A !important;
    padding: 12px 14px !important;
    transition: all 0.25s ease;
}

.stTextInput > div > div > input:focus,
.stTextArea textarea:focus,
.stDateInput input:focus,
.stNumberInput input:focus {
    border-color: #8B5CF6 !important;
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.12) !important;
}

/* Labels */
div[data-testid="stWidgetLabel"] p {
    color: #334155 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* =====================================================
   BUTTONS
===================================================== */
div.stButton > button {
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 1.6rem !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em;
    box-shadow: 0 10px 24px rgba(139, 92, 246, 0.25);
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 32px rgba(139, 92, 246, 0.30);
}

/* =====================================================
   RADIO BUTTONS
===================================================== */
div[role="radiogroup"] > label {
    background: rgba(255, 255, 255, 0.75);
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 8px 14px;
    margin-right: 8px;
    transition: all 0.2s ease;
}

div[role="radiogroup"] > label:hover {
    border-color: #C4B5FD;
    background: #F5F3FF;
}

/* =====================================================
   SLIDER
===================================================== */
.stSlider {
    padding-top: 6px;
}

# Mevcut CSS'teki tüm stAlert stillerini bununla değiştir.
# Bu tasarım, uygulamanın modern glassmorphism temasına tam uyum sağlar.

/* =====================================================
   MODERN ALERT DESIGN
===================================================== */

/* Dış wrapper tamamen şeffaf */
div[data-testid="stAlert"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 1rem 0 !important;
}

/* İç kart */
div[data-testid="stAlert"] > div {
    background: rgba(255, 255, 255, 0.78) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);

    border: 1px solid rgba(255, 255, 255, 0.9) !important;
    border-radius: 24px !important;

    box-shadow:
        0 10px 30px rgba(15, 23, 42, 0.06),
        0 1px 2px rgba(15, 23, 42, 0.05) !important;

    padding: 20px 24px !important;
}

/* İkon ve metni aynı hizada tut */
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
    margin: 0 !important;
}

div[data-testid="stAlert"] p {
    margin: 0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.97rem !important;
    font-weight: 600 !important;
    line-height: 1.6 !important;
    letter-spacing: -0.01em;
}

/* SVG ikon */
div[data-testid="stAlert"] svg {
    width: 1.15rem !important;
    height: 1.15rem !important;
    margin-top: 2px !important;
    opacity: 0.9;
}

/* SUCCESS */
div[data-testid="stAlert"][kind="success"] > div {
    background:
        linear-gradient(135deg,
            rgba(236, 253, 245, 0.95),
            rgba(240, 253, 250, 0.92)) !important;
    border: 1px solid rgba(16, 185, 129, 0.14) !important;
}

div[data-testid="stAlert"][kind="success"] p,
div[data-testid="stAlert"][kind="success"] svg {
    color: #059669 !important;
}

/* INFO */
div[data-testid="stAlert"][kind="info"] > div {
    background:
        linear-gradient(135deg,
            rgba(239, 246, 255, 0.95),
            rgba(245, 243, 255, 0.92)) !important;
    border: 1px solid rgba(99, 102, 241, 0.12) !important;
}

div[data-testid="stAlert"][kind="info"] p,
div[data-testid="stAlert"][kind="info"] svg {
    color: #4F46E5 !important;
}

/* WARNING */
div[data-testid="stAlert"][kind="warning"] > div {
    background:
        linear-gradient(135deg,
            rgba(255, 251, 235, 0.95),
            rgba(255, 247, 237, 0.92)) !important;
    border: 1px solid rgba(245, 158, 11, 0.12) !important;
}

div[data-testid="stAlert"][kind="warning"] p,
div[data-testid="stAlert"][kind="warning"] svg {
    color: #D97706 !important;
}

/* ERROR */
div[data-testid="stAlert"][kind="error"] > div {
    background:
        linear-gradient(135deg,
            rgba(254, 242, 242, 0.95),
            rgba(255, 241, 242, 0.92)) !important;
    border: 1px solid rgba(239, 68, 68, 0.12) !important;
}

div[data-testid="stAlert"][kind="error"] p,
div[data-testid="stAlert"][kind="error"] svg {
    color: #DC2626 !important;
}

/* =====================================================
   DIVIDERS
===================================================== */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(148, 163, 184, 0.4),
        transparent
    );
    margin: 2rem 0;
}

/* =====================================================
   CHARTS
===================================================== */
[data-testid="stPlotlyChart"],
[data-testid="stVegaLiteChart"],
[data-testid="stArrowVegaLiteChart"] {
    background: rgba(255, 255, 255, 0.78) !important;
    border-radius: 24px !important;
    padding: 8px !important;          /* 12px yerine daha küçük */
    border: 1px solid rgba(255,255,255,0.85) !important;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06) !important;
    overflow: hidden !important;      /* Grafiğin kart dışına taşmasını engeller */
}

[data-testid="stPlotlyChart"] > div,
[data-testid="stVegaLiteChart"] > div,
[data-testid="stArrowVegaLiteChart"] > div {
    padding: 0 !important;
    margin: 0 !important;
}

[data-testid="stPlotlyChart"] svg,
[data-testid="stVegaLiteChart"] svg,
[data-testid="stArrowVegaLiteChart"] svg,
[data-testid="stPlotlyChart"] canvas,
[data-testid="stVegaLiteChart"] canvas,
[data-testid="stArrowVegaLiteChart"] canvas {
    max-width: 100% !important;
    border-radius: 18px !important;
}

/* =====================================================
   SCROLLBAR
===================================================== */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: #CBD5E1;
    border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
    background: #94A3B8;
}
            
/* =====================================================
   STREAMLIT ALERT WRAPPER FIX
===================================================== */
div[data-testid="stAlert"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 1rem 0 !important;
}

div[data-testid="stAlert"] > div {
    background: rgba(255, 248, 220, 0.85) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(245, 158, 11, 0.18) !important;
    border-radius: 20px !important;
    box-shadow:
        0 10px 30px rgba(15, 23, 42, 0.06),
        0 1px 2px rgba(15, 23, 42, 0.04) !important;
    padding: 20px 24px !important;
}

div[data-testid="stAlert"][kind="warning"] > div {
    background: rgba(255, 251, 235, 0.92) !important;
    color: #92400E !important;
}

div[data-testid="stAlert"][kind="info"] > div {
    background: rgba(239, 246, 255, 0.92) !important;
    color: #1D4ED8 !important;
}

div[data-testid="stAlert"][kind="success"] > div {
    background: rgba(240, 253, 244, 0.92) !important;
    color: #166534 !important;
}

div[data-testid="stAlert"][kind="error"] > div {
    background: rgba(254, 242, 242, 0.92) !important;
    color: #991B1B !important;
}

div[data-testid="stAlert"] p {
    margin: 0 !important;
    font-weight: 500 !important;
    line-height: 1.6 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# MAIN HEADER
# =========================
st.title("🌸 Wellbeing AI Agent")
st.markdown(
    "<p style='color: #6B4E56; font-size: 1.1rem; margin-top: -15px;'>AI-powered wellbeing assistant designed for women</p>", 
    unsafe_allow_html=True
)

# ==================================================
# NAVIGATION TABS (Dashboard as Default)
# ==================================================
tab_profile, tab_dashboard, tab_daily, tab_planner = st.tabs([
    "Profile Setup",
    "Weekly Dashboard",
    "Daily Analysis",
    "Weekly Planner"
])

# ==========================================
# TAB 0: PROFILE SETUP
# ==========================================
with tab_profile:
    
    st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.82);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.9);
            border-radius: 24px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow:
                0 10px 30px rgba(255, 111, 157, 0.08),
                0 2px 6px rgba(15, 23, 42, 0.03);
        ">
            <h4 style="
                margin: 0 0 8px 0;
                color: #FF6F9D;
                font-size: 1.05rem;
                font-weight: 700;
            ">
                Create or Load Your Profile
            </h4>
            <p style="
                margin: 0;
                color: #6E4E59;
                line-height: 1.6;
                font-size: 0.95rem;
            ">
                Enter your username and cycle information to load an existing profile
                or create a personalized wellbeing profile.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Kullanıcı adı
    username = st.text_input(
        "Username",
        placeholder="Enter your username"
    ).strip().lower()

    # Kayıtlı profil kontrolü
    existing_profile = load_user_profile(username) if username else None

    # Varsayılan değerler
    if existing_profile:
        saved_cycle_info = existing_profile.get("cycle_info", {})
        default_cycle_length = saved_cycle_info.get("cycle_length", 28)
        default_period_length = saved_cycle_info.get("period_length", 5)
    else:
        default_cycle_length = 28
        default_period_length = 5


    # Giriş alanları
    cycle_length = st.number_input(
        "Average Cycle Length (days)",
        value=int(default_cycle_length),
        step=1,
        help="Average number of days from one period start to the next."
    )

    period_length = st.number_input(
        "Period Length (days)",
        value=int(default_period_length),
        step=1,
        help="Typical number of bleeding days."
    )

  
    # =====================================
    # KAYITLI PROFİL VARSA OTOMATİK YÜKLE
    # =====================================
    if existing_profile:
        st.success(f"Welcome back, {username}! Your saved profile has been loaded.")

        st.session_state["username"] = username
        st.session_state["period_dates"] = existing_profile["period_dates"]
        st.session_state["cycle_info"] = existing_profile["cycle_info"]

        cycle_info = existing_profile["cycle_info"]

        st.info(
            f"""
    Current Cycle Day: {cycle_info['current_cycle_day']}

    Average Cycle Length: {cycle_info['cycle_length']} days

    Predicted Next Period: {format_display_date(cycle_info['next_period_date'])}    """
        )

        # =====================================
        # PROFILE EDIT MODE
        # =====================================
        if "edit_profile_mode" not in st.session_state:
            st.session_state["edit_profile_mode"] = False

        # Edit butonu
        if st.button("Edit Profile"):
            st.session_state["edit_profile_mode"] = True

                # Edit modu açıksa formu göster
        if st.session_state["edit_profile_mode"]:

            from datetime import datetime, date

            today = date.today()

            # Kayıtlı tarihleri date objesine dönüştür
            default_dates = [
                datetime.strptime(d, "%Y-%m-%d").date()
                for d in existing_profile["period_dates"]
            ]

            # Gelecekteki tarihleri otomatik çıkar
            default_dates = [
                d for d in default_dates
                if d <= today
            ]

            # Eğer hiç geçerli tarih kalmazsa boş liste kullan
            if not default_dates:
                default_dates = []

            st.write("### Update Your Period Start Dates")

            updated_dates = st.date_input(
                "Select all previous period start dates",
                value=default_dates,
                max_value=today,
                help="You can add new dates or remove old ones."
            )

            # Tek tarih seçildiyse listeye çevir
            if isinstance(updated_dates, date):
                updated_dates = [updated_dates]
            else:
                updated_dates = list(updated_dates)

            # Güncelle butonu
            if st.button("Update Profile"):

                if len(updated_dates) >= 2:

                    date_strings = [
                        d.strftime("%Y-%m-%d")
                        for d in sorted(updated_dates)
                    ]

                    updated_cycle_info = get_cycle_info(
                        date_strings,
                        cycle_length=cycle_length,
                        period_length=period_length
                    )

                    save_user_profile(
                        username,
                        date_strings,
                        updated_cycle_info
                    )

                    st.session_state["period_dates"] = date_strings
                    st.session_state["cycle_info"] = updated_cycle_info
                    st.session_state["edit_profile_mode"] = False

                    st.success("Profile updated successfully.")
                    st.rerun()

                else:
                    st.warning("Please select at least 2 period start dates.")

            # İptal butonu
            if st.button("Cancel"):
                st.session_state["edit_profile_mode"] = False
                st.rerun()


    # =====================================
    # PROFİL YOKSA YENİ OLUŞTUR
    # =====================================
    else:

        from datetime import date

        period_dates = st.date_input(
            "Select Recent Period Start Dates",
            value=[],
            max_value=date.today(),   # Gelecekteki tarihler seçilemez
            help="Select the start dates of your previous periods."
        )

        if st.button("Save Profile"):

            if username and len(period_dates) >= 2:

                # Tarihleri string formatına dönüştür
                date_strings = [
                    d.strftime("%Y-%m-%d")
                    for d in sorted(period_dates)
                ]

                cycle_info = get_cycle_info(
                    date_strings,
                    cycle_length=cycle_length,
                    period_length=period_length
                )

                # JSON dosyasına kaydet
                save_user_profile(
                    username,
                    date_strings,
                    cycle_info
                )

                # Session state'e yükle
                st.session_state["username"] = username
                st.session_state["period_dates"] = date_strings
                st.session_state["cycle_info"] = cycle_info

                st.success(f"Profile for '{username}' has been saved successfully.")

                # Profil bilgilerini göster
                st.info(
                    f"""
    Current Cycle Day: {cycle_info['current_cycle_day']}

    Average Cycle Length: {cycle_info['cycle_length']} days

    Predicted Next Period: {cycle_info['next_period_date']}
    """
                )

            else:
                st.warning(
                    "Please enter a username and select at least 2 period start dates."
                )
# ==========================================
# TAB 1: WEEKLY DASHBOARD
# ==========================================
with tab_dashboard:
    st.write("")
    st.subheader("Weekly Overview")
    st.write("Track your health progress from the last 7 days.")

    if "cycle_info" not in st.session_state:
        st.markdown("""
            <div style="
                background-color: #FFE4E6;
                padding: 20px;
                border-radius: 15px;
                border: 1px solid #FF85A2;
            ">
                <p style="color: #4A2E35; margin: 0;">
                    <b>Note:</b> Please complete your profile setup first.
                </p>
            </div>
        """, unsafe_allow_html=True)

    else:
        cycle_info = st.session_state["cycle_info"]

        entries = get_last_n_entries(7)

        if entries:
            summary = calculate_summary(entries)
            comparison = compare_with_previous(entries)

            col1, col2, col3 = st.columns(3)

            col1.metric("Avg Mood", summary["avg_mood"], comparison["mood_change"])
            col2.metric("Avg Stress", summary["avg_stress"], comparison["stress_change"])
            col3.metric("Avg Sleep", summary["avg_sleep"], comparison["sleep_change"])

            st.write("")

            st.line_chart({
                "Mood": [e["mood"] for e in entries],
                "Stress": [e["stress"] for e in entries],
                "Sleep": [e["sleep"] for e in entries]
            })
        else:
            st.info("Not enough data to display the dashboard yet.")
# ==========================================
# TAB 2: DAILY ANALYSIS (Interactive Version)
# ==========================================
with tab_daily:
    st.write("")
    st.subheader("Daily Wellbeing Log")
    st.write("Record your data to receive personalized AI insights.")

    # 1. Check if profile exists (Logic from your teammate)
    if "cycle_info" not in st.session_state:
        st.markdown("""
            <div style="background-color: #FFE4E6; padding: 20px; border-radius: 15px; border: 1px solid #FF85A2;">
                <p style="color: #4A2E35; margin: 0;"><b>Note:</b> Please complete your profile setup first to track your cycle.</p>
            </div>
        """, unsafe_allow_html=True)
        st.stop()

    cycle_info = st.session_state["cycle_info"]

# 2. Display Cycle Info in a pretty premium card
    st.markdown(f"""
        <div class="cycle-card" style="margin-bottom: 25px;">
            <h4 style="margin-top:0; color: #FF85A2;">Current Cycle Status</h4>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="margin:5px 0; font-size: 1.2rem;"><b>Day {cycle_info['current_cycle_day']}</b></p>
                    <p style="margin:0; font-size: 0.8rem; color: #8C6A74;">Cycle Length: {cycle_info['cycle_length']} days</p>
                </div>
                <div style="text-align: right;">
                    <p style="margin:0; font-size: 0.8rem; color: #8C6A74;">Next Period</p>
                    <p style="margin:0; font-weight: bold; color: #FF85A2;">{format_display_date(cycle_info['next_period_date'])}</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3. INTERACTIVE INPUTS (Vertical Stack)
    
    # --- MOOD SECTION ---
    st.write("#### How is your mood today?")
    mood_map = {"😭": 2, "😟": 4, "😐": 6, "😊": 8, "🤩": 10}
    # Using radio with horizontal=True and a custom label
    selected_mood_emoji = st.radio(
        "Pick an emoji:",
        options=list(mood_map.keys()),
        index=2, # Default to Neutral
        horizontal=True,
        key="mood_radio"
    )
    mood_value = mood_map[selected_mood_emoji]

    # --- STRESS SECTION ---
    st.write("#### Stress Level")
    stress_labels = ["Chill 🍃", "Normal ☁️", "Busy 🐝", "Stressed 🔥", "Overwhelmed 🌋"]
    stress_map = {"Chill 🍃": 2, "Normal ☁️": 4, "Busy 🐝": 6, "Stressed 🔥": 8, "Overwhelmed 🌋": 10}
    
    selected_stress = st.select_slider(
        "How pressured do you feel?",
        options=list(stress_map.keys()),
        value="Normal ☁️"
    )
    stress_value = stress_map[selected_stress]

    # --- SLEEP SECTION ---
    st.write("#### Sleep Duration")
    sleep_options = {
        "Poor (<5h)": 4,
        "Fair (5-6h)": 6,
        "Good (7h)": 8,
        "Excellent (8h+)": 10
    }
    selected_sleep_label = st.radio(
        "How was your rest last night?",
        options=list(sleep_options.keys()),
        index=2, # Default to Good
        horizontal=True,
        key="sleep_radio"
    )
    sleep_value = sleep_options[selected_sleep_label]

    st.write("---")
    note = st.text_area("Additional Notes", placeholder="Anything else on your mind?")

    # 4. ACTION BUTTON
    if st.button("Run Analysis"):
        # Using the automatically calculated cycle_day from teammate's logic
        entry = create_entry(
            mood_value,
            stress_value,
            sleep_value,
            cycle_info["current_cycle_day"],
            note  
        )

        save_data(entry)
        history = load_data()

        with st.spinner("AI is analyzing your data..."):
            analysis = analyze(entry, history)
            suggestions = generate(analysis, entry)

        # Elegant Output Card
        st.markdown(f"""
            <div class="ai-box">
                <h3>AI Analysis & Recommendations</h3>
                <p style="color: #331B29; line-height: 1.6; white-space: pre-line;">{suggestions}</p>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 3: WEEKLY PLANNER
# ==========================================
with tab_planner:
    st.write("")
    st.subheader("Weekly Goal Planner")
    # st.write("Plan your health milestones with your AI Agent.")

    username = st.session_state.get("username", "anonymous")

        # Goal input
    goal = st.text_input(
            "What is your main goal for this week?",
            placeholder="e.g. Eat healthier, Sleep better, Lose weight"
        )

        # Generate plan
    if st.button("Generate Weekly Plan"):
            with st.spinner("Creating your personalized plan..."):
                weekly_plan = create_weekly_plan(goal)

            save_plan(username, goal, weekly_plan)
            st.session_state["latest_weekly_plan"] = weekly_plan

        # Show latest plan
    if "latest_weekly_plan" in st.session_state:
            st.markdown(f"""
                <div class="ai-box">
                    <h3>Your Weekly Plan</h3>
                    <p style="color: #331B29; line-height: 1.6; white-space: pre-line;">
                        {st.session_state["latest_weekly_plan"]}
                    </p>
                </div>
            """, unsafe_allow_html=True)

        # Recent planners
    st.write("")
    st.subheader("Recent Planners")

    recent_plans = get_recent_plans(username, limit=3)

    if recent_plans:
            cols = st.columns(3)

            for i, plan_data in enumerate(recent_plans):
                with cols[i]:
                    display_goal = plan_data["goal"].upper()
                    if st.button(
                        f"{display_goal}",
                        key=f"recent_plan_{i}",
                        use_container_width=True
                    ):
                        st.session_state["selected_recent_plan"] = plan_data

            if "selected_recent_plan" in st.session_state:
                selected = st.session_state["selected_recent_plan"]

                st.markdown(f"""
                    <div class="ai-box">
                        <h3>{selected['goal'].upper()}</h3>
                        <p style="
                            color: #8C6A74;
                            font-size: 0.9rem;
                            margin-bottom: 15px;
                        ">
                            Created: {format_display_date(selected['created_at'][:10])}
                        </p>
                        <p style="
                            color: #331B29;
                            line-height: 1.7;
                            white-space: pre-line;
                        ">
                            {selected['plan']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    else:
            st.info("No previous plans yet.")