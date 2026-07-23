"""
Fase 2: Grabar tu voz por micrófono y transcribirla a texto con Whisper local.
"""

import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
DURACION_SEGUNDOS = 5  # cuánto tiempo graba cada vez que hablas

print("Cargando modelo de transcripción (la primera vez tarda un poco, descarga el modelo)...")
modelo = WhisperModel("small", device="cpu", compute_type="int8")
print("Modelo listo.\n")


def escuchar():
    input("Pulsa Enter y habla (tienes 5 segundos)...")
    print("🎙️  Grabando...")
    audio = sd.rec(
        int(DURACION_SEGUNDOS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    print("Transcribiendo...")

    segmentos, _ = modelo.transcribe(audio.flatten(), language="es")
    texto = " ".join(seg.text for seg in segmentos).strip()

    if texto:
        print(f"Tú (voz): {texto}\n")
    return texto


if __name__ == "__main__":
    # Prueba suelta: solo graba y transcribe, sin hablar con el LLM todavía
    resultado = escuchar()
    print("Transcripción final:", resultado)
