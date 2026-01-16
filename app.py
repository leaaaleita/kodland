from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

# Cliente de IA (Groq)
client = Groq(api_key="Groq_API_Key")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/preguntar", methods=["POST"])
def preguntar():
    data = request.get_json()
    pregunta = data.get("pregunta", "").lower()

    # =========================
    # RESPUESTAS PREDEFINIDAS
    # =========================
    if "prevencion" in pregunta or "prevenir" in pregunta:
        return jsonify({
            "respuesta": "La prevención del cambio climático implica reducir las emisiones de gases de efecto invernadero, usar energías renovables y promover hábitos sostenibles."
        })

    elif "consecuencias" in pregunta or "impactos" in pregunta:
        return jsonify({
            "respuesta": "Las consecuencias del cambio climático incluyen el aumento del nivel del mar, fenómenos climáticos extremos, pérdida de biodiversidad y riesgos para la salud humana."
        })

    elif "causas" in pregunta:
        return jsonify({
            "respuesta": "Las principales causas del cambio climático son la quema de combustibles fósiles, la deforestación y las actividades industriales."
        })

    elif "soluciones" in pregunta:
        return jsonify({
            "respuesta": "Las soluciones incluyen el uso de energías limpias, la reforestación, la eficiencia energética y cambios en el estilo de vida."
        })

    elif "definicion" in pregunta or "qué es" in pregunta or "que es" in pregunta:
        return jsonify({
            "respuesta": "El cambio climático es la alteración a largo plazo del clima del planeta, causada principalmente por la actividad humana."
        })
    elif "pais" in pregunta and "contamin" in pregunta:
        return jsonify({
        "respuesta": "Actualmente, los países que más contaminan son China, Estados Unidos e India, principalmente debido a su alta industrialización y población."
    })


    # =========================
    # SI NO COINCIDE → IA
    # =========================
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente que SOLO responde preguntas sobre cambio climático de forma clara, breve y educativa."
                },
                {
                    "role": "user",
                    "content": pregunta
                }
            ],
            temperature=0.5
        )

        return jsonify({
            "respuesta": response.choices[0].message.content
        })

    except Exception as e:
        print("ERROR IA:", e)
        return jsonify({
            "respuesta": "Lo siento, no puedo responder a esa pregunta en este momento."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
