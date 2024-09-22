# Usa una imagen de Python
FROM python:3.9

# Establece el directorio de trabajo
WORKDIR /usr/src/app

# Copia los archivos necesarios al contenedor
COPY . .

# Instala las dependencias necesarias
RUN pip install grpcio grpcio-tools

# Expone el puerto para el tracker
EXPOSE 50052

# Expone los puertos para los nodos
EXPOSE 50001 50002 50003 50004
