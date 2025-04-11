import joblib
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np # Necesario para convertir lista a formato correcto para predict

# --- 1. Carga del Modelo ---
# Cargamos el modelo entrenado que guardamos en train.py
# Asumimos que el script se ejecuta desde la raíz del proyecto o que el modelo está accesible
model_filename = 'iris_model.joblib'
print(f"Cargando modelo desde {model_filename}...")
try:
    model = joblib.load(model_filename)
    print("Modelo cargado exitosamente.")
    # Obtener los nombres de las características esperadas por el modelo (si es posible/necesario)
    # Esto puede depender de cómo se guardó el modelo o se puede definir explícitamente
    # Para scikit-learn básico, usualmente es el orden de las columnas en el X_train
    expected_features = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)'] # Basado en Iris dataset
except FileNotFoundError:
    print(f"Error: No se encontró el archivo del modelo en {model_filename}. Ejecuta train.py primero.")
    exit()
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    exit()


# --- 2. Creación de la App Flask ---
app = Flask(__name__)

# --- 3. Definición del Endpoint de Predicción ---
@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint para recibir datos de características y devolver predicciones.
    Espera un JSON en el body con la clave "features", que es una lista de números.
    Ejemplo: {"features": [5.1, 3.5, 1.4, 0.2]}
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    if 'features' not in data:
        return jsonify({"error": "Missing 'features' key in JSON body"}), 400

    features = data['features']

    # Validación simple: ¿Número correcto de características?
    if len(features) != len(expected_features):
         return jsonify({"error": f"Expected {len(expected_features)} features, got {len(features)}"}), 400

    try:
        # Convertir la lista a un formato adecuado para scikit-learn (array 2D)
        prediction_input = np.array(features).reshape(1, -1)

        # Realizar la predicción
        prediction = model.predict(prediction_input)

        # Devolver el resultado como JSON
        # Convertimos a int nativo de Python para asegurar serialización JSON
        predicted_class = int(prediction[0])

        # Opcional: Mapear el índice de clase a un nombre legible (si se desea)
        # target_names = ['setosa', 'versicolor', 'virginica'] # Basado en Iris
        # predicted_label = target_names[predicted_class]
        # return jsonify({"prediction": predicted_class, "label": predicted_label})

        return jsonify({"prediction": predicted_class})

    except Exception as e:
        return jsonify({"error": f"Error during prediction: {str(e)}"}), 500


# --- 4. Ejecución de la App ---
if __name__ == '__main__':
    # Ejecutar en el puerto 5000, accesible desde cualquier IP (0.0.0.0)
    # Esto es importante para que sea accesible desde fuera del contenedor Docker más tarde
    print("Iniciando servidor Flask en http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True) # debug=True útil para desarrollo

