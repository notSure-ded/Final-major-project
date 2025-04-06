import json
import random
import sqlite3
import pickle
from ml_model import extract_entity

with open("intent.json") as file:
    intents = json.load(file)

with open("intent_model.pkl", "rb") as f:
    model, vectorizer = pickle.load(f)

def get_intent(user_input):
    input_lower = user_input.lower()
    for intent in intents:
        if any(phrase in input_lower for phrase in intent["patterns"]):
            return random.choice(intent["responses"]), intent["tag"]
    return "I'm not sure what you mean.", "unknown"

def get_bot_response(message, student_id=None):
    msg = message.lower()

    try:
        X_input = vectorizer.transform([msg])
        probs = model.predict_proba(X_input)[0]
        max_prob = max(probs)
        intent_idx = probs.argmax()
        intent = model.classes_[intent_idx]

        # Threshold: Only accept ML prediction if it's confident
        if max_prob > 0.7:
            entity = extract_entity(msg)

            if intent == "location_query":
                return f"{entity.capitalize()} is located in Block B, 2nd floor." if entity else "Please specify the place you're asking about."

            elif intent == "availability_query":
                return f"{entity.title()} is free on Monday and Wednesday at 3 PM." if entity else "Tell me which teacher you're asking about."

            elif intent == "timetable_query":
                return f"The {entity} class is at 10 AM on Tuesday and Thursday." if entity else "Which subject are you talking about?"

    except Exception as e:
        print("ML intent failed:", e)

    # Fall back to pattern matching
    response, tag = get_intent(msg)

    if tag == "attendance" and student_id:
        conn = sqlite3.connect('university.db')
        cur = conn.cursor()
        cur.execute("SELECT name, attendance FROM students WHERE student_id=?", (student_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return f"{row[0]}, your attendance is {row[1]}%."
        else:
            return "Student not found."

    elif tag == "results" and student_id:
        conn = sqlite3.connect('university.db')
        cur = conn.cursor()
        cur.execute("SELECT name, results FROM students WHERE student_id=?", (student_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return f"{row[0]}, your result is {row[1]}%."
        else:
            return "Student not found."

    elif tag == "timetable":
        return "Mon-Fri: 9am-5pm. Labs on Wed/Fri. Sundays are for crying under your blanket."

    return response
