from ollama import chat

class LLMService:
    def explain(self, mission, aircraft_score_json):
        prompt = f"""
            Você é um especialista em planejamento aeronáutico.

            Missão:

            Origem: {mission.origin_airport}

            Destino: {mission.destination_airport}

            Passageiros: {mission.passengers}

            Carga: {mission.cargo_weight} kg

            Aeronave escolhida:

            Nome: {aircraft_score_json.name}

            Alcance: {aircraft_score_json.range_km} km

            Capacidade: {aircraft_score_json.max_passengers}

            Payload: {aircraft_score_json.max_payload_kg} kg

            Velocidade: {aircraft_score_json.cruise_speed} km/h

            Score Final: {aircraft_score_json.final_score:.2f}

            Explique em até 5 linhas por que esta aeronave foi escolhida.
            """
        response = chat(model="qwen3:8b", messages= [{"rolse": "System", "content" : prompt}])

        return response["message"]["content"]