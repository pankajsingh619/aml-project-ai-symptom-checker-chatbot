import gradio as gr
from symptom_checker_backend import SymptomCheckerBackend
import uuid

backend = SymptomCheckerBackend()

EMERGENCY_KEYWORDS = [
    "chest pain", "difficulty breathing", "can't breathe", "cannot breathe",
    "severe bleeding", "unconscious", "stroke", "heart attack",
    "suicide", "overdose", "seizure", "paralysis",
    "severe head injury", "loss of vision", "anaphylaxis"
]

SYMPTOM_ICONS = {
    "fever": "🌡️", "cough": "😷", "headache": "🤕", "fatigue": "😴",
    "nausea": "🤢", "chest pain": "💔", "sore throat": "🦠",
    "shortness of breath": "😤", "dizziness": "🌀", "stomach pain": "📍",
    "rash": "🔴", "runny nose": "🤧"
}

def check_emergency(symptom):
    symptom_lower = symptom.lower()
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in symptom_lower:
            return True, keyword
    return False, None

def get_emergency_response(keyword):
    return f"""
<div class="emergency-banner">
    <div class="emergency-icon">🚨</div>
    <div class="emergency-content">
        <h2>EMERGENCY DETECTED</h2>
        <p>Your symptoms include <strong>"{keyword}"</strong> which may require immediate attention.</p>
        <div class="emergency-actions">
            <div class="action-item">📞</div>
            <div class="action-text">Call 112 or your local emergency number NOW</div>
        </div>
        <div class="emergency-warning">
            This AI cannot provide emergency medical care. Please seek immediate professional help.
        </div>
    </div>
</div>
"""

def analyze_symptoms(symptom, severity, duration, details):
    is_emergency, keyword = check_emergency(symptom)
    if is_emergency:
        return get_emergency_response(keyword)
    
    advice = backend.symptomAdviceMap.get(symptom, "Please consult a healthcare professional.")
    follow_up = backend.followUpQuestions.get(symptom, "")
    
    follow_up_resp = None
    additional = None
    if details:
        follow_up_resp = backend.generate_response(symptom, details)
        additional = backend.follow_up_advice(symptom, details)
    
    severity_lower = severity.lower()
    if severity_lower == "mild":
        banner_class = "low"
        banner_text = "LOW CONCERN"
    elif severity_lower == "severe":
        banner_class = "high"
        banner_text = "HIGH CONCERN"
    else:
        banner_class = "medium"
        banner_text = "MODERATE CONCERN"
    
    icon = SYMPTOM_ICONS.get(symptom, "🏥")
    
    causes = get_possible_causes(symptom)
    
    result = f"""
<div class="results-container">
    <div class="severity-banner {banner_class}">
        <div class="severity-indicator">
            <span class="severity-dot"></span>
            <span class="severity-text">{banner_text}</span>
        </div>
        <p>Based on your {icon} <strong>{symptom}</strong> assessment</p>
    </div>
    
    <div class="cards-grid">
        <div class="result-card causes">
            <div class="card-header">
                <span class="card-icon">🔍</span>
                <h3>Possible Causes</h3>
            </div>
            <div class="card-body">
                {causes}
            </div>
        </div>
        
        <div class="result-card actions">
            <div class="card-header">
                <span class="card-icon">✅</span>
                <h3>Recommended Actions</h3>
            </div>
            <div class="card-body">
                <ul class="action-list">
                    <li>{advice.split('.')[0]}.</li>
                    <li>Monitor your symptoms for changes.</li>
                    <li>Rest and stay well hydrated.</li>
                </ul>
            </div>
        </div>
        
        <div class="result-card warnings">
            <div class="card-header warning">
                <span class="card-icon">⚠️</span>
                <h3>See a Doctor If</h3>
            </div>
            <div class="card-body">
                <ul class="warning-list">
                    <li>Symptoms persist beyond 3 days</li>
                    <li>Condition significantly worsens</li>
                    <li>New symptoms develop</li>
                </ul>
            </div>
        </div>
    </div>
"""
    
    if follow_up_resp:
        result += f"""
    <div class="follow-up-section">
        <div class="card-header">
            <span class="card-icon">💬</span>
            <h3>Follow-up Analysis</h3>
        </div>
        <div class="follow-up-content">
            <p><strong>Your response:</strong> {details}</p>
            <p><strong>Analysis:</strong> {follow_up_resp}</p>
            {f'<p><strong>Additional guidance:</strong> {additional}</p>' if additional else ''}
        </div>
    </div>
"""
    
    result += """
    <div class="next-steps">
        <h4>What would you like to do next?</h4>
        <div class="action-buttons">
            <button class="action-btn" onclick="window.open('https://www.practo.com', '_blank')">📅 Find a Doctor</button>
            <button class="action-btn" onclick="location.reload()">💬 New Assessment</button>
        </div>
    </div>
</div>
"""
    return result

