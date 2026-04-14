# 📘 AI Flashcard Generator

An AI-powered application that converts PDF documents into interactive flashcards to enhance learning using Active Recall and Spaced Repetition techniques.

# 🚀 Live Demo

👉 https://flashcardai-2pqt9e9emt7iaeadv9tn9s.streamlit.app

## 🧠 Features
* 📄 Upload PDF files
* 🤖 AI-generated flashcards (Q&A format)
* 🔄 Flip cards (Active Recall learning)
* 🧠 Spaced repetition (Hard / Medium / Easy rating)
* 📊 Learning progress tracking
* 🎯 Clean and interactive UI using Streamlit

## 🛠️ Tech Stack
* **Frontend & UI:** Streamlit
* **Backend Logic:** Python
* **AI Model:** Cerebras (LLaMA 3.1)
* **PDF Processing:** PyMuPDF
* **Environment Management:** python-dotenv

## ⚙️ Setup Instructions
1. Clone the repository
```commandline
git clone https://github.com/aravindvojjala/Flashcard_AI
cd flashcard-ai
```

2. Install dependencies
```commandline
pip install -r requirements.txt
```

3. Set up environment variables

Create a `.env` file in the root directory:
```commandline
CEREBRAS_API_KEY=your_api_key_here
```
4. Run the application
```commandline
streamlit run main.py
```

## 🌍 Deployment

This app is deployed using **Streamlit Cloud.**

To deploy:

1. Push code to GitHub 
2. Connect repository in Streamlit Cloud
3. Add secret:

CEREBRAS_API_KEY = your_api_key

4. Deploy

## 🧪 How It Works
1. User uploads a PDF
2. Text is extracted using PyMuPDF
3. AI model processes the text
4. Flashcards are generated in Q&A format
5. User interacts using:
   * Flip (to reveal answer)
   * Rate difficulty (spaced repetition)


## 🔐 Security Note
* API keys are stored securely using `.env`
* `.env` is excluded via `.gitignore`
* `.env.example` is provided for reference

## 🎯 Future Improvements
* Save flashcards for later use
* Multi-deck support
* Enhanced UI animations
* Export flashcards

## 👨‍💻 Author

Aravind