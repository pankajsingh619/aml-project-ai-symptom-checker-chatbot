# Sequence Diagram for User Symptom Report Interaction

```plantuml
@startuml
actor User
participant "Login Page" as LoginPage
participant "Web Server" as WebServer
participant "SymptomReportWebApp" as App
participant "SymptomModel" as Model
participant "Chat History" as ChatHistory

User -> LoginPage: Enter username and password
LoginPage -> WebServer: POST /login
WebServer -> App: authenticate user
App --> WebServer: success/failure
WebServer --> LoginPage: redirect or error

User -> App: Access symptom report page
User -> App: Submit symptoms
App -> Model: get_advice(symptoms)
Model --> App: advice
App -> ChatHistory: save chat entry
App --> User: display advice and chat history
@enduml
