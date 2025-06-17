import streamlit as st
from utils.pdf_loader import extract_text_from_pdf
from utils.chunker import chunk_text
from utils.flashcard_gen import generate_flashcards
from utils.exporter import export_as_json, export_as_csv
import random

st.set_page_config(page_title="AI Flashcard Generator", layout="wide")
st.title("📚 AI Flashcard Generator")

def init_state():
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = []
        st.session_state.current = 0
        st.session_state.mode = "idle"
        st.session_state.subject = "General"

init_state()

# Sidebar Inputs
st.sidebar.title("Input Options")
input_mode = st.sidebar.radio("Choose input type", ["Upload PDF", "Paste Text"])
subject_type = st.sidebar.selectbox("Subject Category", ["General", "Biology", "History", "Computer Science"])
st.session_state.subject = subject_type

text = ""
if input_mode == "Upload PDF":
    file = st.sidebar.file_uploader("Upload your PDF", type=["pdf"])
    if file:
        text = extract_text_from_pdf(file)
elif input_mode == "Paste Text":
    text = st.sidebar.text_area("Paste your content here")

if text and st.sidebar.button("Generate Flashcards"):
    chunks = chunk_text(text)
    all_cards = []
    with st.spinner("Generating flashcards..."):
        for chunk in chunks:
            cards = generate_flashcards(chunk, subject=subject_type)
            all_cards.extend(cards)

    st.session_state.flashcards = all_cards
    st.session_state.current = 0
    st.session_state.mode = "review"
    st.rerun()


# Review Mode
if st.session_state.mode == "review":
    cards = st.session_state.flashcards
    idx = st.session_state.current

    if idx < len(cards):
        q = cards[idx]["question"]
        a = cards[idx]["answer"]
        st.markdown(f"### Flashcard {idx + 1} of {len(cards)}")
        st.markdown(f"**Q:** {q}")
        with st.expander("💡 Show Answer"):
            st.write(a)

        col1, col2, col3 = st.columns(3)
        if col1.button("✅ Correct"):
            st.session_state.current += 1
        if col2.button("❌ Incorrect"):
            cards.append(cards.pop(idx))
        if col3.button("🔀 Shuffle"):
            random.shuffle(cards)
            st.session_state.current = 0

    else:
        st.success("🎉 You've reviewed all flashcards!")

    st.download_button("📥 Export JSON", export_as_json(cards), file_name="flashcards.json")
    st.download_button("📥 Export CSV", export_as_csv(cards), file_name="flashcards.csv")

elif st.session_state.mode == "idle":
    st.info("Upload a file or paste content in the sidebar to begin.")
