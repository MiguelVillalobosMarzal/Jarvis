"""
Diagnóstico: muestra en tiempo real el volumen que capta tu micrófono.
Sirve para saber qué UMBRAL_SILENCIO tiene sentido en tu caso.

Ejecuta esto, quédate en silencio 2 segundos, luego habla normal,
y mira los números que salen.
"""

import numpy as np
import sounddevice as sd

SAMPLE_RATE = 16000
BLOQUE_SEGUNDOS = 0.5


def volumen(bloque_audio):
    return np.sqrt(np.mean(bloque_audio ** 2))


print("Mostrando volumen cada 0.5s. Ctrl+C para parar.")
print("Quédate callado un momento, luego habla normal.\n")

with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32") as stream:
    while True:
        bloque, _ = stream.read(int(SAMPLE_RATE * BLOQUE_SEGUNDOS))
        vol = volumen(bloque)
        barra = "#" * int(vol * 500)
        print(f"volumen={vol:.5f}  {barra}")
