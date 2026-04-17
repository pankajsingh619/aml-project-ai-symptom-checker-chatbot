"""
AI Symptom Checker Chatbot
Professional Healthcare Application
"""

import gradio as gr
from symptom_checker_backend import SymptomCheckerBackend

backend = SymptomCheckerBackend()

# Emergency detection
EMERGENCY_KEYWORDS = [
    "chest pain", "difficulty breathing", "can't breathe", "severe bleeding", 
    "unconscious", "stroke", "heart attack", "seizure", "paralysis"
]

def check_emergency(text):
    text = text.lower()
    for kw in EMERGENCY_KEYWORDS:
        if kw in text:
            return True, kw
    return False, None

def analyze(symptom, severity, duration, details):
    """Main analysis function"""
    is_emerg, kw = check_emergency(symptom)
    if is_emerg:
        return f"""
<div style="background: #FEF2F2; border: 2px solid #DC2626; border-radius: 8px; padding: 24px; margin-bottom: 20px;">
    <div style="display: flex; align-items: flex-start; gap: 16px;">
        <div style="font-size: 32px; color: #DC2626;">⚠️</div>
        <div>
            <h3 style="color: #DC2626; margin: 0 0 8px; font-size: 18px;">Emergency Warning: {kw.title()}</h3>
            <p style="color: #7F1D1D; margin: 0 0 12px;">This symptom may require immediate medical attention.</p>
            <div style="background: #FEE2E2; padding: 12px; border-radius: 6px;">
                <strong>Action Required:</strong> Call 112 or seek emergency care immediately.
            </div>
        </div>
    </div>
</div>
"""
    
    advice = backend.symptomAdviceMap.get(symptom, "Please consult a healthcare professional.")
    follow = backend.followUpQuestions.get(symptom, "")
    
    # Build severity badge
    sev = severity.lower()
    sev_data = {
        "mild": ("Mild", "#059669", "#ECFDF5"),
        "moderate": ("Moderate", "#D97706", "#FFFBEB"), 
        "severe": ("Severe", "#DC2626", "#FEF2F2")
    }.get(sev, ("Moderate", "#D97706", "#FFFBEB"))
    
    # Get causes
    causes = get_causes(symptom)
    
    result = f"""
<div style="background: white; border: 1px solid #E5E7EB; border-radius: 8px; overflow: hidden;">
    <!-- Header -->
    <div style="background: linear-gradient(135deg, #1E3A5F 0%, #234E70 100%); color: white; padding: 20px 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="margin: 0; font-size: 20px;">Health Assessment Report</h2>
                <p style="margin: 4px 0 0; opacity: 0.8; font-size: 14px;">Generated: {symptom.title()}</p>
            </div>
            <div style="background: {sev_data[2]}; color: {sev_data[1]}; padding: 6px 14px; border-radius: 4px; font-size: 13px; font-weight: 600;">
                {sev_data[0]} Severity
            </div>
        </div>
    </div>
    
    <!-- Patient Info -->
    <div style="padding: 20px 24px; border-bottom: 1px solid #E5E7EB;">
        <table style="width: 100%; font-size: 14px;">
            <tr>
                <td style="padding: 8px 0; color: #6B7280;">Symptom</td>
                <td style="padding: 8px 0; font-weight: 500;">{symptom.title()}</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; color: #6B7280;">Duration</td>
                <td style="padding: 8px 0;">{duration} days</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; color: #6B7280;">Severity</td>
                <td style="padding: 8px 0;">{severity}</td>
            </tr>
        </table>
    </div>
    
    <!-- Assessment Sections -->
    <div style="padding: 20px 24px;">
        <!-- Causes -->
        <div style="margin-bottom: 20px;">
            <h4 style="color: #1E3A5F; margin: 0 0 12px; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Possible Causes</h4>
            {causes}
        </div>
        
        <!-- Recommendations -->
        <div style="background: #F0FDF4; border-left: 4px solid #059669; padding: 16px; margin-bottom: 16px;">
            <h4 style="color: #059669; margin: 0 0 8px; font-size: 13px;">Recommended Actions</h4>
            <p style="margin: 0; font-size: 14px; line-height: 1.6;">{advice}</p>
        </div>
        
        <!-- Warnings -->
        <div style="background: #FFFBEB; border-left: 4px solid #D97706; padding: 16px;">
            <h4 style="color: #B45309; margin: 0 0 8px; font-size: 13px;">Seek Medical Care If</h4>
            <ul style="margin: 0; padding-left: 20px; font-size: 14px; color: #1F2937;">
                <li>Symptoms persist beyond 3 days</li>
                <li>Condition significantly worsens</li>
                <li>New symptoms develop</li>
            </ul>
        </div>
    </div>
</div>

<!-- Disclaimer -->
<div style="background: #F3F4F6; border-radius: 6px; padding: 16px; margin-top: 20px; font-size: 12px; color: #6B7280; text-align: center;">
    <strong>Disclaimer:</strong> This assessment is for informational purposes only and does not constitute medical advice. 
    Consult a qualified healthcare provider for proper diagnosis and treatment.
</div>
"""
    return result

