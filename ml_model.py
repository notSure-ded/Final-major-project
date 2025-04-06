import re
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

training_data = [
    ("Where is the library?", {"intent": "location_query", "entity": "library"}),
    ("Where is the canteen?", {"intent": "location_query", "entity": "canteen"}),
    ("When is Dr. Sharma free?", {"intent": "availability_query", "entity": "dr. sharma"}),
    ("When is Prof. Mehta free?", {"intent": "availability_query", "entity": "prof. mehta"}),
    ("What time is the physics lecture?", {"intent": "timetable_query", "entity": "physics"}),
    ("When is the chemistry class?", {"intent": "timetable_query", "entity": "chemistry"}),
]


X_train = [x[0].lower() for x in training_data]
y_train = [x[1]['intent'] for x in training_data]

vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X_train)

model = MultinomialNB()
model.fit(X_vec, y_train)

with open("intent_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

# ml_model.py

def extract_entity(message):
    teachers = ["dr. smith", "prof. john", "mr. ray", "ms. priya"]
    places = ["library", "canteen", "lab", "classroom", "auditorium"]
    subjects = ["math", "physics", "chemistry", "cs", "computer science", "ai", "machine learning"]

    msg = message.lower()

    for t in teachers:
        if t in msg:
            return t
    for p in places:
        if p in msg:
            return p
    for s in subjects:
        if s in msg:
            return s
    return None

