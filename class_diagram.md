# Class Diagram

```plantuml
@startuml
class SymptomModel {
  - label_encoder: LabelEncoder
  - scaler: StandardScaler
  - lda: LDA
  - classifier: RandomForestClassifier
  - is_trained: bool
  + train(X, y)
  + predict(X)
  + evaluate(X, y)
}

class SymptomReportWebApp {
  - users: dict
  - chat_history: dict
  + load_users()
  + save_users()
  + load_chat_history(username)
  + save_chat_history(username, chat_history)
  + get_advice(input_text)
  + check_login()
}

class User {
  - username: str
  - password_hash: str
  + login()
  + logout()
}

SymptomReportWebApp "1" *-- "*" User : manages
SymptomReportWebApp ..> SymptomModel : uses
@enduml
