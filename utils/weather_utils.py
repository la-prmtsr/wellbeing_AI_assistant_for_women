import requests


def get_user_location():

    try:

        response = requests.get("https://ipinfo.io/json")

        data = response.json()

        city = data.get("city")

        if not city:
            city = "Sakarya"

        return city

    except:

        return "Sakarya"


def get_weather():

    city = get_user_location()

    url = f"https://wttr.in/{city}?format=j1"

    try:

        response = requests.get(url)

        data = response.json()

        weather = data["current_condition"][0]["weatherDesc"][0]["value"]

        temp = data["current_condition"][0]["temp_C"]

        return {
            "city": city,
            "weather": weather,
            "temperature": temp
        }

    except Exception as e:

        return {
            "city": city,
            "weather": "Unknown",
            "temperature": "Unknown",
            "error": str(e)
        }