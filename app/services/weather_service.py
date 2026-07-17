import requests
import time
class Weather:
    def mission_weather_score(self,origin_lat, origin_lon, destination_lat, destination_lon):
        climact_coords = 10
        score_points_mission = 0
        avg_wind = 0
        avg_visibility = 0
        avg_precipitation = 0
        avg_temperature = 0
        for i in range(climact_coords + 1):
            lat = origin_lat +(destination_lat - origin_lat) * i / climact_coords
            lon = origin_lon + (destination_lon - origin_lon) * i / climact_coords
            score_point = self.weather_score_point(lat,lon)
            score_points_mission += score_point["weather_score"]
            avg_wind+= score_point["score_wind"]
            avg_visibility+= score_point["score_visibility"]
            avg_precipitation += score_point["score_precipitation"]
            avg_temperature += score_point["score_temperature"]

        return {"weather_score": score_points_mission/11,
                "avg_wind":avg_wind/11,
                "avg_visibility":avg_visibility/11,
                "avg_precipitation":avg_precipitation/11,
                "avg_temperature": avg_temperature/11
                }


    def weather_score_point(self,lat, lon):
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
        try:
            response_openmeteo = requests.get(url, timeout= 10)
            data = response_openmeteo.json()
            print(f"\n\n{data}\n\n")
            current = data["current"]
        except Exception as e:
            print(f"Exception {e} ocurred")
            return {
                "score_wmo":50,
                "score_wind":50,
                "score_visibility":50,
                "score_precipitation":50,
                "score_temperature":50,
                "weather_score":50
            }

        score_wmo_i = self.score_wmo(current["weather_code"]) 
        score_wind_i = self.score_wind(current["wind_speed_10m"])
        score_visibility_i = self.score_visibility(current["visibility"]) 
        score_precipitation_i =self.score_precipitation(current["precipitation"])
        score_temperature_i = self.score_temperature(current["temperature_2m"])

        weather_score =(
            score_wmo_i* 0.40 +
            score_wind_i * 0.25 +
            score_visibility_i* 0.20 +
            score_precipitation_i * 0.10 +
            score_temperature_i * 0.05
        )
        score_json = {
            "score_wmo": score_wmo_i,
            "score_wind": current["wind_speed_10m"],
            "score_visibility": current["visibility"],
            "score_precipitation": current["precipitation"],
            "score_temperature": current["temperature_2m"],
            "weather_score": weather_score
        }
        return score_json

    def score_wmo(self, code):
        if code == 0:
            return 100
        elif code == 1:
            return 95
        elif code == 2:
            return 90
        elif code == 3:
            return 85
        elif code in [45, 48]:
            return 60
        elif code in [51, 53, 55]:
            return 75
        elif code in [56, 57]:
            return 55
        elif code == 61:
            return 70
        elif code == 63:
            return 50
        elif code == 65:
            return 35
        elif code == 66:
            return 25
        elif code == 67:
            return 10
        elif code == 71:
            return 55
        elif code == 73:
            return 40
        elif code == 75:
            return 20
        elif code == 77:
            return 35
        elif code == 80:
            return 60
        elif code == 81:
            return 40
        elif code == 82:
            return 15
        elif code == 85:
            return 30
        elif code == 86:
            return 15
        elif code == 95:
            return 10
        elif code == 96:
            return 5
        elif code == 99:
            return 0
        return 50
        
    def score_wind(self, v_wind):
        if v_wind <= 20:
            return 100
        elif v_wind >= 60:
            return 0
        else:
            return round((60 - v_wind) / 40 * 100, 2)
        
    def score_precipitation(self, volume):
        if volume == 0:
            return 100
        elif volume >= 10:
            return 0
        else:
            return round((10 - volume) / 10 * 100, 2)
        
    def score_visibility(self, meters):
        if meters >= 10000:
            return 100
        elif meters < 2000:
            return 0
        else:
            return round((meters- 2000 )/8000 *100, 2)
        
    def score_temperature(self, temp):
        ideal = 17.5
        if temp <= -40 or temp >= 45:
            return 0
        elif temp < ideal:
            return round((temp + 40) / (ideal + 40) * 100, 2)
        else:
            return round((45 - temp) / (45 - ideal) * 100, 2)

