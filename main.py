import streamlit as st
import fitz
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import re

# Load env
#load_dotenv()
api_key = os.getenv("CEREBRAS_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.cerebras.ai/v1"
)

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="Flashcard AI", layout="centered")

st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #1e1e1e;
    color: white;
    font-size: 18px;
    text-align: center;
    margin-top: 20px;
}
button {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📘 Flashcard AI (Smart Learning)")

# ---------------- FUNCTIONS ----------------

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])


def generate_flashcards(text):
    prompt = f"""
    You are an expert teacher.

    Create detailed flashcards from the text.

    Rules:
    - Each answer must be 3–5 lines (NOT one line)
    - Include explanation + example if possible
    - Cover concepts, definitions, and reasoning
    - Minimum 5 flashcards

    Return ONLY JSON:
    [
      {{
        "question": "...",
        "answer": "detailed explanation (3–5 lines)"
      }}
    ]

    Text:
    {text[:5000]}
    """

    response = client.chat.completions.create(
        model="llama3.1-8b",
        messages=[{"role": "user", "content": prompt}],
    )

    raw_output = response.choices[0].message.content

    # 🔥 Extract JSON safely
    try:
        json_match = re.search(r"\[.*\]", raw_output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            st.error("No valid JSON found in response")
            return []
    except Exception as e:
        st.error(f"Parsing error: {e}")
        st.text_area("DEBUG RAW OUTPUT", raw_output, height=300)
        return []

# ---------------- SESSION STATE ----------------

if "cards" not in st.session_state:
    st.session_state.cards = []

if "index" not in st.session_state:
    st.session_state.index = 0

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

if "scores" not in st.session_state:
    st.session_state.scores = []  # spaced repetition


# ---------------- UPLOAD ----------------

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file and not st.session_state.cards:
    with st.spinner("Generating flashcards..."):
        text = extract_text(uploaded_file)
        if len(text.strip()) < 50:
            st.error("PDF text extraction failed or empty")
            st.stop()
        cards = generate_flashcards(text)

        st.session_state.cards = cards
        st.session_state.scores = [0] * len(cards)

        st.success(f"{len(cards)} Flashcards Generated!")

# ---------------- DISPLAY CARD ----------------

if st.session_state.cards:
    i = st.session_state.index
    card = st.session_state.cards[i]

    st.markdown(f"### Card {i + 1} / {len(st.session_state.cards)}")

    # ---------------- QUESTION / ANSWER ----------------

    if not st.session_state.show_answer:

        st.markdown(f"""
        <div class='card'>
        ❓ <b>Question:</b><br><br>
        {card['question']}
        </div>
        """, unsafe_allow_html=True)

        st.info("Think of the answer before revealing it!")

        if st.button("🔄 Show Answer", key="flip"):
            st.session_state.show_answer = True

    else:
        st.markdown(f"""
        <div class='card'>
        ✅ <b>Answer:</b><br><br>
        {card['answer'].replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🧠 Rate your understanding")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("❌ Hard", key="hard"):
                st.session_state.scores[i] -= 1
                st.session_state.index += 1
                st.session_state.show_answer = False

        with col2:
            if st.button("😐 Medium", key="medium"):
                st.session_state.index += 1
                st.session_state.show_answer = False

        with col3:
            if st.button("✅ Easy", key="easy"):
                st.session_state.scores[i] += 1
                st.session_state.index += 1
                st.session_state.show_answer = False

   # ---------------- NAVIGATION ----------------

    col4, col5 = st.columns(2)

    with col4:
        if st.button("⬅️ Previous", key="prev"):
            st.session_state.index -= 1
            st.session_state.show_answer = False

    with col5:
        if st.button("➡️ Next", key="next"):
            st.session_state.index += 1
            st.session_state.show_answer = False

    # ---------------- SAFE INDEX ----------------
    st.session_state.index = st.session_state.index % len(st.session_state.cards)

    # ---------------- PROGRESS ----------------

    st.markdown("### 📊 Learning Progress")

    mastered = sum(1 for s in st.session_state.scores if s > 1)
    weak = sum(1 for s in st.session_state.scores if s < 0)

    st.write(f"✅ Mastered: {mastered}")
    st.write(f"⚠️ Needs Review: {weak}")

    st.progress(mastered / len(st.session_state.cards))