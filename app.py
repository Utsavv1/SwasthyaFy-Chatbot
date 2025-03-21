from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import google.generativeai as genai
import re  

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
app.secret_key = "AIzaSyAy00DV8ewg2EAQYjKzMetfHzGE0zky7qg"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        phone_number = request.form.get("phone number") 
        age = request.form.get("age")
        gender = request.form.get("gender")
        current_user = {"name": name, "phone number": phone_number, "age": age, "gender": gender}
        if "user_info" in session:
            if session["user_info"] != current_user:
                session.clear()  
                session["user_info"] = current_user
                session["chat_history"] = []
        else:
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

    if request.method == "POST":
        user_input = request.form.get("user_input").strip().lower()
        chat_history.append({"role": "user", "content": user_input})
        session["chat_history"] = chat_history 
        question_count = sum(1 for msg in chat_history if msg["role"] == "model" and "?" in msg["content"])

        try:
            if question_count < 6:
                prompt = f"Ask the next clarifying question about the user's symptoms. So far, the user has said: {', '.join([msg['content'] for msg in chat_history if msg['role'] == 'user'])}."
                response = model.generate_content(prompt)
                bot_response = response.text.strip()
            else:
                prompt = (
                    f"Based on the user's symptoms ({', '.join([msg['content'] for msg in chat_history if msg['role'] == 'user'])}), "
                    f"Based on the user's symptoms, provide a detailed History of Present Illness (HPI) summarizing the onset, duration, severity, location, and associated factors of the symptoms."
                    "provide a list of 3 probable diseases, each on a new line."
                    "Also provide that diseases Description, Precautions, Medication, and iet."
                )
                response = model.generate_content(prompt)
                bot_response = response.text.strip()

                bot_response = clean_response(bot_response)

                session["predicted_diseases"] = bot_response
                return redirect(url_for("disease_prediction"))
        except Exception as e:
            bot_response = f"Sorry, I encountered an error: {str(e)}"
        chat_history.append({"role": "model", "content": bot_response})
        session["chat_history"] = chat_history  

    return render_template("chatbot.html", user_info=user_info, chat_history=chat_history)

@app.route("/disease-prediction", methods=["GET"])
def disease_prediction():
    predicted_diseases = session.get("predicted_diseases", "No predictions available.")

    user_info = session.get("user_info", {}) 
    chat_history = session.get("chat_history", [])
    user_responses = [msg["content"] for msg in chat_history if msg["role"] == "user"]
    return render_template(
        "disease_prediction.html",
        predicted_diseases=predicted_diseases,
        user_info=user_info,
        user_responses=user_responses
    )

@app.route("/clear-chat", methods=["POST"])
def clear_chat():
    try:
        session.pop("chat_history", None)
        return jsonify({"success": True})  
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Helper function to clean the response
def clean_response(response):
    """
    Cleans the response by removing unwanted characters, extra spaces, and formatting.
    """

    response = response.replace("*", "").replace("_", "")
    
    response = response.capitalize()
    response = re.sub(r"\*\*(.*?)\*\*", r"\1", response)

    return response

if __name__ == "__main__":
    app.run(debug=True)