import re
import string

import nltk
import streamlit as st
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


FALLBACK_RESPONSE = "Sorry, I don't understand the question."
SIMILARITY_THRESHOLD = 0.3


FAQ_DATA = [
    {"question": "What is AI?", "answer": "AI stands for Artificial Intelligence."},
    {
        "question": "What is machine learning?",
        "answer": "Machine learning is a subset of AI where systems learn from data.",
    },
    {
        "question": "What is deep learning?",
        "answer": "Deep learning is a machine learning technique based on neural networks.",
    },
    {
        "question": "What is Python?",
        "answer": "Python is a popular programming language used for web, data, and AI projects.",
    },
    {
        "question": "What is NLP?",
        "answer": "NLP means Natural Language Processing, a field focused on language understanding.",
    },
    {
        "question": "What is Streamlit?",
        "answer": "Streamlit is a Python framework for building interactive data and AI apps quickly.",
    },
    {
        "question": "What is scikit-learn?",
        "answer": "Scikit-learn is a Python library for machine learning algorithms and tools.",
    },
    {
        "question": "What is overfitting?",
        "answer": "Overfitting happens when a model learns training data too closely and performs poorly on new data.",
    },
    {
        "question": "What is underfitting?",
        "answer": "Underfitting happens when a model is too simple to learn patterns in the data.",
    },
    {
        "question": "What is a dataset?",
        "answer": "A dataset is a collection of data used for analysis or model training.",
    },
    {
        "question": "What is cosine similarity?",
        "answer": "Cosine similarity measures how similar two text vectors are by comparing their angle.",
    },
    {
        "question": "What is TF-IDF?",
        "answer": "TF-IDF is a text representation technique that weighs words by importance in documents.",
    },
    {
        "question": "Why is preprocessing needed in NLP?",
        "answer": "Preprocessing cleans and standardizes text so models can compare meaning more effectively.",
    },
    {
        "question": "Can this chatbot answer any question?",
        "answer": "No. This chatbot answers only questions similar to the FAQs it knows.",
    },
]


def setup_nltk():
    """Ensure required NLTK tokenizer resources are available."""
    resources = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
    ]
    for resource_path, resource_name in resources:
        try:
            nltk.data.find(resource_path)
        except LookupError:
            nltk.download(resource_name, quiet=True)


def preprocess_text(text):
    """Lowercase, remove punctuation, tokenize, and rebuild text."""
    text = text.lower().strip()
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    tokens = word_tokenize(text)
    return " ".join(token for token in tokens if token.strip())


setup_nltk()
PREPROCESSED_QUESTIONS = [preprocess_text(item["question"]) for item in FAQ_DATA]
VECTORIZER = TfidfVectorizer()
FAQ_VECTORS = VECTORIZER.fit_transform(PREPROCESSED_QUESTIONS)


def get_best_match(user_input):
    """Return index and score of best FAQ match for given user input."""
    processed_input = preprocess_text(user_input)
    input_vector = VECTORIZER.transform([processed_input])
    similarities = cosine_similarity(input_vector, FAQ_VECTORS).flatten()
    best_index = similarities.argmax()
    best_score = similarities[best_index]
    return best_index, best_score


def chatbot_response(user_input):
    """Return chatbot response using cosine similarity over FAQ questions."""
    if not user_input or not user_input.strip():
        return FALLBACK_RESPONSE

    best_index, best_score = get_best_match(user_input)

    if best_score < SIMILARITY_THRESHOLD:
        return FALLBACK_RESPONSE

    return FAQ_DATA[best_index]["answer"]


def init_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def main():
    setup_nltk()
    init_state()

    st.set_page_config(page_title="AI FAQ Chatbot", page_icon="💬", layout="centered")
    st.title("AI FAQ Chatbot")
    st.caption("Ask a question about AI, ML, NLP, and related basics.")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your question here...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        bot_reply = chatbot_response(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            st.markdown(bot_reply)


if __name__ == "__main__":
    main()
