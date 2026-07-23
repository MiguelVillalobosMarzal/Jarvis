"""
Fase 1: Chat de texto con Jarvis (cerebro local via Ollama).

Requiere que Ollama esté instalado y corriendo, y que hayas hecho:
    ollama pull llama3.2
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"

SYSTEM_PROMPT = (
    "Eres Jarvis, un asistente personal inteligente, cercano y con un "
    "toque de humor seco. Respondes de forma breve y directa, como un "
    "buen ayudante que conoce bien a su usuario."
)


def chat():
    print("Jarvis (fase texto) listo. Escribe 'salir' para terminar.\n")

    historial = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        mensaje = input("Tú: ").strip()
        if mensaje.lower() in ("salir", "exit", "quit"):
            print("Jarvis: Hasta luego.")
            break
        if not mensaje:
            continue

        historial.append({"role": "user", "content": mensaje})

        try:
            respuesta = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "messages": historial,
                    "stream": False,
                },
                timeout=60,
            )
            respuesta.raise_for_status()
            data = respuesta.json()
            texto = data["message"]["content"]
        except requests.exceptions.ConnectionError:
            print(
                "\n[Error] No puedo conectar con Ollama. "
                "¿Está instalado y corriendo? Prueba a abrir Ollama "
                "o ejecutar 'ollama serve' en otra terminal.\n"
            )
            continue
        except Exception as e:
            print(f"\n[Error inesperado] {e}\n")
            continue

        print(f"Jarvis: {texto}\n")
        historial.append({"role": "assistant", "content": texto})


if __name__ == "__main__":
    chat()
