# AI Symptom Checker Chatbot 🤖🏥

A professional healthcare AI application that helps users understand their symptoms and provides health guidance with follow-up questions.

## 🚀 Live Demo

**Try the live app:** https://huggingface.co/spaces/pankaj092223/ai-symptom-checker-chatbot

## 🎯 Features

- **Emergency Detection** - Identifies critical symptoms requiring immediate attention
- **Visual Symptom Selector** - 12 symptom buttons with icons for easy selection
- **Severity Assessment** - Three-level severity scale (Mild/Moderate/Severe)
- **Possible Causes** - Likelihood-based possible causes with percentages
- **Recommended Actions** - Personalized health advice
- **Warning Signs** - Red flags to watch for
- **Follow-up Questions** - Interactive question flow
- **Professional Healthcare UI** - Clean, medical-grade design
- **Privacy Protected** - No data stored permanently

## 📋 How to Use

1. **Select a Symptom** - Click on any symptom from the grid (fever, cough, headache, etc.)
2. **Choose Severity** - Select how severe the symptom is (Mild, Moderate, or Severe)
3. **Set Duration** - Use the slider to indicate how many days you've had the symptom
4. **Add Details** - Optionally provide additional information
5. **Analyze** - Click "Analyze Symptoms" to get your assessment
6. **View Results** - See possible causes, actions, and warnings

## 🛠️ Tech Stack

- **Frontend:** Gradio (Python)
- **Backend:** Python
- **Deployment:** Hugging Face Spaces

## 📁 Files

```
├── app.py                        # Main Gradio application
├── symptom_checker_backend.py   # Backend logic
├── symptom_checker_gui.py       # Tkinter GUI version
├── symptom_checker_frontend.py # Frontend components
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/pankajsingh619/aml-project-ai-symptom-checker-chatbot.git

# Navigate to folder
cd aml-project-ai-symptom-checker-chatbot

# Install dependencies
pip install gradio

# Run locally
python app.py
```

## ⚠️ Disclaimer

This AI tool provides general health information only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or qualified health provider. If you're experiencing a medical emergency, call your local emergency services immediately.

## 📱 Available Symptoms

| Symptom | Icon | Description |
|---------|------|-------------|
| Fever | 🌡️ | Elevated body temperature |
| Cough | 😷 | Persistent coughing |
| Headache | 🤕 | Head pain or migraine |
| Fatigue | 😴 | Excessive tiredness |
| Nausea | 🤢 | Feeling sick to stomach |
| Chest Pain | 💔 | Pain or discomfort in chest |
| Sore Throat | 🦠 | Throat pain or irritation |
| Dizziness | 🌀 | Lightheadedness |
| Shortness of Breath | 😤 | Breathing difficulty |
| Stomach Pain | 📍 | Abdominal discomfort |
| Rash | 🔴 | Skin rash or irritation |
| Runny Nose | 🤧 | Nasal discharge |

## 🔒 Privacy

- No personal data is stored permanently
- Conversations are not saved after session ends
- No account required to use
- Results are not shared with third parties

## 📝 Code Documentation

### Main Functions

```python
# Check for emergency keywords
check_emergency(symptom) -> (bool, str)

# Analyze symptoms and generate response
analyze_symptoms(symptom, severity, duration, details) -> HTML

# Get possible causes with likelihood
get_possible_causes(symptom) -> HTML
```

### Key Variables

```python
# Emergency keywords that trigger alerts
EMERGENCY_KEYWORDS = ["chest pain", "difficulty breathing", ...]

# Emoji mappings for symptoms
SYMPTOM_ICONS = {"fever": "🌡️", "cough": "😷", ...}

# Healthcare color palette
COLORS = {
    "primary": "#0066CC",    # Deep Blue - Trust
    "secondary": "#00A3B4", # Teal - Healthcare
    "success": "#00A67E",   # Green
    "warning": "#F5A623",    # Amber
    "error": "#D64242"       # Soft red
}
```

## 👨‍💻 Author

**Pankaj Singh**
- GitHub: [@pankajsingh619](https://github.com/pankajsingh619)

## 📄 License

Educational Use Only - Not a Medical Device

---

*Last Updated: April 2026*