def get_possible_causes(symptom):
    causes_map = {
        "fever": [("65%", "Viral Infection", "Common cold or flu"), ("30%", "Bacterial Infection", "May need antibiotics"), ("15%", "Other Causes", "Heat exhaustion, immune response")],
        "cough": [("50%", "Common Cold", "Viral respiratory infection"), ("25%", "Allergies", "Seasonal or environmental"), ("15%", "GERD", "Acid reflux irritation"), ("10%", "Asthma", "Airway inflammation")],
        "headache": [("40%", "Tension Headache", "Stress or muscle strain"), ("25%", "Dehydration", "Not enough fluids"), ("20%", "Migraine", "Neurological condition"), ("15%", "Sinusitis", "Sinus inflammation")],
        "fatigue": [("45%", "Lack of Sleep", "Insufficient rest"), ("25%", "Stress/Anxiety", "Mental health impact"), ("20%", "Anemia", "Low iron levels"), ("10%", "Thyroid Issues", "Metabolic disorder")],
        "nausea": [("40%", "Gastritis", "Stomach lining inflammation"), ("30%", "Food Poisoning", "Contaminated food/beverages"), ("20%", "Motion Sickness", "Travel-related"), ("10%", "Pregnancy", "Morning sickness")],
        "chest pain": [("35%", "Muscle Strain", "Chest wall pain"), ("25%", "Anxiety/Panic", "Stress-related"), ("20%", "GERD", "Acid reflux"), ("20%", "Cardiac Issue", "Heart-related - seek care")],
        "sore throat": [("50%", "Viral Pharyngitis", "Common cold/flu"), ("25%", "Strep Throat", "Bacterial infection"), ("15%", "Allergies", "Post-nasal drip"), ("10%", "Tonsillitis", "Tonsil inflammation")],
        "shortness of breath": [("30%", "Anxiety", "Hyperventilation"), ("25%", "Asthma", "Airway constriction"), ("20%", "COPD", "Chronic lung disease"), ("25%", "Other Causes", "Various conditions")],
        "dizziness": [("40%", "Dehydration", "Low fluid intake"), ("25%", "Inner Ear Issue", "Vertigo/BPPV"), ("20%", "Low Blood Sugar", "Hypoglycemia"), ("15%", "Medication Effect", "Side effect")],
        "stomach pain": [("35%", "Indigestion", "Digestive discomfort"), ("25%", "Gas/Bloating", "Gastrointestinal gas"), ("20%", "Food Intolerance", "Lactose/gluten sensitivity"), ("20%", "Gastroenteritis", "Stomach flu")],
        "rash": [("40%", "Allergic Reaction", "Contact or food allergy"), ("30%", "Eczema", "Chronic skin condition"), ("20%", "Infection", "Bacterial or viral"), ("10%", "Heat Rash", "Blocked sweat glands")],
        "runny nose": [("55%", "Common Cold", "Viral infection"), ("30%", "Allergies", "Hay fever/allergic rhinitis"), ("15%", "Sinusitis", "Sinus infection")],
    }
    
    causes = causes_map.get(symptom, [("50%", "Various Causes", "Multiple possibilities"), ("30%", "Infection", "Possible bacterial/viral"), ("20%", "Other Factors", "Various triggers")])
    
    html = ""
    for percent, name, desc in causes:
        html += f'''
        <div class="cause-item">
            <span class="cause-percent">{percent}</span>
            <div class="cause-info">
                <strong>{name}</strong>
                <p>{desc}</p>
            </div>
        </div>
        '''
    return html

