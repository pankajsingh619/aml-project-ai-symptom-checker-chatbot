"""
AI Symptom Checker Chatbot
A professional healthcare AI application
"""

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

def check_emergency(symptoms_text):
    """Check for emergency keywords"""
    text = symptoms_text.lower()
    for kw in EMERGENCY_KEYWORDS:
        if kw in text:
            return True, kw
    return False, None

def analyze(symptom, severity, duration, details):
    """Main analysis function"""
    is_emerg, kw = check_emergency(symptom)
    if is_emerg:
        return f"""
<div style="background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%); 
            color: white; padding: 30px; border-radius: 16px; text-align: center;">
    <div style="font-size: 60px; margin-bottom: 16px;">🚨</div>
    <h2 style="margin: 0 0 12px;">EMERGENCY DETECTED</h2>
    <p style="font-size: 18px; margin-bottom: 20px;">"{kw}" requires immediate attention</p>
    <div style="background: rgba(255,255,255,0.2); padding: 16px; border-radius: 12px;">
        <p style="font-size: 20px; font-weight: bold; margin: 0;">📞 Call 112 or Emergency Services NOW</p>
    </div>
    <p style="margin-top: 16px; opacity: 0.9;">Do not wait - seek immediate medical care</p>
</div>
"""
    
    advice = backend.symptomAdviceMap.get(symptom, "Consult a healthcare professional.")
    follow = backend.followUpQuestions.get(symptom, "")
    
    follow_resp = None
    add_advice = None
    if details:
        follow_resp = backend.generate_response(symptom, details)
        add_advice = backend.follow_up_advice(symptom, details)
    
    sev = severity.lower()
    banner = {"mild": ("🟢", "LOW CONCERN", "#059669"), 
              "moderate": ("🟡", "MODERATE CONCERN", "#D97706"),
              "severe": ("🔴", "HIGH CONCERN", "#DC2626")}.get(sev, ("🟡", "CONCERN", "#D97706"))
    
    icon = SYMPTOM_ICONS.get(symptom, "🏥")
    causes = get_causes(symptom)
    
    return f"""
<div style="background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
    <div style="background: linear-gradient(135deg, {banner[2]} 0%, {banner[2]}CC 100%); 
                color: white; padding: 24px; display: flex; align-items: center; gap: 16px;">
        <span style="font-size: 48px;">{banner[0]}</span>
        <div>
            <div style="font-size: 14px; font-weight: 600; letter-spacing: 1px;">{banner[1]}</div>
            <div style="font-size: 20px; font-weight: bold;">{icon} {symptom.title()}</div>
        </div>
    </div>
    
    <div style="padding: 24px;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
            <div style="background: #F3F4F6; padding: 16px; border-radius: 12px; text-align: center;">
                <div style="font-size: 24px; font-weight: bold; color: #0066CC;">{severity}</div>
                <div style="font-size: 12px; color: #6B7280;">Severity</div>
            </div>
            <div style="background: #F3F4F6; padding: 16px; border-radius: 12px; text-align: center;">
                <div style="font-size: 24px; font-weight: bold; color: #0066CC;">{duration} days</div>
                <div style="font-size: 12px; color: #6B7280;">Duration</div>
            </div>
        </div>
        
        <div style="margin-bottom: 20px;">
            <h3 style="color: #0066CC; margin: 0 0 12px; font-size: 16px;">🔍 Possible Causes</h3>
            {causes}
        </div>
        
        <div style="background: #ECFDF5; border-left: 4px solid #059669; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
            <h3 style="color: #059669; margin: 0 0 8px; font-size: 14px;">✅ Recommended Actions</h3>
            <p style="margin: 0; color: #1F2937;">{advice}</p>
        </div>
        
        <div style="background: #FEF3C7; border-left: 4px solid #F59E0B; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
            <h3 style="color: #B45309; margin: 0 0 8px; font-size: 14px;">⚠️ See Doctor If</h3>
            <ul style="margin: 0; padding-left: 20px; color: #1F2937;">
                <li>Symptoms persist beyond 3 days</li>
                <li>Condition significantly worsens</li>
                <li>New symptoms develop</li>
            </ul>
        </div>
"""
    
    if follow_resp:
        result += f"""
        <div style="background: #EFF6FF; border-left: 4px solid #0066CC; padding: 16px; border-radius: 8px;">
            <h3 style="color: #0066CC; margin: 0 0 8px; font-size: 14px;">💬 Follow-up Analysis</h3>
            <p style="margin: 0; color: #1F2937;"><strong>Your response:</strong> {details}</p>
            <p style="margin: 8px 0 0; color: #1F2937;">{follow_resp}</p>
            {f'<p style="margin: 8px 0 0; color: #059669;"><strong>Additional:</strong> {add_advice}</p>' if add_advice else ''}
        </div>
"""
    
    result += """
    </div>
</div>

<div style="background: #FEF3C7; border: 1px solid #FCD34D; border-radius: 12px; padding: 16px; margin-top: 20px; text-align: center;">
    <strong>⚠️ Disclaimer:</strong> This is for educational purposes only. Not medical advice. Consult a doctor for proper diagnosis.
</div>
"""
    return result

