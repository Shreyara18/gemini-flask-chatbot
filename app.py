from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("\nAVAILABLE MODELS:\n")

for m in genai.list_models():
    print(m.name)
    
# Load the Gemini model
model = genai.GenerativeModel("models/gemini-flash-lite-latest")
# Define the route for the home page
@app.route('/')
def index():
    return render_template('index.html')


# Define the route for the chat endpoint, which accepts POST requests
@app.route('/chat', methods=['POST'])
def chat():

    # Get the user's message from the JSON payload of the request
    user_input = request.json.get('message')

    print(f"Received message: {user_input}")

    # Get the response from Gemini
    response = get_gemini_response(user_input)

    print(f"Gemini response: {response}")

    # Return the Gemini response as a JSON object
    return jsonify({'response': response})


# Function to get a response from Gemini
def get_gemini_response(user_input):

    try:

        # Generate content using Gemini
        response = model.generate_content(user_input)

        # Return the generated response text
        return response.text

    except Exception as e:

    # Handle errors
        print(f"FULL ERROR: {e}")

        return f"Gemini Error: {e}"

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)