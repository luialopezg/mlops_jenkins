# 1. Usar una imagen base oficial de Python
# Usaremos una versión específica para mayor reproducibilidad
FROM python:3.9-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de dependencias PRIMERO
# Esto aprovecha el caché de Docker: si requirements.txt no cambia,
# no se reinstalan las dependencias en cada build.
COPY requirements.txt .

# 4. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto de los archivos necesarios
# Copiamos la carpeta de scripts y el modelo entrenado
COPY ./scripts /app/scripts
COPY iris_model.joblib .

# 6. Exponer el puerto que usará la aplicación Flask
EXPOSE 5000

# 7. Comando para ejecutar la aplicación cuando se inicie el contenedor
# Usamos la forma exec para que Flask sea el proceso principal (PID 1)
CMD ["python", "scripts/predict.py"]