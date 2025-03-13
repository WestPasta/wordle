from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app and CORS (to allow React to communicate with Flask)
app = Flask(__name__)
CORS(app)

# Firebase Admin SDK setup
cred = credentials.Certificate(r"C:\Issac Compass\Hackathon\backend\ickathon-firebase-adminsdk-fbsvc-6c2c33ae2f.json")  # Path to Firebase service account credentials
firebase_admin.initialize_app(cred)
db = firestore.client()  # Initialize Firestore

# Hardcoded correct word (for now)
CORRECT_WORD = "apple"

# Wordle check function
def check_guess(guess):
    result = []
    for i, letter in enumerate(guess):
        if letter == CORRECT_WORD[i]:
            result.append("✅")  # Correct letter in correct position
        elif letter in CORRECT_WORD:
            result.append("🟡")  # Correct letter, wrong position
        else:
            result.append("⬜")  # Letter not in word
    return result

# Route to get the correct word
@app.route("/word", methods=["GET"])
def get_word():
    return jsonify({"word": CORRECT_WORD})

@app.route("/check-word", methods=["POST"])
def check_word():
    data = request.json
    guess = data.get("guess", "").lower()
    user_id = data.get("userId")  # Get user ID from request
    username = data.get("username")  # Get username from request

    if len(guess) != 5:
        return jsonify({"error": "Word must be 5 letters"}), 400

    result = check_guess(guess)

    # ✅ Auto-save score if user wins
    if guess == CORRECT_WORD:
        if not user_id:
            return jsonify({"error": "Missing user ID"}), 400
        
        score_data = {
            "userId": user_id,
            "username": username,
            "score": 1,  # Fixed score for now
            "timestamp": firestore.SERVER_TIMESTAMP
        }

        try:
            db.collection("scores").add(score_data)  # Save to Firestore
            return jsonify({"result": result, "message": "You won! Score saved."})
        except Exception as e:
            return jsonify({"error": f"Error saving score: {str(e)}"}), 500

    return jsonify({"result": result})

def apply_cors(response):
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    return response

if __name__ == "__main__":
    app.run(debug=True)
