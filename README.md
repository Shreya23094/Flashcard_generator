# 📘 AI Flashcard Generator

A Streamlit web app that automatically generates flashcards from uploaded PDF documents using Hugging Face's transformer models.

## 🚀 Features

- Upload any PDF and extract its content.
- Generate **question-answer style flashcards** using a language model (`flan-t5-large`).
- View the flashcards interactively.
- Easily extendable and lightweight.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

git clone https://github.com/your-username/flashcard-generator.git
cd flashcard-generator

### 2. Create a Virtual Environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Run the app locally:
streamlit run app.py