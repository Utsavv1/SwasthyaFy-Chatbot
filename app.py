from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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

        # Check if the user is new or returning
        current_user = {"name": name, "email": email, "age": age, "gender": gender}
        if "user_info" in session:
            # If the user info in the session doesn't match the current user, start a new chat
            if session["user_info"] != current_user:
                session.clear()  # Clear session for the new user
                session["user_info"] = current_user
                session["chat_history"] = []  # Start a new chat history
        else:
            # Initialize session for the new user
            session["user_info"] = current_user
            session["chat_history"] = []  # Start a new chat history

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

        # Add user message to chat history
        chat_history.append({"role": "user", "content": user_input})
        session["chat_history"] = chat_history  # Save updated chat history to session

        # Count the number of questions asked so far
        question_count = sum(1 for msg in chat_history if msg["role"] == "model" and "?" in msg["content"])

        # Generate bot response
        try:
            if question_count < 6:
                # Ask the next question
                prompt = f"Ask the next clarifying question about the user's symptoms. So far, the user has said: {', '.join([msg['content'] for msg in chat_history if msg['role'] == 'user'])}."
                response = model.generate_content(prompt)
                bot_response = response.text.strip()
            else:
                # Provide a list of probable diseases and descriptions
                prompt = (
                    f"Based on the user's symptoms ({', '.join([msg['content'] for msg in chat_history if msg['role'] == 'user'])}), "
                    "provide a list of 3 probable diseases, describe each disease on a new line with their number, along with their descriptions."
                )
                response = model.generate_content(prompt)
                bot_response = response.text.strip()
        except Exception as e:
            bot_response = f"Sorry, I encountered an error: {str(e)}"

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