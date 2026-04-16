import json
from io import BytesIO

import streamlit as st


def get_languages() -> dict[str, str]:
    """Return supported languages for source/target dropdowns."""
    return {
        "English": "en",
        "Hindi": "hi",
        "Gujarati": "gu",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
    }


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Translate text using googletrans first, then deep-translator fallback."""
    # Try googletrans first (requested primary option).
    try:
        from googletrans import Translator

        translator = Translator()
        result = translator.translate(text, src=source_lang, dest=target_lang)
        if result and result.text:
            return result.text
    except Exception:
        pass

    # Fallback to deep-translator if googletrans fails.
    from deep_translator import GoogleTranslator

    return GoogleTranslator(source=source_lang, target=target_lang).translate(text)


def render_copy_button(text: str) -> None:
    """Render a simple HTML/JS copy button for translated output."""
    payload = json.dumps(text)
    copy_html = f"""
    <div style=\"margin-top: 0.5rem;\">
      <button onclick='navigator.clipboard.writeText({payload})'
              style='padding: 0.45rem 0.8rem; border-radius: 8px; border: 1px solid #ccc; cursor: pointer;'>
        Copy to Clipboard
      </button>
    </div>
    """
    st.components.v1.html(copy_html, height=52)


def render_tts(text: str, lang_code: str) -> None:
    """Generate and play text-to-speech audio (optional feature)."""
    from gtts import gTTS

    audio_fp = BytesIO()
    tts = gTTS(text=text, lang=lang_code)
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    st.audio(audio_fp.read(), format="audio/mp3")


def main() -> None:
    st.set_page_config(page_title="AI Language Translator", page_icon="🌍", layout="centered")

    st.title("AI Language Translator")
    st.caption("Simple and clean text translation using Google Translate providers.")

    languages = get_languages()
    source_options = {"Auto Detect": "auto", **languages}

    input_text = st.text_area("Enter text", placeholder="Type text to translate...", height=150)

    col1, col2 = st.columns(2)
    with col1:
        src_name = st.selectbox("Source Language", list(source_options.keys()), index=0)
    with col2:
        default_target = list(languages.keys()).index("Hindi")
        tgt_name = st.selectbox("Target Language", list(languages.keys()), index=default_target)

    translate_clicked = st.button("Translate", type="primary", use_container_width=True)

    if translate_clicked:
        text = input_text.strip()
        if not text:
            st.warning("Please enter some text to translate.")
            return

        src_code = source_options[src_name]
        tgt_code = languages[tgt_name]

        try:
            translated = translate_text(text=text, source_lang=src_code, target_lang=tgt_code)
            st.subheader("Translated Text")
            st.text_area("Result", translated, height=150, disabled=True, label_visibility="collapsed")
            render_copy_button(translated)

            enable_tts = st.checkbox("Play text-to-speech", value=False)
            if enable_tts:
                try:
                    render_tts(translated, tgt_code)
                except Exception as tts_error:
                    st.info(f"Text-to-speech is unavailable for this language/input: {tts_error}")

        except Exception as err:
            st.error(f"Translation failed. Please try again. Details: {err}")


if __name__ == "__main__":
    main()
