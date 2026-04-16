# AI FAQ Chatbot

A simple FAQ chatbot built with Python, Streamlit, NLTK, and scikit-learn.

## Features

- Conversational chat UI with Streamlit
- FAQ matching using TF-IDF + cosine similarity
- Basic NLP preprocessing (lowercasing, punctuation removal, tokenization)
- Chat history for both user and bot messages
- Fallback response when confidence is low

## Project Structure

- `app.py` - Main chatbot app
- `requirements.txt` - Python dependencies
- `README.md` - Setup and usage instructions

## Setup

### 1. Create virtual environment

```powershell
python -m venv venv
```

### 2. Activate virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the app

```powershell
streamlit run app.py
```

## How It Works

1. FAQ questions are preprocessed.
2. TF-IDF vectors are created from FAQ questions.
3. User query is preprocessed and vectorized.
4. Cosine similarity is computed against all FAQ questions.
5. The answer of the best match is returned if score >= 0.3.
6. Otherwise, fallback response is shown.
