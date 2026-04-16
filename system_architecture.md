# System Architecture Diagram

```plantuml
@startuml
package "User Interface" {
  [Login Page]
  [Symptom Report Page]
}

package "Web Application" {
  [Bottle Web Server]
  [User Management Module]
  [Symptom Processing Module]
  [Chat History Module]
}

package "AI Model" {
  [SymptomModel Class]
  [ML Training Component]
}

User --> "Login Page" : Login/Logout
User --> "Symptom Report Page" : Input Symptoms
"Login Page" --> "User Management Module" : Authenticate User
"Symptom Report Page" --> "Symptom Processing Module" : Send Symptoms
"Symptom Processing Module" --> "SymptomModel Class" : Predict Symptoms
"Symptom Processing Module" --> "Chat History Module" : Save Chat
"SymptomModel Class" --> "ML Training Component" : Train Model
@enduml
