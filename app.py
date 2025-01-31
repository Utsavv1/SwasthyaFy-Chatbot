from flask import Flask, render_template, request, redirect, url_for
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
                "first you want to ask the user's name ,user's age and their gender",
                "You are a healthcare chatbot. Ask 5 questions related to the symptoms but one by one the user provides and predict potential diseases. ",
                "you want give list of 3 related disease like first disease after that in new line second disease and after that in new line third disease that symptoms the user was provided.",
                "aslo give the description of that disease",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Okay, I'm ready to help. Please tell me about your symptoms. After you describe them, I'll ask some clarifying questions.  \n\n"
                "**Important Disclaimer:** I am an AI chatbot and cannot provide medical diagnoses. My purpose is to offer information and potential possibilities based on your input. "
                "Always consult with a doctor or other qualified healthcare professional for any health concerns. Do not delay seeking medical advice because of something you read here.",
            ],
        },
    ]
)

app = Flask(__name__)

# Initialize chat history in session
chat_history = []

@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history
    
    if request.method == "POST":
        # Get user input
        user_input = request.form.get("user_input")
        if user_input:
            # Add user message to chat history
            chat_history.append({"role": "user", "content": user_input})

            # Check if the user input is a greeting
            greeting_keywords = ["hi", "hello", "hey", "hola", "greetings"]
            if any(greeting in user_input.lower() for greeting in greeting_keywords):
                chatbot_response = "Hello! How can I assist you today? Please describe your symptoms."
                chat_history.append({"role": "model", "content": chatbot_response})

            else:
                # Process as a symptom-related question if not a greeting
                response = chat_session.send_message(user_input)
                
                # Safely extract the text from the response
                chatbot_response = ""
                if hasattr(response, '_result') and len(response._result.candidates) > 0:
                    candidate = response._result.candidates[0]
                    parts = candidate.content.parts if hasattr(candidate.content, 'parts') else []
                    if parts:
                        chatbot_response = parts[0].text if hasattr(parts[0], 'text') else "No valid response found"

                chat_history.append({"role": "model", "content": chatbot_response})
        
    return render_template("index.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
