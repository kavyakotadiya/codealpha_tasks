# AI Language Translator

A simple, demo-ready language translation app built with Python and Streamlit.

It translates text between selected languages using `googletrans` with automatic fallback to `deep-translator` if needed.

## Features

- Text input box
- Source language dropdown (with Auto Detect)
- Target language dropdown
- Translate button
- Clear translated output display
- Copy to Clipboard button
- Optional text-to-speech playback (gTTS)

## Supported Languages

- English
- Hindi
- Gujarati
- Spanish
- French
- German

## Setup

1. Create virtual environment:

```powershell
python -m venv .venv
```

2. Activate virtual environment (PowerShell):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Run the app:

```bash
python -m streamlit run app.py
```

## Project Structure

- `app.py` - Main Streamlit app
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

## Screenshot

_Add screenshot here_
