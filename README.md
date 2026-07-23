# Jarvis — Proyecto personal

Asistente de voz construido paso a paso, 100% local y gratis para empezar.

## Fase 0 — Setup

1. Instala [Python 3.10+](https://www.python.org/downloads/) y [Git](https://git-scm.com/downloads).
2. Instala [Ollama](https://ollama.com/download) (motor para correr LLMs en local, gratis).
3. Una vez instalado Ollama, descarga un modelo pequeño y rápido:
   ```bash
   ollama pull llama3.2
   ```
4. Crea un entorno virtual de Python dentro de esta carpeta:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Mac/Linux:
   source venv/bin/activate
   ```
5. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Fase 1 — Chat de texto con el cerebro local

Con Ollama corriendo en segundo plano (se queda activo tras instalarlo), ejecuta:

```bash
python chat.py
```

Esto abre un chat por terminal con tu LLM local. Escribe algo, pulsa Enter, y Jarvis (versión texto, sin voz todavía) te responde. Escribe `salir` para terminar.

## Subir esto a GitHub (para que no se pierda nunca)

```bash
git init
git add .
git commit -m "Fase 0 y 1: setup y chat de texto"
```

Luego crea un repositorio vacío en GitHub (botón "New repository", puede ser privado) y sigue las instrucciones que te da GitHub para conectar tu carpeta local con ese repo remoto (`git remote add origin ...` y `git push`).

A partir de aquí, cada vez que avances una fase: `git add .` → `git commit -m "mensaje"` → `git push`.

## Próximas fases

- Fase 2: añadir entrada de voz (Whisper)
- Fase 3: añadir salida de voz (Piper)
- Fase 4: wake word ("Oye Jarvis")
- Fase 5: herramientas (function calling)
- Fase 6: memoria persistente
- Fase 7: conectar Claude API (opcional, cuando quieras más inteligencia)
- Fase 8: portabilidad con Docker
- Fase 9: interfaz visual chula
