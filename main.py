import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from flask import Flask, render_template, request, jsonify
import requests
import json
# Initialize Flask app
app = Flask(__name__)

# Replace disease names with numeric labels
disease_mapping = {
    'Fungal infection': 0, 'Allergy': 1, 'GERD': 2, 'Chronic cholestasis': 3, 'Drug Reaction': 4,
    'Peptic ulcer diseae': 5, 'AIDS': 6, 'Diabetes ': 7, 'Gastroenteritis': 8, 'Bronchial Asthma': 9,
    'Hypertension ': 10, 'Migraine': 11, 'Cervical spondylosis': 12, 'Paralysis (brain hemorrhage)': 13,
    'Jaundice': 14, 'Malaria': 15, 'Chicken pox': 16, 'Dengue': 17, 'Typhoid': 18, 'hepatitis A': 19,
    'Hepatitis B': 20, 'Hepatitis C': 21, 'Hepatitis D': 22, 'Hepatitis E': 23, 'Alcoholic hepatitis': 24,
    'Tuberculosis': 25, 'Common Cold': 26, 'Pneumonia': 27, 'Dimorphic hemmorhoids(piles)': 28,
    'Heart attack': 29, 'Varicose veins': 30, 'Hypothyroidism': 31, 'Hyperthyroidism': 32, 'Hypoglycemia': 33,
    'Osteoarthristis': 34, 'Arthritis': 35, '(vertigo) Paroymsal  Positional Vertigo': 36, 'Acne': 37,
    'Urinary tract infection': 38, 'Psoriasis': 39, 'Impetigo': 40
}

# Load and preprocess training data
df = pd.read_csv("Training.csv")
df.replace({'prognosis': disease_mapping}, inplace=True)

# Extract features (symptoms) and target (disease)
symptoms = ['back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
            'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
            'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
            'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
            'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
            'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
            'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
            'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
            'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
            'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
            'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of_urine',
            'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
            'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
            'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria',
            'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances',
            'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
            'distention_of_abdomen', 'history_of_alcohol_consumption', 'blood_in_sputum', 'prominent_veins_on_calf',
            'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
            'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
            'yellow_crust_ooze']
symptoms = [symptom for symptom in symptoms if symptom in df.columns]
X = df[symptoms]
y = df['prognosis']

# Train the Decision Tree model
clf = DecisionTreeClassifier()
clf.fit(X, y)

@app.route('/')
def home():
    return render_template('index.html', symptoms=symptoms)

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    input_data = request.form
    symptom_values = [1 if input_data.get(symptom) == 'on' else 0 for symptom in symptoms]
    prediction = clf.predict([symptom_values])[0]
    disease_name = next(key for key, value in disease_mapping.items() if value == prediction)
    
    

    # Ensure the API key is set in environment variables
    # Ensure the API key is set in environment variables
    API_KEY = "YOUR_API_KEY"
    if not API_KEY:
        raise ValueError("COHERE_API_KEY environment variable is not set.")

    url = "https://api.cohere.ai/v1/generate"
    # Construct the prompt
    prompt = f"""Provide a comprehensive response for the health issue: {disease_name}. Include effective home remedies using simple, natural ingredients; commonly used medications (over-the-counter or prescribed) with general usage guidance; key precautions to manage or prevent the condition; and clear indicators of when to seek professional medical advice. Ensure the information is concise, easy to understand, and practical."""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # Cohere payload structure
    data = {
        "model": "command-xlarge-nightly",  # Use your desired Cohere model
        "prompt": prompt,
        "max_tokens": 300,  # Adjust token count as needed
        "temperature": 0.7,  # Controls creativity; lower values are more deterministic
    }

    try:
        # Send the request to Cohere's API
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            data= result.get("generations", [{}])[0].get("text", "No response text")
            print(data)
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


    return render_template('index.html', symptoms=symptoms, prediction=disease_name,remedy=data)

if __name__ == '__main__':
    app.run(debug=True)