symptoms_list = list(backend.symptomKeywordsMap.keys())

CUSTOM_CSS = """
:root {
    --primary: #0066CC;
    --primary-light: #3388DD;
    --primary-dark: #004C99;
    --secondary: #00A3B4;
    --success: #00A67E;
    --success-light: #00D4A0;
    --success-bg: rgba(0, 166, 126, 0.1);
    --warning: #F5A623;
    --warning-light: #FFB84D;
    --warning-bg: rgba(245, 166, 35, 0.1);
    --error: #D64242;
    --error-light: #FF6B6B;
    --error-bg: rgba(214, 66, 66, 0.1);
    --bg-main: #F4F7FA;
    --bg-surface: #FFFFFF;
    --text-primary: #1A1F36;
    --text-secondary: #5E6688;
    --text-muted: #9AA3B8;
    --border: #E3E8EF;
    --border-light: #EEF1F5;
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
}

.gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    background: var(--bg-main) !important;
    max-width: 880px !important;
    margin: 0 auto !important;
    padding: 20px !important;
}

.gradio-container footer,
.gradio-container .built-with,
.gradio-container .api-link { display: none !important; }

/* HEADER */
.app-header {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    padding: 28px 32px !important;
    border-radius: var(--radius-lg) !important;
    margin-bottom: 24px !important;
    box-shadow: var(--shadow-lg);
}

.header-top {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
}

.logo-icon { font-size: 48px; }

.header-text h1 {
    font-size: 26px;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.5px;
}

.header-text p {
    opacity: 0.9;
    font-size: 14px;
    margin: 4px 0 0;
}

.trust-bar {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

.trust-item {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.15);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    backdrop-filter: blur(10px);
}

/* INPUT SECTION */
.input-section {
    background: var(--bg-surface);
    border-radius: var(--radius-lg);
    padding: 24px;
    box-shadow: var(--shadow-md);
    margin-bottom: 20px;
}

.section-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 12px;
}

/* SYMPTOM GRID */
.symptom-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin: 16px 0;
}

.symptom-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    padding: 14px 8px;
    background: var(--bg-main);
    border: 2px solid var(--border);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 12px;
    font-weight: 500;
    color: var(--text-secondary);
}

.symptom-btn:hover {
    border-color: var(--primary);
    background: rgba(0, 102, 204, 0.05);
    color: var(--primary);
    transform: translateY(-2px);
}

.symptom-btn.selected {
    border-color: var(--primary);
    background: var(--primary);
    color: white;
}

.symptom-icon { font-size: 24px; }

/* SEVERITY SELECTOR */
.severity-selector { margin: 20px 0; }

.severity-options {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
}

.severity-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 16px 12px;
    background: var(--bg-surface);
    border: 2px solid var(--border);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s;
    text-align: center;
}

.severity-btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
}

.severity-btn.mild { border-color: var(--success); }
.severity-btn.mild.selected { background: var(--success-bg); }
.severity-btn.moderate { border-color: var(--warning); }
.severity-btn.moderate.selected { background: var(--warning-bg); }
.severity-btn.severe { border-color: var(--error); }
.severity-btn.severe.selected { background: var(--error-bg); }

.severity-icon { font-size: 32px; }
.severity-label { font-weight: 600; color: var(--text-primary); font-size: 14px; }
.severity-desc { font-size: 11px; color: var(--text-muted); line-height: 1.3; }

/* INPUT FIELDS */
.gr-text-input input,
.gr-text-input textarea {
    border: 2px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    transition: all 0.2s !important;
    background: var(--bg-surface) !important;
}

.gr-text-input input:focus,
.gr-text-input textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.1) !important;
}

.gr-text-input label {
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    font-size: 14px !important;
    margin-bottom: 8px !important;
}

/* ANALYZE BUTTON */
.analyze-btn {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 16px 32px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    color: white !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    margin-top: 20px !important;
    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3) !important;
}

.analyze-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4) !important;
}

/* RESULTS */
.results-container {
    background: var(--bg-surface);
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-lg);
    animation: slideUp 0.4s ease;
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.severity-banner { padding: 20px 24px; color: white; }
.severity-banner.low { background: linear-gradient(135deg, var(--success) 0%, var(--success-light) 100%); }
.severity-banner.medium { background: linear-gradient(135deg, var(--warning) 0%, var(--warning-light) 100%); }
.severity-banner.high { background: linear-gradient(135deg, var(--error) 0%, var(--error-light) 100%); }

.severity-indicator { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }

.severity-dot {
    width: 10px; height: 10px;
    background: white; border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(1.2); }
}

.severity-text { font-weight: 700; font-size: 14px; letter-spacing: 1px; }

.cards-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    padding: 20px;
}

.result-card {
    background: var(--bg-main);
    border-radius: var(--radius-md);
    padding: 16px;
    border: 1px solid var(--border-light);
}

.result-card.causes { grid-column: span 2; }

.card-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.card-icon { font-size: 20px; }
.card-header h3 { font-size: 14px; font-weight: 600; color: var(--text-primary); margin: 0; }
.card-header.warning h3 { color: var(--error); }

.cause-item {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid var(--border-light);
}

.cause-item:last-child { border-bottom: none; }
.cause-percent { font-weight: 700; color: var(--primary); font-size: 14px; }
.cause-info strong { color: var(--text-primary); display: block; }
.cause-info p { margin: 2px 0 0; font-size: 12px; }

.action-list, .warning-list { list-style: none; padding: 0; margin: 0; }
.action-list li, .warning-list li { padding: 8px 0; padding-left: 20px; position: relative; }
.action-list li::before { content: "✓"; position: absolute; left: 0; color: var(--success); font-weight: bold; }
.warning-list li::before { content: "!"; position: absolute; left: 0; color: var(--error); font-weight: bold; }

/* EMERGENCY */
.emergency-banner {
    background: linear-gradient(135deg, var(--error) 0%, #B71C1C 100%);
    color: white; padding: 24px;
    display: flex; gap: 16px;
    align-items: flex-start;
}

.emergency-icon { font-size: 48px; }
.emergency-content h2 { margin: 0 0 8px; font-size: 18px; }
.emergency-actions { display: flex; align-items: center; gap: 8px; margin: 12px 0; }
.action-item { font-size: 24px; }
.emergency-warning { background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px; font-size: 12px; }

/* FOLLOW-UP */
.follow-up-section {
    background: rgba(0, 102, 204, 0.05);
    padding: 16px 20px;
    border-top: 1px solid var(--border-light);
}

.follow-up-content p { margin: 8px 0; font-size: 13px; }

/* NEXT STEPS */
.next-steps {
    padding: 20px;
    border-top: 1px solid var(--border-light);
    text-align: center;
}

.next-steps h4 { font-size: 14px; color: var(--text-secondary); margin-bottom: 12px; }

.action-buttons { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
.action-btn {
    padding: 10px 20px; border-radius: var(--radius-sm);
    border: 1px solid var(--border); background: var(--bg-surface);
    color: var(--text-secondary); font-size: 13px; font-weight: 500;
    cursor: pointer; transition: all 0.2s;
}
.action-btn:hover { border-color: var(--primary); color: var(--primary); }

/* DISCLAIMER */
.disclaimer-section {
    background: var(--warning-bg);
    border: 1px solid rgba(245, 166, 35, 0.3);
    border-radius: var(--radius-md);
    padding: 16px;
    margin: 20px 0;
    font-size: 12px;
    color: var(--text-secondary);
    line-height: 1.6;
}

.privacy-section {
    background: rgba(0, 102, 204, 0.05);
    border-radius: var(--radius-md);
    padding: 12px 16px;
    font-size: 12px;
    color: var(--text-secondary);
    display: flex; align-items: center; gap: 8px;
}

/* FOOTER */
.app-footer {
    text-align: center; padding: 20px;
    color: var(--text-muted); font-size: 11px;
    border-top: 1px solid var(--border-light);
    margin-top: 24px;
}

/* EXAMPLES */
.gr-examples { display: none !important; }

/* MOBILE */
@media (max-width: 640px) {
    .gradio-container { padding: 12px !important; }
    .app-header { padding: 20px !important; border-radius: var(--radius-md) !important; }
    .header-text h1 { font-size: 20px; }
    .symptom-grid { grid-template-columns: repeat(3, 1fr); gap: 8px; }
    .symptom-btn { padding: 10px 6px; }
    .symptom-icon { font-size: 20px; }
    .severity-options { grid-template-columns: 1fr; }
    .cards-grid { grid-template-columns: 1fr; }
    .result-card.causes { grid-column: span 1; }
    .action-buttons { flex-direction: column; }
    .action-btn { width: 100%; }
}
"""

