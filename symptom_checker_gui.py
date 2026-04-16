import tkinter as tk
from symptom_checker_frontend import SymptomReportForm
from symptom_checker_backend import SymptomCheckerBackend

class SymptomCheckerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Symptom Checker Chatbot")
        self.geometry("700x550")

        self.backend = SymptomCheckerBackend()

        self.frontend = SymptomReportForm(
            self,
            symptomKeywordsMap=self.backend.symptomKeywordsMap,
            symptomAdviceMap=self.backend.symptomAdviceMap,
            followUpQuestions=self.backend.followUpQuestions,
            submit_answer_callback=self.submit_answer
        )
        self.frontend.pack(fill="both", expand=True)

    def submit_answer(self, symptom, answer):
        response = self.backend.generate_response(symptom, answer)
        additional_advice = self.backend.follow_up_advice(symptom, answer)
        return response, additional_advice

if __name__ == "__main__":
    app = SymptomCheckerApp()
    app.mainloop()
