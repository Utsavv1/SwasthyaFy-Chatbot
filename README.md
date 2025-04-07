# 🏥 Gemini Healthcare Chatbot

![Gemini Healthcare Chatbot UI](https://via.placeholder.com/1000x400.png?text=Gemini+Healthcare+Chatbot+UI)

The **Gemini Healthcare Chatbot** is an AI-powered web application built with **Python** and **Flask**, integrated with the **Google Gemini API** to identify possible diseases based on user-reported symptoms. This project is ideal for:

- 🧪 Educational learning in healthcare AI
- 🧰 Prototyping intelligent medical assistants
- 🏥 Building larger healthcare platforms

It simulates a realistic diagnostic conversation, predicts probable diseases, and suggests precautions, medications, and diets accordingly.

---

## 🚀 Features

- 💬 **Interactive Conversations** — Engages users through dynamic, question-based symptom collection.
- 🧠 **AI-Powered Disease Prediction** — Predicts 3 probable diseases using symptom data.
- 👤 **User Personalization** — Collects and displays user data (name, age, gender, email).
- 🌐 **Multilingual Support** *(optional)* — Translate output with Google Translate API.
- 📱 **Responsive UI** — Built with mobile-first, modern design in mind.
- 💾 **Session Management** — Uses Flask sessions to retain user context.
- ⚠️ **Error Handling** — Catches missing or invalid inputs gracefully.

---

## 🧰 Tech Stack

| Layer        | Technology                  |
|--------------|------------------------------|
| Backend      | Python, Flask                |
| Frontend     | HTML, CSS, Jinja2 Templates  |
| AI Model     | Google Gemini API (`gemini-1.5-flash`) |
| API Client   | `google-generativeai`        |
| Environment  | `.env` for API key           |

---

## 📦 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Google Gemini API Key

---

## 🔑 Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app)
2. Sign in with your Google account
3. Create a new API key
4. Save the key for the `.env` file

---

~## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/gemini-healthcare-chatbot.git
cd gemini-healthcare-chatbot
```

## 2. 🧪 Create & Activate Virtual Environment (Recommended)


# For Linux/macOS
```bash
python -m venv venv
source venv/bin/activate
```
# For Windows
```bash
python -m venv venv
venv\Scripts\activate~
```