import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")

# Encode categorical variables
for col in df.columns:
    if df[col].dtype == 'object':
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

# Separate features and label
X = df.drop("Stress_Detection", axis=1)
y = df["Stress_Detection"]

# Split and train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "stress_model.pkl")

print("✅ Model trained and saved as 'stress_model.pkl'")
