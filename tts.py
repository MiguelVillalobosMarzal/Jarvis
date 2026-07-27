"""
Fase 3: Convertir texto a voz con Piper y reproducirlo.

Cómo funciona:
1. Le pasamos el texto a piper.exe por la "entrada estándar" (como si
   se lo escribiéramos a mano en la terminal).
2. Piper genera un archivo de audio (.wav) con esa voz.
3. Leemos ese archivo y lo reproducimos por los altavoces.

"""

import subprocess
import tempfile
import os

import soundfile as sf
import sounddevice as sd

PIPER_EXE = r"C:\Users\villa\piper\piper.exe"
PIPER_MODEL = r"C:\Users\villa\piper\es_ES-sharvard-medium.onnx"


def hablar(texto):
    """Convierte texto a voz con Piper y lo reproduce por los altavoces."""
    if not texto:
        return

    # Archivo temporal donde Piper va a escribir el audio generado
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        ruta_wav = tmp.name

    try:
        subprocess.run(
            [PIPER_EXE, "--model", PIPER_MODEL, "--output_file", ruta_wav],
            input=texto,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=True,
        )

        datos, samplerate = sf.read(ruta_wav)
        sd.play(datos, samplerate)
        sd.wait()  # espera a que termine de reproducirse antes de continuar

    except FileNotFoundError:
        print(
            f"\n[Error] No encuentro piper.exe en '{PIPER_EXE}'. "
            "Revisa la ruta en tts.py.\n"
        )
    except subprocess.CalledProcessError as e:
        print(f"\n[Error de Piper] {e.stderr}\n")
    finally:
        if os.path.exists(ruta_wav):
            os.remove(ruta_wav)


if __name__ == "__main__":
    # Prueba suelta
    hablar("Hola, soy Jarvis. Esta es una prueba de mi voz.")
