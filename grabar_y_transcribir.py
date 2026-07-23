"""
Fase 2 (mejorada): Grabar tu voz y parar automáticamente cuando te callas,
en vez de usar un tiempo fijo.

Concepto (VAD casero, "Voice Activity Detection"):
1. Grabamos en trocitos pequeños (bloques de 0.5s) sin parar.
2. Medimos el "volumen" de cada trocito (su energía media).
3. Si llevamos varios trocitos seguidos en silencio -> paramos.
4. Si sigues hablando, seguimos grabando (hasta un máximo por seguridad).
"""

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
BLOQUE_SEGUNDOS = 0.5          # tamaño de cada "trocito" de audio
UMBRAL_SILENCIO = 0.01        # volumen por debajo del cual consideramos "silencio"
BLOQUES_SILENCIO_PARA_PARAR = 4  # 5 bloques de 0.5s = 2.0s de silencio -> paras
MAX_SEGUNDOS = 45             # límite de seguridad para que no grabe eternamente

print("Cargando modelo de transcripción...")
modelo = WhisperModel("small", device="cpu", compute_type="int8")
print("Modelo listo.\n")


def volumen(bloque_audio):
    """Calcula el volumen medio de un trocito de audio (RMS)."""
    return np.sqrt(np.mean(bloque_audio ** 2))


def escuchar():
    input("Pulsa Enter y empieza a hablar (para solo cuando te calles)...")
    print("🎙️  Escuchando...")

    bloques_grabados = []
    bloques_en_silencio = 0
    bloques_totales = 0
    max_bloques = int(MAX_SEGUNDOS / BLOQUE_SEGUNDOS)

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32") as stream:
        while bloques_totales < max_bloques:
            bloque, _ = stream.read(int(SAMPLE_RATE * BLOQUE_SEGUNDOS))
            bloques_grabados.append(bloque)
            bloques_totales += 1

            vol = volumen(bloque)

            if vol < UMBRAL_SILENCIO:
                bloques_en_silencio += 1
            else:
                bloques_en_silencio = 0  # has vuelto a hablar, reiniciamos el contador

            # Si llevamos ya varios bloques de silencio seguidos, paramos
            if bloques_en_silencio >= BLOQUES_SILENCIO_PARA_PARAR:
                break

    print("Transcribiendo...")
    audio_completo = np.concatenate(bloques_grabados).flatten()

    segmentos, _ = modelo.transcribe(audio_completo, language="es")
    texto = " ".join(seg.text for seg in segmentos).strip()

    if texto:
        print(f"Tú (voz): {texto}\n")
    return texto


if __name__ == "__main__":
    resultado = escuchar()
    print("Transcripción final:", resultado)