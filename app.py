from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os
import re

app = Flask(__name__)
CORS(app)

# Configuration
VECTORIZER_PATH = "medical_vectorizer.joblib"
MATRIX_PATH = "medical_matrix.joblib"
DATA_PATH = "medical_data.csv"

# Medical keywords list (expandable)
MEDICAL_KEYWORDS = [
    'pain', 'ache', 'fever', 'cough', 'cold', 'headache', 'stomach',
    'nausea', 'vomit', 'diarrhea', 'constipation', 'rash', 'itch',
    'dizzy', 'fatigue', 'weakness', 'infection', 'injury', 'wound',
    'burn', 'fracture', 'allergy', 'allergic', 'breath', 'breathe',
    'blood', 'bleed', 'pressure', 'bp', 'sugar', 'diabetes', 'asthma',
    'heart', 'chest', 'lung', 'liver', 'kidney', 'urine', 'bladder',
    'bone', 'muscle', 'joint', 'swell', 'swelling', 'medicine', 'pill',
    'tablet', 'dose', 'dosage', 'symptom', 'diagnose', 'treatment',
    'therapy', 'doctor', 'hospital', 'clinic', 'pharmacy', 'drug',
    'prescription', 'ill', 'sick', 'disease', 'condition', 'health'
]

# Load resources
vectorizer = None
tfidf_matrix = None
data = None

def load_resources():
    global vectorizer, tfidf_matrix, data
    
    # Load CSV data
    try:
        data = pd.read_csv(DATA_PATH)
        data['Description'] = data['Description'].fillna('')
        data['Patient'] = data['Patient'].fillna('')
        data['Doctor'] = data['Doctor'].fillna('Please consult a doctor for personalized advice')
    except Exception as e:
        print(f"Error loading medical data: {e}")
        data = pd.DataFrame({
            'Description': ['headache', 'stomach pain', 'fever', 'cough'],
            'Patient': ['I have a headache', 'My stomach hurts', 'I have fever', 'I have cough'],
            'Doctor': ['Take paracetamol', 'Try antacids', 'Rest and hydrate', 'Consult a doctor if persistent']
        })
    
    if os.path.exists(VECTORIZER_PATH) and os.path.exists(MATRIX_PATH):
        vectorizer = joblib.load(VECTORIZER_PATH)
        tfidf_matrix = joblib.load(MATRIX_PATH)
    else:
        print("Creating new vectorizer...")
        vectorizer = TfidfVectorizer(stop_words='english')
        combined_text = data['Description'] + " " + data['Patient']
        tfidf_matrix = vectorizer.fit_transform(combined_text)
        joblib.dump(vectorizer, VECTORIZER_PATH)
        joblib.dump(tfidf_matrix, MATRIX_PATH)

load_resources()

def is_medical_query(user_input):
    user_input = user_input.lower()

    if any(re.search(r'\b' + keyword + r'\b', user_input) for keyword in MEDICAL_KEYWORDS):
        return True

    symptom_patterns = [
        r'i have (a|an|the) \w+',
        r'my \w+ hurts',
        r'\w+ pain',
        r'what (is|are) (the )?symptoms of',
        r'what (should|can) i take for',
        r'how to treat \w+',
        r'medicine for \w+'
    ]

    if any(re.search(pattern, user_input) for pattern in symptom_patterns):
        return True

    return False

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '').strip().lower()

        if not user_input:
            return jsonify({'response': "Please enter a valid medical question."})

        if user_input == 'exit':
            return jsonify({'response': "Goodbye! Take care of your health."})

        if not is_medical_query(user_input):
            return jsonify({
                'response': "I specialize only in medical questions. Please ask about symptoms, conditions, or treatments."
            })

        # TF-IDF & similarity
        query_vector = vectorizer.transform([user_input])
        similarity_scores = cosine_similarity(query_vector, tfidf_matrix)
        best_match_idx = similarity_scores.argmax()
        confidence = similarity_scores.max()

        response = data.iloc[best_match_idx]['Doctor']

        serious_conditions = [
            'chest pain', 'difficulty breathing', 'severe pain',
            "can't breathe", 'heart attack', 'stroke', 'bleeding',
            'unconscious', 'broken bone', 'high fever'
        ]
        if any(cond in user_input for cond in serious_conditions):
            response += " ⚠️ This sounds serious. Please seek immediate medical attention!"

        return jsonify({
            'response': response,
            'confidence': f"{confidence:.2f}",
            'follow_up': [
                "Would you like to know about typical treatments?",
                "Want to see possible causes?",
                "When should someone visit a doctor for this?"
            ]
        })

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'response': "I can only answer medical questions. Please describe your health concern."})

@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    return jsonify({
        'examples': [
            "I have a headache",
            "My stomach is hurting",
            "How to treat high fever?",
            "What medicine is good for diarrhea?",
            "Symptoms of COVID-19"
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)
