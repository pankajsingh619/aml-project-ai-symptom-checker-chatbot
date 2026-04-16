class SymptomCheckerBackend:
    def __init__(self):
        self.symptomKeywordsMap = {
            "fever": ["fever", "temperature", "hot", "chills"],
            "cough": ["cough", "coughing"],
            "headache": ["headache", "head pain", "migraine"],
            "stomach pain": ["stomach pain", "abdominal pain", "belly ache"],
            "fatigue": ["fatigue", "tired", "exhausted", "weakness"],
            "rash": ["rash", "skin rash", "itchy skin"],
            "shortness of breath": ["shortness of breath", "breathless", "difficulty breathing"],
            "chest pain": ["chest pain", "chest discomfort", "heart pain"],
            "nausea": ["nausea", "queasy", "sick to stomach"],
            "dizziness": ["dizziness", "lightheaded", "faint"],
            "sore throat": ["sore throat", "throat pain", "scratchy throat"],
            "runny nose": ["runny nose", "nasal discharge", "sniffling"],
        }

        self.symptomAdviceMap = {
            "fever": "You may have an infection. Stay hydrated and rest. If fever persists for more than 3 days, see a doctor.",
            "cough": "A cough can be caused by a cold or flu. If it lasts more than 2 weeks or you have difficulty breathing, consult a healthcare professional.",
            "headache": "Headaches can be caused by stress or dehydration. Try to rest and drink water. If severe or persistent, seek medical advice.",
            "stomach pain": "Stomach pain can have many causes. If severe or accompanied by vomiting, see a doctor.",
            "fatigue": "Fatigue can be due to many reasons including lack of sleep or illness. Rest well and monitor your symptoms.",
            "rash": "Skin rashes can be allergic reactions or infections. If rash spreads or is accompanied by fever, seek medical help.",
            "shortness of breath": "Shortness of breath can be serious. If you experience this symptom, seek emergency medical care immediately.",
            "chest pain": "Chest pain can be a sign of a serious condition. Please seek emergency medical care immediately.",
            "nausea": "Nausea can be caused by various conditions. If persistent or severe, consult a healthcare professional.",
            "dizziness": "Dizziness can be caused by dehydration or other issues. Sit or lie down and rest. Seek medical advice if it persists.",
            "sore throat": "Sore throat can be due to infections or allergies. Gargle warm salt water and rest your voice.",
            "runny nose": "Runny nose is often caused by colds or allergies. Stay hydrated and consider antihistamines if allergic.",
        }

        self.followUpQuestions = {
            "fever": "Is your temperature above 101°F (38.3°C)? (yes/no)",
            "cough": "Is your cough dry or productive (with phlegm)?",
            "headache": "Is your headache localized or all over your head?",
            "stomach pain": "Is the pain sharp or dull?",
            "rash": "Is the rash itchy or painful?",
            "nausea": "Are you experiencing vomiting along with nausea? (yes/no)",
            "dizziness": "Do you feel like you might faint? (yes/no)",
            "sore throat": "Do you have difficulty swallowing? (yes/no)",
            "runny nose": "Is your runny nose accompanied by sneezing? (yes/no)",
        }

    def generate_response(self, symptom, answer):
        answer = answer.lower()
        if symptom == "fever":
            if answer in ['yes', 'y']:
                return "A high fever can be serious. Please monitor your temperature and consider seeing a doctor if it persists."
            else:
                return "A mild fever is usually less concerning, but monitor for changes."
        elif symptom == "cough":
            if "dry" in answer:
                return "A dry cough might indicate irritation or viral infection."
            elif "productive" in answer or "phlegm" in answer:
                return "A productive cough with phlegm could suggest infection. Watch for colored mucus."
            else:
                return "Thank you for the information about your cough."
        # Add more specific responses for other symptoms as needed
        else:
            return "Thank you for that information. Let me know if you have any other concerns."

    def follow_up_advice(self, symptom, answer):
        answer = answer.lower()
        if symptom == "fever":
            if answer in ['yes', 'y']:
                return "Since your temperature is above 101°F, please monitor closely and consider seeing a healthcare professional. Also, keep track of any other symptoms like chills or sweating."
            else:
                return "Keep monitoring your temperature and stay hydrated."
        elif symptom == "cough":
            if "dry" in answer:
                return "A dry cough can be irritating; avoid smoke and allergens. If it persists, consider consulting a doctor."
            elif "productive" in answer or "phlegm" in answer:
                return "A productive cough may require medical attention if persistent. Watch for changes in mucus color."
            else:
                return None
        # Add more specific advice for other symptoms as needed
        else:
            return None
