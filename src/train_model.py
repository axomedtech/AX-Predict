from sklearn.tree import DecisionTreeClassifier # type: ignore
import pickle
from load_data import load_ml_data

df = load_ml_data()

X = df[['age', 'fever', 'cough', 'headache', 'fatigue']]
y = df['disease']

model = DecisionTreeClassifier()
model.fit(X, y)

print("Model Training Completed ✔️")

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)