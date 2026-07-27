import requests
from grabar_y_transcribir import escuchar
from tts import hablar

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"

SYSTEM_PROMPT = (
    "Eres Jarvis, un asistente personal inteligente, cercano y con un "
    "toque de humor seco. Respondes de forma breve y directa, como un "
    "buen ayudante que conoce bien a su usuario."
)


def chat_voz():
    print("Jarvis (fase voz) listo. Di 'salir' para terminar.\n")

    historial = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        mensaje = escuchar()

        if not mensaje:
            print("No te he oído bien, prueba otra vez.\n")
            continue

        if mensaje.lower().strip(".,!¡¿? ") in ("salir","salid", "exit", "quit"):
            print("Jarvis: Hasta luego.")
            hablar("Hasta luego.")
            break

        historial.append({"role": "user", "content": mensaje})

        try:
            respuesta = requests.post(
                OLLAMA_URL,
                json={"model": MODEL, "messages": historial, "stream": False},
                timeout=60,
            )
            respuesta.raise_for_status()
            texto = respuesta.json()["message"]["content"]
        except requests.exceptions.ConnectionError:
            print(
                "\n[Error] No puedo conectar con Ollama. "
                "Asegúrate de que está abierto y corriendo.\n"
            )
            continue
        except Exception as e:
            print(f"\n[Error inesperado] {e}\n")
            continue

        print(f"Jarvis: {texto}\n")
        hablar(texto)
        historial.append({"role": "assistant", "content": texto})


if __name__ == "__main__":
    chat_voz()
