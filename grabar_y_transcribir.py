"""
Fase 2 (v4): Grabar tu voz y parar cuando te callas, con autocalibración
y margen de silencio ajustado para permitir pausas naturales al hablar
(basado en pruebas reales de micrófono: las pausas entre palabras/frases
pueden durar 2-3 segundos sin que signifique que has terminado).
"""

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000

BLOQUE_SEGUNDOS = 0.5             # tamaño de cada "trocito" de audio
BLOQUES_SILENCIO_PARA_PARAR = 6   # 6 x 0.5s = 3s de silencio real para parar
MAX_SEGUNDOS = 30                 # límite de seguridad para que no grabe eternamente
MULTIPLICADOR_UMBRAL = 2.5
UMBRAL_MINIMO = 0.003             # volumen por debajo del cual consideramos "silencio"

print("Cargando modelo de transcripción...")
modelo = WhisperModel("small", device="cpu", compute_type="int8")
print("Modelo listo.\n")


def volumen(bloque_audio):
    return np.sqrt(np.mean(bloque_audio ** 2))


def calibrar(stream):
    print("Calibrando... quédate en silencio un segundo.")
    niveles = []
    for _ in range(int(1 / BLOQUE_SEGUNDOS)):
        bloque, _ = stream.read(int(SAMPLE_RATE * BLOQUE_SEGUNDOS))
        niveles.append(volumen(bloque))
    ruido_fondo = float(np.mean(niveles))
    umbral = max(ruido_fondo * MULTIPLICADOR_UMBRAL, UMBRAL_MINIMO)
    print(f"Ruido de fondo: {ruido_fondo:.5f} -> umbral de silencio: {umbral:.5f}\n")
    return umbral


def escuchar():
    input("Pulsa Enter y prepárate (calibrando, no hables aún)...")

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32") as stream:
        umbral = calibrar(stream)

        print("🎙️  Habla ya. Paro tras ~3s de silencio real...")
        bloques_grabados = []
        bloques_en_silencio = 0
        bloques_totales = 0
        max_bloques = int(MAX_SEGUNDOS / BLOQUE_SEGUNDOS)

        while bloques_totales < max_bloques:
            bloque, _ = stream.read(int(SAMPLE_RATE * BLOQUE_SEGUNDOS))
            bloques_grabados.append(bloque)
            bloques_totales += 1

            vol = volumen(bloque)

            if vol < umbral:
                bloques_en_silencio += 1
            else:
                bloques_en_silencio = 0

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