def get_causes(symptom):
    """Get possible causes"""
    causes_map = {
        "fever": [("65%", "Viral Infection"), ("25%", "Bacterial Infection"), ("10%", "Other")],
        "cough": [("50%", "Common Cold"), ("30%", "Allergies"), ("20%", "Other")],
        "headache": [("40%", "Tension"), ("30%", "Dehydration"), ("20%", "Migraine")],
        "fatigue": [("45%", "Lack of Rest"), ("30%", "Stress"), ("25%", "Medical Condition")],
        "nausea": [("40%", "Gastritis"), ("35%", "Food Related"), ("25%", "Other")],
        "chest pain": [("35%", "Muscle Strain"), ("30%", "GERD"), ("35%", "Other")],
        "sore throat": [("50%", "Viral"), ("30%", "Bacterial"), ("20%", "Allergies")],
        "dizziness": [("40%", "Dehydration"), ("35%", "Vertigo"), ("25%", "Other")],
        "stomach pain": [("40%", "Indigestion"), ("35%", "Gas"), ("25%", "Infection")],
        "shortness of breath": [("35%", "Anxiety"), ("30%", "Respiratory"), ("35%", "Other")],
        "rash": [("45%", "Allergy"), ("30%", "Skin Condition"), ("25%", "Infection")],
        "runny nose": [("55%", "Common Cold"), ("30%", "Allergies"), ("15%", "Other")],
    }
    c = causes_map.get(symptom, [("50%", "Various Causes")])
    html = '<table style="width: 100%; font-size: 14px;">'
    for pct, name in c:
        html += f'''
        <tr>
            <td style="padding: 10px 0; border-bottom: 1px solid #E5E7EB;">
                <span style="background: #1E3A5F; color: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600; margin-right: 12px;">{pct}</span>
                {name}
            </td>
        </tr>'''
    html += '</table>'
    return html

symptoms_list = list(backend.symptomKeywordsMap.keys())

