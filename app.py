"""
AI Symptom Checker - Flask Web App
Professional Healthcare Application for Render Deployment
"""

from flask import Flask, render_template_string
from symptom_checker_backend import SymptomCheckerBackend

app = Flask(__name__)
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

@app.route('/')
def home():
    symptoms_list = list(backend.symptomKeywordsMap.keys())
    
    HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Symptom Checker</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #F8FAFC; color: #1E293B; line-height: 1.6; }
        .container { max-width: 680px; margin: 0 auto; padding: 24px 16px; }
        
        /* Header */
        .header { background: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 24px; margin-bottom: 20px; }
        .header h1 { color: #1E3A5F; font-size: 24px; font-weight: 600; margin-bottom: 8px; }
        .header p { color: #64748B; font-size: 14px; }
        .header-meta { display: flex; gap: 16px; margin-top: 16px; padding-top: 16px; border-top: 1px solid #E2E8F0; font-size: 12px; color: #64748B; }
        
        /* Card */
        .card { background: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 24px; margin-bottom: 20px; }
        .card h3 { color: #1E293B; font-size: 16px; font-weight: 600; margin-bottom: 16px; }
        
        /* Grid */
        .symptom-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        .symptom-btn { padding: 12px 8px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; text-align: center; cursor: pointer; font-size: 13px; color: #475569; transition: all 0.15s; }
        .symptom-btn:hover { border-color: #1E3A5F; background: #F1F5F9; }
        .symptom-btn.selected { background: #1E3A5F; border-color: #1E3A5F; color: white; }
        
        /* Severity */
        .severity-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 16px 0; }
        .sev-btn { padding: 14px; background: white; border: 1px solid #E2E8F0; border-radius: 6px; text-align: center; cursor: pointer; font-size: 14px; font-weight: 500; color: #475569; }
        .sev-btn:hover { background: #F8FAFC; }
        .sev-btn.selected { border-color: #1E3A5F; background: #1E3A5F; color: white; }
        
        /* Form */
        .form-group { margin-bottom: 16px; }
        .form-group label { display: block; font-weight: 600; color: #334155; font-size: 13px; margin-bottom: 6px; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 12px; border: 1px solid #E2E8F0; border-radius: 6px; font-size: 14px; }
        .form-group input:focus, .form-group textarea:focus { outline: none; border-color: #1E3A5F; }
        .form-group textarea { min-height: 80px; resize: vertical; }
        
        /* Button */
        .submit-btn { width: 100%; padding: 14px; background: #1E3A5F; border: none; border-radius: 6px; font-size: 15px; font-weight: 600; color: white; cursor: pointer; }
        .submit-btn:hover { background: #234E70; }
        
        /* Results */
        .results { margin-top: 24px; }
        .result-card { background: white; border: 1px solid #E5E7EB; border-radius: 8px; overflow: hidden; }
        .result-header { background: linear-gradient(135deg, #1E3A5F 0%, #234E70 100%); color: white; padding: 20px 24px; display: flex; justify-content: space-between; align-items: center; }
        .result-header h2 { font-size: 20px; font-weight: 600; }
        .severity-badge { padding: 6px 14px; border-radius: 4px; font-size: 13px; font-weight: 600; }
        .result-body { padding: 20px 24px; }
        .result-row { display: flex; padding: 12px 0; border-bottom: 1px solid #E5E7EB; }
        .result-row:last-child { border-bottom: none; }
        .result-label { color: #6B7280; width: 100px; }
        .result-value { font-weight: 500; }
        
        .cause-table { width: 100%; font-size: 14px; }
        .cause-row { padding: 12px 0; border-bottom: 1px solid #E5E7EB; }
        .cause-pct { background: #1E3A5F; color: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600; margin-right: 12px; }
        
        .recommend { background: #F0FDF4; border-left: 4px solid #059669; padding: 16px; margin: 16px 0; }
        .recommend h4 { color: #059669; font-size: 13px; margin-bottom: 8px; }
        
        .warning { background: #FFFBEB; border-left: 4px solid #D97706; padding: 16px; }
        .warning h4 { color: #B45309; font-size: 13px; margin-bottom: 8px; }
        
        .disclaimer { background: #F1F5F9; border-radius: 6px; padding: 16px; margin-top: 20px; font-size: 12px; color: #64748B; text-align: center; }
        
        @media (max-width: 500px) {
            .symptom-grid { grid-template-columns: repeat(2, 1fr); }
            .severity-grid { grid-template-columns: 1fr; }
            .result-header { flex-direction: column; align-items: flex-start; gap: 12px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI Symptom Checker</h1>
            <p>Professional health assessment tool</p>
            <div class="header-meta">
                <span>🔒 Private</span>
                <span>📋 Educational</span>
                <span>⚡ Instant</span>
            </div>
        </div>
        
        <form method="POST" action="/analyze">
            <div class="card">
                <h3>Select Symptom</h3>
                <div class="symptom-grid">'''
    
    for s in symptoms_list:
        HTML += f'<div class="symptom-btn" onclick="selectSymptom(this, \'{s}\')">{s.title()}</div>'
    
    HTML += '''</div>
            </div>
            
            <div class="card">
                <h3>Severity Level</h3>
                <div class="severity-grid">
                    <div class="sev-btn" onclick="selectSeverity(this, 'Mild')">Mild</div>
                    <div class="sev-btn selected" onclick="selectSeverity(this, 'Moderate')">Moderate</div>
                    <div class="sev-btn" onclick="selectSeverity(this, 'Severe')">Severe</div>
                </div>
            </div>
            
            <div class="card">
                <div class="form-group">
                    <label>Selected Symptom</label>
                    <select name="symptom" id="symptom">
                        <option value="fever">Fever</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Duration (days)</label>
                    <input type="number" name="duration" value="3" min="1" max="30">
                </div>
                
                <div class="form-group">
                    <label>Additional Details (optional)</label>
                    <textarea name="details" placeholder="Describe any additional symptoms or details..."></textarea>
                </div>
                
                <input type="hidden" name="severity" id="severity" value="Moderate">
                <button type="submit" class="submit-btn">Generate Assessment</button>
            </div>
        </form>
        
        <div class="disclaimer">
            <strong>Medical Disclaimer:</strong> This tool provides general health information only. 
            It is not a substitute for professional medical advice, diagnosis, or treatment.
        </div>
    </div>
    
    <script>
    function selectSymptom(el, val) {
        document.querySelectorAll('.symptom-btn').forEach(b => b.classList.remove('selected'));
        el.classList.add('selected');
        document.getElementById('symptom').value = val;
    }
    function selectSeverity(el, val) {
        document.querySelectorAll('.sev-btn').forEach(b => b.classList.remove('selected'));
        el.classList.add('selected');
        document.getElementById('severity').value = val;
    }
    </script>
</body>
</html>'''
    return render_template_string(HTML)

@app.route('/analyze', methods=['POST'])
def analyze():
    symptom = request.form.get('symptom', 'fever')
    severity = request.form.get('severity', 'Moderate')
    duration = request.form.get('duration', '3')
    details = request.form.get('details', '')
    
    is_emerg, kw = check_emergency(symptom)
    if is_emerg:
        return f'''
        <div class="result-card">
            <div class="result-header" style="background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);">
                <h2>⚠️ Emergency Warning</h2>
            </div>
            <div class="result-body">
                <p style="color: #DC2626; font-size: 18px; margin-bottom: 12px;"><strong>{kw.title()}</strong> may require immediate medical attention.</p>
                <div style="background: #FEE2E2; padding: 16px; border-radius: 6px;">
                    <strong>Action Required:</strong> Call 112 or seek emergency care immediately.
                </div>
            </div>
        </div>'''
    
    advice = backend.symptomAdviceMap.get(symptom, "Please consult a healthcare professional.")
    
    # Severity colors
    sev_data = {"mild": ("Mild", "#059669", "#ECFDF5"), "moderate": ("Moderate", "#D97706", "#FFFBEB"), "severe": ("Severe", "#DC2626", "#FEF2F2")}
    sev = sev_data.get(severity.lower(), sev_data["moderate"])
    
    # Causes
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
    causes = causes_map.get(symptom, [("50%", "Various Causes")])
    
    causes_html = '<table class="cause-table">'
    for pct, name in causes:
        causes_html += f'<tr><td class="cause-row"><span class="cause-pct">{pct}</span>{name}</td></tr>'
    causes_html += '</table>'
    
    return f'''
    <div class="results">
        <div class="result-card">
            <div class="result-header">
                <h2>Health Assessment Report</h2>
                <div class="severity-badge" style="background: {sev[2]}; color: {sev[1]};">{sev[0]}</div>
            </div>
            <div class="result-body">
                <div class="result-row">
                    <span class="result-label">Symptom</span>
                    <span class="result-value">{symptom.title()}</span>
                </div>
                <div class="result-row">
                    <span class="result-label">Duration</span>
                    <span class="result-value">{duration} days</span>
                </div>
                <div class="result-row">
                    <span class="result-label">Severity</span>
                    <span class="result-value">{severity}</span>
                </div>
            </div>
        </div>
        
        <div class="result-card">
            <div class="result-body" style="padding-top: 0;">
                <h4 style="color: #1E3A5F; margin: 0 0 12px; font-size: 14px; text-transform: uppercase;">Possible Causes</h4>
                {causes_html}
                
                <div class="recommend">
                    <h4>Recommended Actions</h4>
                    <p>{advice}</p>
                </div>
                
                <div class="warning">
                    <h4>Seek Medical Care If</h4>
                    <ul style="margin: 0; padding-left: 20px;">
                        <li>Symptoms persist beyond 3 days</li>
                        <li>Condition significantly worsens</li>
                        <li>New symptoms develop</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="disclaimer">
            <strong>Disclaimer:</strong> This assessment is for informational purposes only and does not constitute medical advice.
        </div>
    </div>'''

from flask import request

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=True)