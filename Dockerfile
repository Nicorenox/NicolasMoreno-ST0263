# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de tu proyecto al contenedor
COPY . .

# Exponer el puerto del tracker y los nodos
EXPOSE 50052 50001 50002 50003 50004

# Comando por defecto para ejecutar el tracker
CMD ["python", "tracker.py"]
