import requests
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def fetch_covid_data(date):
    """
    Récupère les données COVID pour une date spécifique.
    """
    url = "https://covid-api.com/api/reports"
    response = requests.get(url, params={"date": date})

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"⚠ Erreur {response.status_code} pour la date {date}")
        return []

def extract_data():
    start_date = datetime(2020, 2, 1)
    end_date = datetime(2023, 3, 1)

    current_date = start_date
    all_data = []

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        data = fetch_covid_data(date_str)

        for entry in data:
            all_data.append({
                "date": entry.get("date", date_str),
                "name": entry.get("region", {}).get("name", "N/A"),
                "iso": entry.get("region", {}).get("iso", "N/A"),
                "lat": entry.get("region", {}).get("lat", "N/A"),
                "long": entry.get("region", {}).get("long", "N/A"),
                "confirmed": entry.get("confirmed", 0),
                "deaths": entry.get("deaths", 0),
                "recovered": entry.get("recovered", 0),
                "active": entry.get("active", 0),
                "fatality_rate": entry.get("fatality_rate", 0.0),
                "last_update": entry.get("last_update", "N/A")
            })

        print(f"Données récupérées pour {date_str}")
        current_date += relativedelta(months=1)

    df = pd.DataFrame(all_data)
    df.to_csv("covid_data.csv", index=False, encoding="utf-8")
    print(df)

extract_data()