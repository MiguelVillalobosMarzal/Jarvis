"""
Fase 2 (v5): Grabar tu voz y parar cuando te callas.
 
Cambio respecto a v4: ya NO se recalibra en cada turno de conversación
(eso obligaba a esperar un segundo en silencio antes de cada frase).
En su lugar, usamos un umbral FIJO, calculado a partir de mediciones
reales hechas con herramientas/diagnostico_microfono.py.
 
Si en el futuro cambias de micrófono o de sala y esto deja de
funcionar bien, vuelve a ejecutar diagnostico_microfono.py y ajusta
UMBRAL_SILENCIO aquí abajo con los nuevos valores.
"""

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
BLOQUE_SEGUNDOS = 0.5             # tamaño de cada "trocito" de audio
BLOQUES_SILENCIO_PARA_PARAR = 6   # 6 x 0.5s = 3s de silencio real para parar
MAX_SEGUNDOS = 30                 # límite de seguridad para que no grabe eternamente
UMBRAL_SILENCIO = 0.003             # volumen por debajo del cual consideramos "silencio"

print("Cargando modelo de transcripción...")
modelo = WhisperModel("small", device="cpu", compute_type="int8")
print("Modelo listo.\n")
 
 
def volumen(bloque_audio):
    return np.sqrt(np.mean(bloque_audio ** 2))
 
 
def escuchar():
    input("Pulsa Enter y habla (paro tras ~3s de silencio real)...")
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