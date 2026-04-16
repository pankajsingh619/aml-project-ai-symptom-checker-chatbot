import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import font as tkfont

class SymptomReportForm(tk.Frame):
    def __init__(self, master, symptomKeywordsMap, symptomAdviceMap, followUpQuestions, submit_answer_callback):
        super().__init__(master)
        self.master = master
        self.symptomKeywordsMap = symptomKeywordsMap
        self.symptomAdviceMap = symptomAdviceMap
        self.followUpQuestions = followUpQuestions
        self.submit_answer_callback = submit_answer_callback

        self.current_page = 0
        self.pages = []

        self.addedSymptoms = []

        self.create_pages()
        self.show_page(0)

    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.show_page(self.current_page + 1)

    def prev_page(self):
        if self.current_page > 0:
            self.show_page(self.current_page - 1)

    def create_pages(self):
        # Page 0: Patient details page
        page0 = tk.Frame(self)
        self.pages.append(page0)

        tk.Label(page0, text="Patient Details", font=tkfont.Font(size=18, weight="bold")).pack(pady=10)

        form_frame = tk.Frame(page0)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Full Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.nameEntry = tk.Entry(form_frame, width=40)
        self.nameEntry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Age:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.ageEntry = tk.Entry(form_frame, width=40)
        self.ageEntry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Gender:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.genderVar = tk.StringVar(value="Select")
        genderOptions = ["Male", "Female", "Other"]
        self.genderMenu = tk.OptionMenu(form_frame, self.genderVar, *genderOptions)
        self.genderMenu.grid(row=2, column=1, pady=5, sticky='w')

        tk.Label(form_frame, text="Contact Number:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.contactEntry = tk.Entry(form_frame, width=40)
        self.contactEntry.grid(row=3, column=1, pady=5)

        tk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.emailEntry = tk.Entry(form_frame, width=40)
        self.emailEntry.grid(row=4, column=1, pady=5)

        nav_frame = tk.Frame(page0)
        nav_frame.pack(pady=10)
        next_button = tk.Button(nav_frame, text="Next", command=self.next_page)
        next_button.pack()

        # Page 1: Symptom input page
        page1 = tk.Frame(self)
        self.pages.append(page1)

        self.patientNameLabel = tk.Label(page1, text="Patient: ", font=tkfont.Font(size=16, weight="bold"))
        self.patientNameLabel.pack(pady=10)

        instructionLabel = tk.Label(page1, text="Add symptoms from the list, select severity and duration:")
        instructionLabel.pack()

        symptom_frame = tk.Frame(page1)
        symptom_frame.pack(pady=5)

        tk.Label(symptom_frame, text="Symptom:").grid(row=0, column=0, padx=5, pady=5)
        self.symptomVar = tk.StringVar(value=list(self.symptomKeywordsMap.keys())[0])
        symptomOptions = list(self.symptomKeywordsMap.keys())
        self.symptomMenu = tk.OptionMenu(symptom_frame, self.symptomVar, *symptomOptions)
        self.symptomMenu.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(symptom_frame, text="Severity:").grid(row=1, column=0, padx=5, pady=5)
        self.severityVar = tk.StringVar(value="Mild")
        severityOptions = ["Mild", "Moderate", "Severe"]
        self.severityMenu = tk.OptionMenu(symptom_frame, self.severityVar, *severityOptions)
        self.severityMenu.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(symptom_frame, text="Duration (days):").grid(row=2, column=0, padx=5, pady=5)
        self.durationEntry = tk.Entry(symptom_frame, width=10)
        self.durationEntry.grid(row=2, column=1, padx=5, pady=5)

        addSymptomButton = tk.Button(symptom_frame, text="Add Symptom", command=self.add_symptom)
        addSymptomButton.grid(row=3, column=0, columnspan=2, pady=10)

        self.addedSymptomsListbox = tk.Listbox(page1, width=60, height=5)
        self.addedSymptomsListbox.pack(pady=5)

        nav_frame1 = tk.Frame(page1)
        nav_frame1.pack(pady=5)
        backButton = tk.Button(nav_frame1, text="Back", command=self.prev_page)
        backButton.pack(side='left', padx=10)
        nextButton1 = tk.Button(nav_frame1, text="Next", command=self.go_to_advice_page)
        nextButton1.pack(side='right', padx=10)

        # Page 2: Advice and chat page
        page2 = tk.Frame(self)
        self.pages.append(page2)

        adviceLabel = tk.Label(page2, text="Advice:", font=tkfont.Font(size=16, weight="bold"))
        adviceLabel.pack(anchor="w", padx=10, pady=5)

        self.adviceArea = scrolledtext.ScrolledText(page2, width=60, height=10, state='disabled')
        self.adviceArea.pack(pady=5)

        chatLabel = tk.Label(page2, text="Chat History:", font=tkfont.Font(size=16, weight="bold"))
        chatLabel.pack(anchor="w", padx=10, pady=5)

        self.chatHistoryArea = scrolledtext.ScrolledText(page2, width=60, height=10, state='disabled')
        self.chatHistoryArea.pack(pady=5)

        answerFrame = tk.Frame(page2)
        answerFrame.pack(pady=5)

        tk.Label(answerFrame, text="Your Answer:").grid(row=0, column=0, padx=5, pady=5)
        self.answerEntry = tk.Entry(answerFrame, width=40)
        self.answerEntry.grid(row=0, column=1, padx=5, pady=5)

        submitAnswerButton = tk.Button(answerFrame, text="Submit Answer", command=self.submit_answer)
        submitAnswerButton.grid(row=0, column=2, padx=5, pady=5)

        backButton2 = tk.Button(page2, text="Back", command=self.prev_page)
        backButton2.pack(pady=10)

    def go_to_advice_page(self):
        if not self.addedSymptoms:
            messagebox.showwarning("No Symptoms", "Please add at least one symptom first.")
            return
        self.next_page()
        self.provide_advice()

    def on_page_change(self, event=None):
        if self.current_page == 2:
            self.provide_advice()

    def show_page(self, page_index):
        for page in self.pages:
            page.pack_forget()
        self.pages[page_index].pack(fill='both', expand=True)
        self.current_page = page_index
        self.event_generate("<<PageChanged>>")

    def add_symptom(self):
        symptom = self.symptomVar.get()
        severity = self.severityVar.get()
        duration = self.durationEntry.get().strip()
        if not duration.isdigit() or int(duration) <= 0:
            messagebox.showwarning("Input Error", "Please enter a valid duration in days.")
            return
        for s in self.addedSymptoms:
            if s['symptom'] == symptom:
                messagebox.showwarning("Duplicate Symptom", f"{symptom} is already added.")
                return
        symptom_entry = f"{symptom} - Severity: {severity}, Duration: {duration} days"
        self.addedSymptomsListbox.insert(tk.END, symptom_entry)
        self.addedSymptoms.append({
            "symptom": symptom,
            "severity": severity,
            "duration": int(duration)
        })
        self.durationEntry.delete(0, tk.END)

    def provide_advice(self):
        self.adviceArea.config(state='normal')
        self.adviceArea.delete("1.0", tk.END)
        self.chatHistoryArea.config(state='normal')
        self.chatHistoryArea.delete("1.0", tk.END)
        if not self.addedSymptoms:
            self.adviceArea.insert(tk.END, "No symptoms added. Please add symptoms.\n")
            self.adviceArea.config(state='disabled')
            self.chatHistoryArea.config(state='disabled')
            return
        self.awaitingAnswer = False
        self.currentFollowUpSymptom = None
        self.follow_up_queue = []
        for symptom_info in self.addedSymptoms:
            symptom = symptom_info['symptom']
            severity = symptom_info['severity']
            duration = symptom_info['duration']
            advice = self.symptomAdviceMap.get(symptom, "No advice available.")
            self.adviceArea.insert(tk.END,
                f"{symptom.capitalize()} (Severity: {severity}, Duration: {duration} days):\n{advice}\n\n")
            self.add_chat_message(f"Bot: Regarding your {symptom}:\n{advice}")
            follow_up = self.followUpQuestions.get(symptom)
            if follow_up:
                self.follow_up_queue.append((symptom, follow_up))
        self.adviceArea.config(state='disabled')
        self.ask_next_follow_up()

    def add_chat_message(self, message):
        self.chatHistoryArea.config(state='normal')
        self.chatHistoryArea.insert(tk.END, message + "\n")
        self.chatHistoryArea.see(tk.END)
        self.chatHistoryArea.config(state='disabled')

    def ask_next_follow_up(self):
        if self.follow_up_queue:
            self.currentFollowUpSymptom, follow_up = self.follow_up_queue.pop(0)
            self.add_chat_message(f"Bot: {follow_up}")
            self.awaitingAnswer = True
            self.answerEntry.config(state='normal')
            self.answerEntry.focus()
        else:
            self.currentFollowUpSymptom = None
            self.awaitingAnswer = False
            self.answerEntry.config(state='disabled')
            self.add_chat_message("Bot: Thank you for your responses. Is there anything else you'd like to add?")

    def submit_answer(self):
        if not self.awaitingAnswer or not self.currentFollowUpSymptom:
            messagebox.showinfo("Info", "No follow-up question to answer.")
            return
        answer = self.answerEntry.get().strip()
        if not answer:
            messagebox.showwarning("Input Error", "Please enter an answer.")
            return
        self.add_chat_message(f"You: {answer}")
        response = self.generate_response(answer)
        self.add_chat_message(f"Bot: {response}")
        additional_advice = self.follow_up_advice(self.currentFollowUpSymptom, answer)
        if additional_advice:
            self.add_chat_message(f"Bot: {additional_advice}")
        self.answerEntry.delete(0, tk.END)
        self.ask_next_follow_up()