with gr.Blocks(title="AI Symptom Checker") as demo:
    
    session_id = gr.State(value=str(uuid.uuid4())[:8])
    
    gr.HTML("""
    <div class="app-header">
        <div class="header-top">
            <span class="logo-icon">🏥</span>
            <div class="header-text">
                <h1>AI Symptom Checker</h1>
                <p>Get instant health guidance powered by AI</p>
            </div>
        </div>
        <div class="trust-bar">
            <span class="trust-item">🔒 Private</span>
            <span class="trust-item">⚡ Instant</span>
            <span class="trust-item">📋 Educational</span>
        </div>
    </div>
    """)
    
    gr.HTML("""
    <div class="input-section">
        <div class="section-title">Select Your Symptom:</div>
        <div class="symptom-grid">
            <div class="symptom-btn" onclick="selectSymptom('fever')">
                <span class="symptom-icon">🌡️</span>
                <span>Fever</span>
            </div>
            <div class="symptom-btn" onclick="selectSymptom('cough')">
                <span class="symptom-icon">😷</span>
                <span>Cough</span>
            </div>
            <div class="symptom-btn" onclick="selectSymptom('headache')">
                <span class="symptom-icon">🤕</span>
                <span>Headache</span>
            </div>
            <div class="symptom-btn" onclick="selectSymptom('fatigue')">
                <span class="symptom-icon">😴</span>
                <span>Fatigue</span>
            </div>
            <div class="symptom-btn" onclick="selectSymptom('nausea')">
                <span class="symptom-icon">🤢</span>
                <span>Nausea</span>
            </div>
            <div class="symptom-btn" onclick="selectSymptom('chest pain')">
                <span class="symptom-icon">💔</span>
                <span>Chest Pain</span>
            </div>
            <div class="symptom-btn" onclick="selectSymptom('sore throat')">
                <span class="symptom-icon">🦠</span>
                <span>Sore Throat</span>
            </div>
            <div class="symptom-btn" onclick="selectSymptom('dizziness')">
                <span class="symptom-icon">🌀</span>
                <span>Dizziness</span>
            </div>
            <div class="symptom-btn" onclick="selectSymptom('shortness of breath')">
                <span class="symptom-icon">😤</span>
                <span>Breathing</span>
            </div>
            <div class="symptom-btn" onclick="selectSymptom('stomach pain')">
                <span class="symptom-icon">📍</span>
                <span>Stomach Pain</span>
            </div>
            <div class="symptom-btn" onclick="selectSymptom('rash')">
                <span class="symptom-icon">🔴</span>
                <span>Rash</span>
            </div>
            <div class="symptom-btn" onclick="selectSymptom('runny nose')">
                <span class="symptom-icon">🤧</span>
                <span>Runny Nose</span>
            </div>
        </div>
    </div>
    <script>
    function selectSymptom(symptom) {
        document.querySelectorAll('.symptom-btn').forEach(btn => btn.classList.remove('selected'));
        event.currentTarget.classList.add('selected');
        // Find and update the dropdown
        const dropdown = document.querySelector('select');
        if (dropdown) {
            for (let option of dropdown.options) {
                if (option.text.toLowerCase() === symptom.toLowerCase()) {
                    dropdown.value = option.value;
                    dropdown.dispatchEvent(new Event('change'));
                    break;
                }
            }
        }
    }
    </script>
    """)
    
    with gr.Column():
        symptom_input = gr.Dropdown(
            choices=symptoms_list,
            value="fever",
            label="Selected Symptom",
            visible=True
        )
        
        gr.HTML("""
        <div class="severity-selector">
            <div class="section-title">How Severe Is It?</div>
            <div class="severity-options">
                <div class="severity-btn mild" onclick="selectSeverity('Mild', this)">
                    <span class="severity-icon">🙂</span>
                    <span class="severity-label">Mild</span>
                    <span class="severity-desc">Annoying but manageable</span>
                </div>
                <div class="severity-btn moderate selected" onclick="selectSeverity('Moderate', this)">
                    <span class="severity-icon">😐</span>
                    <span class="severity-label">Moderate</span>
                    <span class="severity-desc">Affecting daily activities</span>
                </div>
                <div class="severity-btn severe" onclick="selectSeverity('Severe', this)">
                    <span class="severity-icon">😣</span>
                    <span class="severity-label">Severe</span>
                    <span class="severity-desc">Hard to ignore</span>
                </div>
            </div>
        </div>
        <script>
        function selectSeverity(value, el) {
            document.querySelectorAll('.severity-btn').forEach(btn => btn.classList.remove('selected'));
            el.classList.add('selected');
        }
        </script>
        """)
        
        severity_input = gr.Radio(
            ["Mild", "Moderate", "Severe"],
            value="Moderate",
            label="Severity",
            visible=False
        )
        
        duration_input = gr.Slider(1, 30, value=3, step=1, label="Duration (days)")
        
        additional_info = gr.Textbox(
            label="Additional Details (optional)",
            placeholder="Any extra symptoms or information...",
            lines=2
        )
        
        analyze_btn = gr.Button("🔍 Analyze Symptoms", elem_classes="analyze-btn")
        
        output_area = gr.HTML()
        
        gr.HTML("""
        <div class="disclaimer-section">
            <strong>⚠️ Medical Disclaimer:</strong> This AI tool provides general health information only and is NOT a substitute for professional medical advice. Always seek the advice of your physician. If experiencing a medical emergency, call emergency services immediately.
        </div>
        """)
        
        gr.HTML("""
        <div class="privacy-section">
            🔒 Your privacy is protected - no data is stored permanently
        </div>
        """)
        
        gr.HTML("""
        <div class="app-footer">
            AI Symptom Checker | For Educational Purposes Only | Not a Medical Device
        </div>
        """)
    
    analyze_btn.click(
        fn=analyze_symptoms,
        inputs=[symptom_input, severity_input, duration_input, additional_info],
        outputs=output_area
    )

if __name__ == "__main__":
    demo.launch(css=CUSTOM_CSS)
