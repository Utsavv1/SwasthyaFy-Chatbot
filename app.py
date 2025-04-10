from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import google.generativeai as genai
import re  
from googletrans import Translator  
import secrets  
from pymongo import MongoClient  # 👈 Add this

# 🔌 Connect to MongoDB here
client = MongoClient("mongodb://localhost:27017/")  
db = client["healthbot_db"]
chats_collection = db["chat_conversations"]

genai.configure(api_key="AIzaSyAy00DV8ewg2EAQYjKzMetfHzGE0zky7qg")
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  
translator = Translator()  

lang_map = {
    "english": "en",
    "hindi": "hi",
    "gujarati": "gu",
    "marathi": "mr",
    "kannada": "kn"
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        phone_number = request.form.get("phone_number") 
        age = request.form.get("age")
        gender = request.form.get("gender")
        language = request.form.get("language", "english")  

        session["language"] = language  # Store language in session
        
        current_user = {"name": name, "phone_number": phone_number, "age": age, "gender": gender}
        session["user_info"] = current_user
        session["chat_history"] = []

        return redirect(url_for("chatbot"))
    
    return render_template("index.html")

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    user_info = session.get("user_info", {})
    if not user_info:
        return redirect(url_for("index"))  
    
    chat_history = session.get("chat_history", [])
    language = session.get("language", "english")

    if request.method == "POST":
        user_input = request.form.get("user_input").strip()

        translated_input = user_input if language == "english" else translate_to_english(user_input, language)

        chat_history.append({"role": "user", "content": user_input})
        session["chat_history"] = chat_history  

        question_count = sum(1 for msg in chat_history if msg["role"] == "model" and "?" in msg["content"])

        try:
            if question_count < 6:
                prompt = f"Ask the next clarifying question about the user's symptoms. The user has said: {', '.join([msg['content'] for msg in chat_history if msg['role'] == 'user'])}."
                response = model.generate_content(prompt)
                bot_response = response.text.strip()
            else:
                prompt = (
                    f"Based on the user's symptoms ({', '.join([msg['content'] for msg in chat_history if msg['role'] == 'user'])}), "
                    f"provide a detailed History of Present Illness (HPI) summarizing the onset, duration, severity, location, and associated factors of the symptoms."
                    "Provide a list of 3 probable diseases, each on a new line."
                    "Also provide that disease's Description, Precautions, Medication, and Diet. The details should be in bullet points."
                    "Translates all HTML pages into the user's selected language"
                )
                response = model.generate_content(prompt)
                bot_response = response.text.strip()

                bot_response = clean_response(bot_response)
                
                if language != "english":
                    bot_response = translate_text(bot_response, language)

                session["predicted_diseases"] = bot_response
                return redirect(url_for("disease_prediction"))
        except Exception as e:
            bot_response = f"Sorry, I encountered an error: {str(e)}"
        
        if language != "english":
            bot_response = translate_text(bot_response, language)

        chat_history.append({"role": "model", "content": bot_response})
        session["chat_history"] = chat_history  

    return render_template("chatbot.html", user_info=user_info, chat_history=chat_history, language=language)

# def translate_text(text, language_name):
#     if not text or language_name == "english":
#         return text
#     try:
#         lang_map = {
#             "english": "en",
#             "hindi": "hi",
#             "gujarati": "gu",
#             "marathi": "mr",
#             "kannada": "kn"
#         }
#         language_code = lang_map.get(language_name.lower(), "en")
#         return translator.translate(text, dest=language_code).text
#     except Exception as e:
#         print(f"Translation Error: {e}")
#         return text

@app.route("/disease-prediction", methods=["GET"])
def disease_prediction():
    predicted_diseases = session.get("predicted_diseases", "No predictions available.")
    user_info = session.get("user_info", {})    
    user_responses = [msg["content"] for msg in session.get("chat_history", []) if msg["role"] == "user"]
    
    selected_language = request.args.get("lang", session.get("language", "english")).lower()
    session["language"] = selected_language  # Update session in case it's new
    language_code = lang_map.get(selected_language, "en")

    if not session.get("data_saved", False) and user_info and predicted_diseases:
        try:
            chats_collection.insert_one({
                "user": user_info,
                "chat_history": session.get("chat_history", []),
                "prediction": predicted_diseases
            })
            session["data_saved"] = True  # ✅ Mark as saved
        except Exception as e:
            print("MongoDB Insert Error:", e)

    if selected_language != "english":
        if isinstance(predicted_diseases, list):
            predicted_diseases = [translate_text(disease, selected_language) for disease in predicted_diseases]
        else:
            predicted_diseases = translate_text(predicted_diseases, selected_language)

        user_responses = [translate_text(response, selected_language) for response in user_responses]

        user_info = {
            key: translate_text(str(value), selected_language) for key, value in user_info.items()
        }

    return render_template(
        "disease_prediction.html",
        predicted_diseases=predicted_diseases,
        user_info=user_info,
        user_responses=user_responses,
        language_code=language_code
    )

@app.route("/clear-chat", methods=["POST"])
def clear_chat():
    try:
        session.pop("chat_history", None)
        return jsonify({"success": True})  
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/set-language", methods=["POST"])
def set_language():
    language = request.form.get("language", "english")
    session["language"] = language
    return jsonify({"success": True, "language": language})

def clean_response(response):
    response = response.replace("*", "").replace("_", "")
    response = response.capitalize()
    response = re.sub(r"\*\*(#.*?)\*\*", r"\1", response)
    return response

def translate_text(text, target_language_name):
    if not text or target_language_name == "english":
        return text
    try:
        lang_code = lang_map.get(target_language_name.lower(), "en")
        return translator.translate(text, dest=lang_code).text
    except Exception as e:
        print(f"Translation Error: {e}")
        return text
    
@app.route("/view-data")
def view_data():
    data = chats_collection.find().sort("_id", -1).limit(1)
    latest = next(data, {})
    return jsonify(latest)

if __name__ == "__main__":
    app.run(debug=True)