def get_causes(symptom):
    """Get possible causes"""
    causes_map = {
        "fever": [("65%", "Viral Infection", "Common cold/flu"), ("30%", "Bacterial Infection", "May need antibiotics")],
        "cough": [("50%", "Common Cold", "Viral infection"), ("25%", "Allergies", "Seasonal triggers")],
        "headache": [("40%", "Tension", "Stress/strain"), ("25%", "Dehydration", "Not enough fluids")],
        "fatigue": [("45%", "Lack of Sleep", "Insufficient rest"), ("25%", "Stress", "Mental strain")],
        "nausea": [("40%", "Gastritis", "Stomach inflammation"), ("30%", "Food Poisoning", "Contaminated food")],
        "chest pain": [("35%", "Muscle Strain", "Physical exertion"), ("25%", "Anxiety", "Stress-related")],
        "sore throat": [("50%", "Viral Pharyngitis", "Common cold"), ("25%", "Strep Throat", "Bacterial")],
        "dizziness": [("40%", "Dehydration", "Low fluids"), ("25%", "Inner Ear", "Vertigo")],
        "stomach pain": [("35%", "Indigestion", "Digestive issues"), ("25%", "Gas", "Bloating")],
        "shortness of breath": [("30%", "Anxiety", "Hyperventilation"), ("25%", "Asthma", "Airway issues")],
        "rash": [("40%", "Allergy", "Contact/food"), ("30%", "Eczema", "Skin condition")],
        "runny nose": [("55%", "Common Cold", "Viral"), ("30%", "Allergies", "Hay fever")],
    }
    c = causes_map.get(symptom, [("50%", "Various Causes", "Multiple factors")])
    html = ""
    for pct, name, desc in c:
        html += f'<div style="display: flex; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px solid #E5E7EB;"><span style="background: #0066CC; color: white; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">{pct}</span><div><strong>{name}</strong><br><span style="font-size: 12px; color: #6B7280;">{desc}</span></div></div>'
    return html

symptoms_list = list(backend.symptomKeywordsMap.keys())

CSS = """
* { box-sizing: border-box; }
body { 
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: linear-gradient(180deg, #E0F2FE 0%, #FFFFFF 50%) !important;
    min-height: 100vh;
}
.gradio-container {
    max-width: 700px !important;
    padding: 20px !important;
}
footer, .built-with { display: none !important; }
.main-header {
    background: linear-gradient(135deg, #0066CC 0%, #0891B2 100%);
    color: white;
    padding: 32px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 10px 40px rgba(0,102,204,0.3);
}
.main-header h1 {
    margin: 0 0 8px;
    font-size: 32px;
    font-weight: 700;
}
.main-header p {
    margin: 0;
    opacity: 0.9;
    font-size: 16px;
}
.trust-tags {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 16px;
    flex-wrap: wrap;
}
.trust-tag {
    background: rgba(255,255,255,0.2);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
}
.card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.symptom-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
}
.symptom-pill {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 12px 8px;
    background: #F9FAFB;
    border: 2px solid #E5E7EB;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 11px;
}
.symptom-pill:hover {
    border-color: #0066CC;
    background: #EFF6FF;
    transform: translateY(-2px);
}
.symptom-pill.active {
    border-color: #0066CC;
    background: #0066CC;
    color: white;
}
.symptom-pill span:first-child {
    font-size: 24px;
    margin-bottom: 4px;
}
.severity-btns {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 16px 0;
}
.sev-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px;
    background: white;
    border: 2px solid #E5E7EB;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
}
.sev-btn:hover { transform: translateY(-2px); }
.sev-btn.selected { border-width: 3px; }
.sev-btn.mild.selected { border-color: #059669; background: #ECFDF5; }
.sev-btn.moderate.selected { border-color: #D97706; background: #FFFBEB; }
.sev-btn.severe.selected { border-color: #DC2626; background: #FEF2F2; }
.sev-btn span:first-child { font-size: 28px; }
.sev-btn strong { font-size: 14px; margin: 4px 0; }
.sev-btn small { font-size: 10px; color: #6B7280; }
.analyze-btn {
    background: linear-gradient(135deg, #0066CC 0%, #0891B2 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 16px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    color: white !important;
    width: 100%;
    margin-top: 16px;
    box-shadow: 0 4px 15px rgba(0,102,204,0.4) !important;
}
.analyze-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,102,204,0.5) !important;
}
.input-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}
.input-wrap label {
    font-weight: 600 !important;
    color: #1F2937 !important;
    font-size: 14px !important;
    margin-bottom: 8px !important;
}
.gr-input input, .gr-text textarea {
    border: 2px solid #E5E7EB !important;
    border-radius: 10px !important;
    padding: 12px !important;
}
.gr-input input:focus, .gr-text textarea:focus {
    border-color: #0066CC !important;
    box-shadow: 0 0 0 3px rgba(0,102,204,0.1) !important;
}
@media (max-width: 600px) {
    .symptom-grid { grid-template-columns: repeat(3, 1fr); }
    .severity-btns { grid-template-columns: 1fr; }
    .input-row { grid-template-columns: 1fr; }
    .main-header h1 { font-size: 24px; }
}
"""

