# agent/reasoning.py

import google.generativeai as genai
from config import GEMINI_API_KEY
from utils.weather_utils import get_weather

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze(input_data, history):

    weather_data = get_weather()
    history_context = ""

    # Son 5 kaydı metne dönüştür
    for entry in history[-5:]:
        history_context += f"""
        Tarih: {entry.get('date')}
        Mood: {entry.get('mood')}
        Stress: {entry.get('stress')}
        Sleep: {entry.get('sleep')}
        Cycle Day: {entry.get('cycle_day')}
        Note: {entry.get('note')}
        """

    # -------------------------
    # Pattern Detection
    # -------------------------
    pattern_insights = []

    recent_entries = history[-5:]

    if len(recent_entries) >= 3:
        low_sleep_count = 0
        high_stress_count = 0
        low_mood_count = 0

        for entry in recent_entries:
            if entry.get("sleep", 0) < 6:
                low_sleep_count += 1

            if entry.get("stress", 0) >= 7:
                high_stress_count += 1

            if entry.get("mood", 10) <= 4:
                low_mood_count += 1

        if low_sleep_count >= 2 and high_stress_count >= 2:
            pattern_insights.append(
                "Son girişlerde düşük uyku süresi ile yüksek stres arasında bir ilişki gözlemleniyor."
            )

        if low_mood_count >= 3:
            pattern_insights.append(
                "Son günlerde ruh halinin genel olarak düşük seyrettiği görülüyor."
            )

        if high_stress_count >= 3:
            pattern_insights.append(
                "Stres seviyen son girişlerde sürekli yüksek görünüyor."
            )

    if not pattern_insights:
        pattern_insights.append(
            "Belirgin bir davranış paterni tespit edilmedi."
        )

    # -------------------------
    # Prompt
    # -------------------------
    prompt = f"""
    Sen kadınlar için geliştirilmiş akıllı bir wellbeing analiz ajanısın.

    Kullanıcının:
    - ruh hali
    - stres seviyesi
    - uyku düzeni
    - regl döngüsü
    - geçmiş davranışları
    - bulunduğu şehirdeki hava durumu

    birlikte analiz edilmelidir.

    Şu anki kullanıcı verisi:
    {input_data}

    Kullanıcının bulunduğu şehir:
    {weather_data['city']}

    Güncel hava durumu:
    - Hava: {weather_data['weather']}
    - Sıcaklık: {weather_data['temperature']}°C

    Son kullanıcı geçmişi:
    {history_context}

    Tespit edilen davranış paternleri:
    {chr(10).join(pattern_insights)}

    Weather bilgisi GERÇEK ve güncel veridir.
    Hava durumunu doğrudan analizine dahil et.

    Kullanıcının mevcut psikolojik durumunu değerlendir.
    Geçmiş verilerde trend veya pattern varsa belirt.

    Eğer hava:
    - güneşli/açıksa → outdoor aktiviteleri destekle
    - yağmurlu/kapalıysa → indoor aktiviteler öner

    Analizin:
    - kısa
    - net
    - akıllı
    - doğal
    - bağlamsal

    olsun.

    Asla:
    - "hava nasıl bilmiyorum"
    - "eğer hava güzelse"

    gibi varsayımsal cümleler kurma.
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Analiz sırasında hata oluştu: {str(e)}"