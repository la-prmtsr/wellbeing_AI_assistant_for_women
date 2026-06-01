# agent/planner.py

import google.generativeai as genai
from config import GEMINI_API_KEY
from utils.weather_utils import get_weather

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def create_weekly_plan(goal):

    weather_data = get_weather()

    prompt = f"""
    Sen wellbeing planning agentisin.

    Kullanıcının hedefi:
    {goal}

    Şehir:
    {weather_data['city']}

    Güncel hava:
    {weather_data['weather']}

    Kullanıcı için 7 günlük wellbeing planı oluştur.

    Plan:
    - gerçekçi
    - uygulanabilir
    - motive edici
    - kısa
    - günlük hayat odaklı

    olsun.

    Eğer hava güzelse outdoor aktiviteler ekle.

    Format:

    Pazartesi:
    ...

    Salı:
    ...
    """

    response = model.generate_content(prompt)

    return response.text