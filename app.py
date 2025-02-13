from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyBFcVdWmupoYN_u6yH4lykcdx6qymaiXLY")  # Replace with your actual API key

# Create the model with generation configuration
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

# Start the chat session with an initial system message
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "You are a healthcare chatbot. Ask 6 question related the first answer but ask one question at a time and in the end provide probable disease.",
                "You want to give a list of 3 related diseases like: first disease, then in a new line second disease, and then in a new line third disease based on the symptoms the user provides.",
                "Also, give the description of those diseases.",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Okay, I'm ready to help. Please tell me about your symptoms. After you describe them, I'll ask some clarifying questions one by one. after that provide list of that 3 disease not in same line \n\n"
                "**Important Disclaimer:** I am an AI chatbot and cannot provide medical diagnoses. My purpose is to offer information and potential possibilities based on your input."
                "Always consult with a doctor or other qualified healthcare professional for any health concerns. Do not delay seeking medical advice because of something you read here.",
            ],
        },
    ]
)

app = Flask(__name__)
app.secret_key = "AIzaSyBFcVdWmupoYN_u6yH4lykcdx6qymaiXLY"  # Required for session management

# Route for the user information page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user information from the form
        name = request.form.get("name")
        email = request.form.get("email")  # Get email from the form
        age = request.form.get("age")
        gender = request.form.get("gender")

        # Store user information in the session
        session["user_info"] = {
            "name": name,
            "email": email,  # Add email to session
            "age": age,
            "gender": gender
        }

        # Initialize chat history for the user if not already present
        if "chat_history" not in session:
            session["chat_history"] = []

        # Redirect to the chatbot page
        return redirect(url_for("chatbot"))

    return render_template("index.html")

# Route for the chatbot page
@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    # Retrieve user information from the session
    user_info = session.get("user_info", {})
    if not user_info:
        return redirect(url_for("index"))  # Redirect to the user info page if no user data exists

    # Retrieve chat history from the session
    chat_history = session.get("chat_history", [])

    if request.method == "POST":
        # Get user input
        user_input = request.form.get("user_input").strip().lower()  # Normalize input

        # Check for greeting keywords
        greeting_keywords = ["hello", "hi", "hey", "hola", "greetings"]
        if any(greeting in user_input for greeting in greeting_keywords):
            bot_response = "Hello! How can I assist you today?"
        else:
            # Simulate bot response (replace with actual AI logic)
            bot_response = f"You said: {user_input}. Here's my response."

        # Add user message to chat history
        chat_history.append({"role": "user", "content": user_input})
        session["chat_history"] = chat_history  # Save updated chat history to session

        # Add bot response to chat history
        chat_history.append({"role": "model", "content": bot_response})
        session["chat_history"] = chat_history  # Save updated chat history to session

    return render_template("chatbot.html", user_info=user_info, chat_history=chat_history)

# Route to clear chat history
@app.route("/clear-chat", methods=["POST"])
def clear_chat():
    try:
        # Clear chat history from the session
        session.pop("chat_history", None)
        return jsonify({"success": True})  # Return a JSON response
    except Exception as e:
        # Handle unexpected errors gracefully
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)