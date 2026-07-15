from ollama import chat

class LLMService:
    def explain(self, mission, score_json, aircraft):
        contexto = f"""
Missão:
Origem: {mission.origin_airport}
Destino: {mission.destination_airport}
Passageiros: {mission.passengers}
Carga: {mission.cargo_weight} kg

Aeronave escolhida:
Nome: {aircraft.name}
Alcance: {aircraft.range_km} km
Capacidade: {aircraft.max_passengers}
Payload: {aircraft.max_payload_kg} kg
Velocidade: {aircraft.cruise_speed} km/h
Score Final: {score_json["final_score"]:.2f}

Explique em até 5 linhas por que esta aeronave foi escolhida.
"""
        response = chat(
            model="llama3.1:8b",
            messages=[
                {"role": "system", "content": "Você é um especialista em planejamento aeronáutico."},
                {"role": "user", "content": contexto},
            ],
        )
        print(response["message"]["content"])
        return response["message"]["content"]