with gr.Blocks(css=CSS, title="AI Symptom Checker") as demo:
    gr.HTML("""
    <div class="main-header">
        <h1>🏥 AI Symptom Checker</h1>
        <p>Get instant health guidance powered by AI</p>
        <div class="trust-tags">
            <span class="trust-tag">🔒 Private</span>
            <span class="trust-tag">⚡ Instant</span>
            <span class="trust-tag">📋 Educational</span>
        </div>
    </div>
    """)
    
    gr.HTML('''
    <div class="card">
        <h3 style="margin: 0 0 16px; color: #1F2937;">Select Your Symptom:</h3>
        <div class="symptom-grid">
            <div class="symptom-pill" onclick="selectSymptom(this, \'fever\')"><span>🌡️</span><span>Fever</span></div>
            <div class="symptom-pill" onclick="selectSymptom(this, \'cough\')"><span>😷</span><span>Cough</span></div>
            <div class="symptom-pill" onclick="selectSymptom(this, \'headache\')"><span>🤕</span><span>Headache</span></div>
            <div class="symptom-pill" onclick="selectSymptom(this, \'fatigue\')"><span>😴</span><span>Fatigue</span></div>
            <div class="symptom-pill" onclick="selectSymptom(this, \'nausea\')"><span>🤢</span><span>Nausea</span></div>
            <div class="symptom-pill" onclick="selectSymptom(this, \'chest pain\')"><span>💔</span><span>Chest Pain</span></div>
            <div class="symptom-pill" onclick="selectSymptom(this, \'sore throat\')"><span>🦠</span><span>Sore Throat</span></div>
            <div class="symptom-pill" onclick="selectSymptom(this, \'dizziness\')"><span>🌀</span><span>Dizziness</span></div>
            <div class="symptom-pill" onclick="selectSymptom(this, \'shortness of breath\')"><span>😤</span><span>Breathing</span></div>
            <div class="symptom-pill" onclick="selectSymptom(this, \'stomach pain\')"><span>📍</span><span>Stomach Pain</span></div>
            <div class="symptom-pill" onclick="selectSymptom(this, \'rash\')"><span>🔴</span><span>Rash</span></div>
            <div class="symptom-pill" onclick="selectSymptom(this, \'runny nose\')"><span>🤧</span><span>Runny Nose</span></div>
        </div>
    </div>
    <script>
    function selectSymptom(el, val) {
        document.querySelectorAll('.symptom-pill').forEach(b => b.classList.remove('active'));
        el.classList.add('active');
        const sel = document.querySelector('select');
        if(sel) { sel.value = val; sel.dispatchEvent(new Event('change')); }
    }
    </script>
    ''')
    
    symptom_input = gr.Dropdown(choices=symptoms_list, value="fever", label="Selected Symptom", visible=True)
    
    gr.HTML('''
    <div class="card">
        <h3 style="margin: 0 0 12px; color: #1F2937;">How Severe Is It?</h3>
        <div class="severity-btns">
            <div class="sev-btn mild" onclick="setSeverity(\'Mild\', this)"><span>🙂</span><strong>Mild</strong><small>Manageable</small></div>
            <div class="sev-btn moderate selected" onclick="setSeverity(\'Moderate\', this)"><span>😐</span><strong>Moderate</strong><small>Daily affected</small></div>
            <div class="sev-btn severe" onclick="setSeverity(\'Severe\', this)"><span>😣</span><strong>Severe</strong><small>Hard to ignore</small></div>
        </div>
    </div>
    <script>
    function setSeverity(val, el) {
        document.querySelectorAll('.sev-btn').forEach(b => b.classList.remove('selected'));
        el.classList.add('selected');
    }
    </script>
    ''')
    
    severity_input = gr.Radio(choices=["Mild", "Moderate", "Severe"], value="Moderate", label="Severity", visible=False)
    
    gr.HTML('<div class="card">')
    duration_input = gr.Slider(1, 30, value=3, step=1, label="Duration (days)")
    additional_info = gr.Textbox(label="Additional Details (optional)", placeholder="Any extra symptoms or information...", lines=2)
    gr.HTML('</div>')
    
    analyze_btn = gr.Button("🔍 Analyze Symptoms", elem_classes="analyze-btn")
    
    output_area = gr.HTML()
    
    gr.HTML("""
    <div style="background: #FEF3C7; border: 1px solid #FCD34D; border-radius: 12px; padding: 16px; margin-top: 16px; text-align: center; font-size: 13px;">
        <strong>⚠️ Medical Disclaimer:</strong> This AI provides general health info only. Not a substitute for professional medical advice.
    </div>
    """)
    
    analyze_btn.click(fn=analyze, inputs=[symptom_input, severity_input, duration_input, additional_info], outputs=output_area)

if __name__ == "__main__":
    demo.launch()
