import folium
from folium import Map
import os
from dotenv import load_dotenv
import requests
import streamlit as st

load_dotenv()
USER_SKYNET = os.getenv("USER_SKYNETWORK_API")
PASSWORD_SKYNET = os.getenv("PASSWORD_SKYWORK_API")

@st.cache_data(ttl=300)
def get_aircrafts(latmin, lonmin, latmax, lonmax):
    response = requests.get(
        f"https://opensky-network.org/api/states/all?lamin={latmin}&lomin={lonmin}&lamax={latmax}&lomax={lonmax}",
        auth=(USER_SKYNET, PASSWORD_SKYNET),
        timeout=10
    )
    return response.json()["states"]

def icon_selector(code):
    if code == 0:
        return {
            "icon": "sun",
            "color": "orange",
            "status": "Céu limpo"
        }

    elif code == 1:
        return {
            "icon": "cloud-sun",
            "color": "orange",
            "status": "Predominantemente limpo"
        }

    elif code == 2:
        return {
            "icon": "cloud-sun",
            "color": "lightgray",
            "status": "Parcialmente nublado"
        }

    elif code == 3:
        return {
            "icon": "cloud",
            "color": "gray",
            "status": "Nublado"
        }

    elif code in [45, 48]:
        return {
            "icon": "smog",
            "color": "gray",
            "status": "Névoa"
        }

    elif code in [51, 53, 55]:
        return {
            "icon": "cloud-rain",
            "color": "lightblue",
            "status": "Garoa"
        }

    elif code in [56, 57]:
        return {
            "icon": "cloud-rain",
            "color": "cadetblue",
            "status": "Garoa congelante"
        }

    elif code in [61, 63, 65]:
        return {
            "icon": "cloud-showers-heavy",
            "color": "blue",
            "status": "Chuva"
        }

    elif code in [66, 67]:
        return {
            "icon": "cloud-meatball",
            "color": "cadetblue",
            "status": "Chuva congelante"
        }

    elif code in [71, 73, 75, 77]:
        return {
            "icon": "snowflake",
            "color": "lightgray",
            "status": "Neve"
        }

    elif code in [80, 81, 82]:
        return {
            "icon": "cloud-showers-heavy",
            "color": "darkblue",
            "status": "Pancadas de chuva"
        }

    elif code in [85, 86]:
        return {
            "icon": "snowflake",
            "color": "blue",
            "status": "Pancadas de neve"
        }

    elif code in [95, 96, 99]:
        return {
            "icon": "bolt",
            "color": "red",
            "status": "Tempestade"
        }

    return {
        "icon": "question-circle",
        "color": "black",
        "status": "Condição desconhecida"
    }
def router_map( origin_lat, origin_lon, destination_lat, destination_lon, origin_name, destination_name):
    center_lat = (origin_lat + destination_lat)/2
    center_lon = (origin_lon + destination_lon)/2
    
    map = Map(location=[center_lat, center_lon], zoom_start= 5, tiles="cartodbpositron")
    folium.Marker(
            location=[destination_lat, destination_lon],
            popup= destination_name,
            tooltip="Destino",
            icon=folium.Icon(color="blue", icon="plane-arrival", prefix="fa")
    ).add_to(map)

    folium.Marker(
            location=[origin_lat, origin_lon],
            popup= origin_name,
            tooltip="Origem",
            icon=folium.Icon(color="red", icon="plane-departure", prefix= "fa")
    ).add_to(map)

    folium.PolyLine(
            locations=[[origin_lat,origin_lon],[destination_lat, destination_lon]],
            color = "#FF0000",
            weight = 3,
            opacity = 0.8,
            dash_array = "10, 5"
    ).add_to(map)
    margin = 0.5
    latmin = min(origin_lat, destination_lat) - margin
    latmax = max(origin_lat, destination_lat) + margin

    lonmin = min(origin_lon, destination_lon) - margin
    lonmax = max(origin_lon, destination_lon) + margin
    #OPENSKYNET
    try:
        aircrafts = get_aircrafts(
            latmin,
            lonmin,
            latmax,
            lonmax
        )
        for aircraft in aircrafts:
            lat, lon = aircraft[6], aircraft[5]

            if lat is None or lon is None:
                continue
            callsign = aircraft[1].strip() if aircraft[1] else "Desconhecido"
            altitude = aircraft[7] if aircraft[7] is not None else 0
            speed = aircraft[9] if aircraft[9] is not None else 0
            heading = aircraft[10] if aircraft[10] is not None else 0

            popup_html = f"""
            <b>{callsign}</b><br>
            País: {aircraft[2]}<br>
            Altitude: {altitude:.0f} m<br>
            Velocidade: {speed:.1f} m/s
            """

            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip="Aircraft",
                icon=folium.Icon(
                    color="green",
                    icon="plane",
                    prefix="fa",
                    angle=int(heading)
                )
            ).add_to(map)

    except Exception as e:
        print(f"Erro na requisição: {e}")

    #OPEN METEO
    try:
        climact_coords = 10
        for i in range(climact_coords + 1):

            lat = origin_lat +(destination_lat - origin_lat) * i / climact_coords
            lon = origin_lon + (destination_lon - origin_lon) * i / climact_coords
            url = (
                "https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}"
                f"&longitude={lon}"
                "&current=temperature_2m,"
                "precipitation,"
                "cloud_cover,"
                "wind_speed_10m,"
                "wind_direction_10m,"
                "visibility,"
                "weather_code"
            )
            response_openmeto = requests.get(url, timeout= 10)
            data = response_openmeto.json()
            current = data["current"]
            weather_data = icon_selector(current["weather_code"])
            popup=f"""
                <b>{weather_data["status"]}</b><br>
                Temperatura: {current["temperature_2m"]} °C<br>
                Nuvens: {current["cloud_cover"]}%<br>
                Vento: {current["wind_speed_10m"]} km/h<br>
                Visibilidade: {current["visibility"]} m<br>
                Precipitação: {current["precipitation"]} mm
                """
            folium.Marker(
                location=[lat, lon],
                tooltip= "Weather",
                popup= folium.Popup(popup, max_width=250),
                icon=folium.Icon(color=weather_data["color"], icon=weather_data["icon"], prefix="fa")
            ).add_to(map)
    except Exception as e:
        print(f"Erro na requisição: {e}")
    
    return map