import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
import joblib
import os

# --- 1. Carga y Preparación de Datos ---
print("Cargando datos...")
iris = load_iris()
# Convertimos a DataFrame de Pandas para familiaridad, aunque no estrictamente necesario aquí
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['target'] = iris.target

X = df[iris.feature_names]
y = df['target']

# Dividir datos en entrenamiento y prueba
print("Dividiendo datos...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- 2. Entrenamiento del Modelo ---
print("Entrenando modelo...")
# Usaremos un modelo simple: Regresión Logística
model = LogisticRegression(max_iter=200) # Aumentamos iteraciones para convergencia
model.fit(X_train, y_train)

# --- 3. Evaluación del Modelo ---
print("Evaluando modelo...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión (Accuracy) en el conjunto de prueba: {accuracy:.4f}")

# --- 4. Guardar el Modelo Entrenado ---
# Guardaremos el modelo en la raíz del proyecto por ahora.
# El .gitignore debería evitar que se suba al repositorio.
model_filename = 'iris_model.joblib'
print(f"Guardando modelo en {model_filename}...")
joblib.dump(model, model_filename)

print("Script de entrenamiento completado.")