# Professional Healthcare CSS
CSS = """
* { box-sizing: border-box; }
body { 
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #F8FAFC !important;
}
.gradio-container {
    max-width: 680px !important;
    padding: 24px !important;
}
footer, .built-with { display: none !important; }

/* Header */
.app-header {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 20px;
}
.app-header h1 {
    color: #1E3A5F;
    font-size: 24px;
    font-weight: 600;
    margin: 0;
}
.app-header p {
    color: #64748B;
    font-size: 14px;
    margin: 8px 0 0;
}
.header-meta {
    display: flex;
    gap: 16px;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid #E2E8F0;
    font-size: 12px;
    color: #64748B;
}
.header-meta span {
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Form Card */
.form-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 20px;
}
.form-card h3 {
    color: #1E293B;
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 16px;
}

/* Symptom Pills */
.symptom-wrap {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
}
.symptom-option {
    padding: 12px 8px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    text-align: center;
    cursor: pointer;
    font-size: 12px;
    color: #475569;
    transition: all 0.15s;
}
.symptom-option:hover {
    border-color: #1E3A5F;
    background: #F1F5F9;
}
.symptom-option.selected {
    background: #1E3A5F;
    border-color: #1E3A5F;
    color: white;
}

/* Severity */
.severity-wrap {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 16px 0;
}
.severity-opt {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 14px;
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    color: #475569;
    transition: all 0.15s;
}
.severity-opt:hover { background: #F8FAFC; }
.severity-opt.selected {
    border-color: #1E3A5F;
    background: #1E3A5F;
    color: white;
}

/* Inputs */
label {
    font-weight: 600 !important;
    color: #334155 !important;
    font-size: 13px !important;
    margin-bottom: 6px !important;
}
input[type="text"], input[type="number"], textarea, select {
    border: 1px solid #E2E8F0 !important;
    border-radius: 6px !important;
    padding: 12px !important;
    font-size: 14px !important;
}
input:focus, textarea:focus, select:focus {
    border-color: #1E3A5F !important;
    outline: none !important;
    box-shadow: 0 0 0 2px #1E3A5F20 !important;
}

/* Button */
.submit-btn {
    background: #1E3A5F !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 14px 24px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: white !important;
}
.submit-btn:hover {
    background: #234E70 !important;
}

/* Results */
.results-area {
    margin-top: 20px;
}

/* Disclaimer Footer */
.disclaimer {
    background: #F1F5F9;
    border-radius: 6px;
    padding: 16px;
    margin-top: 20px;
    font-size: 12px;
    color: #64748B;
    text-align: center;
}

/* Mobile */
@media (max-width: 500px) {
    .symptom-wrap { grid-template-columns: repeat(3, 1fr); }
    .severity-wrap { grid-template-columns: 1fr; }
}
"""

with gr.Blocks(css=CSS, title="AI Symptom Checker") as demo:
    
    # Header
    gr.HTML("""
    <div class="app-header">
        <h1>AI Symptom Checker</h1>
        <p>Professional health assessment tool</p>
        <div class="header-meta">
            <span>🔒 Private</span>
            <span>📋 Educational</span>
            <span>⚡ Instant</span>
        </div>
    </div>
    """)
    
    # Symptom Selection
    gr.HTML('<div class="form-card"><h3>Select Symptom</h3><div class="symptom-wrap">')
    for s in symptoms_list:
        gr.HTML(f'<div class="symptom-option" onclick="selectS(\'{s}\', this)">{s.title()}</div>')
    gr.HTML('</div></div>')
    
    gr.HTML("""
    <script>
    function selectS(val, el) {
        document.querySelectorAll('.symptom-option').forEach(o => o.classList.remove('selected'));
        el.classList.add('selected');
        const sel = document.querySelector('select');
        if(sel) { sel.value = val; sel.dispatchEvent(new Event('change')); }
    }
    </script>
    """)
    
    symptom_input = gr.Dropdown(choices=symptoms_list, value="fever", label="Selected Symptom", visible=True)
    
    gr.HTML('<div class="form-card"><h3>Severity Level</h3><div class="severity-wrap"><div class="severity-opt" onclick="setSev(\'Mild\', this)">Mild</div><div class="severity-opt selected" onclick="setSev(\'Moderate\', this)">Moderate</div><div class="severity-opt" onclick="setSev(\'Severe\', this)">Severe</div></div></div>')
    
    gr.HTML("""
    <script>
    function setSev(val, el) {
        document.querySelectorAll('.severity-opt').forEach(o => o.classList.remove('selected'));
        el.classList.add('selected');
    }
    </script>
    """)
    
    severity_input = gr.Radio(choices=["Mild", "Moderate", "Severe"], value="Moderate", visible=False)
    
    gr.HTML('<div class="form-card">')
    duration_input = gr.Slider(1, 30, value=3, step=1, label="Duration (days)")
    additional = gr.Textbox(label="Additional Information", placeholder="Describe any additional symptoms or details...")
    gr.HTML('</div>')
    
    analyze_btn = gr.Button("Generate Assessment", elem_classes="submit-btn")
    
    output = gr.HTML(elem_classes="results-area")
    
    gr.HTML("""
    <div class="disclaimer">
        <strong>Medical Disclaimer:</strong> This tool provides general health information only. 
        It is not a substitute for professional medical advice, diagnosis, or treatment.
    </div>
    """)
    
    analyze_btn.click(fn=analyze, inputs=[symptom_input, severity_input, duration_input, additional], outputs=output)

if __name__ == "__main__":
    demo.launch()