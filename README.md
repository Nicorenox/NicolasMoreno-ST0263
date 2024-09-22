# sr0263
# Sistema P2P para Compartición de Archivos

Este proyecto es parte del reto 1 de diseño e implementación de un sistema P2P, en el cual cada nodo (o proceso) contiene uno o más microservicios para implementar las funcionalidades de un sistema de compartición de archivos completamente distribuido y descentralizado, similar a la red BitTorrent.

## Objetivo del Proyecto
El objetivo de este proyecto es implementar una versión a escala de una red P2P similar a BitTorrent. Para ello, cada nodo o peer está compuesto por un módulo servidor (PServidor), definido como varios microservicios, y un módulo cliente (PCliente). Estos módulos permiten:

- **Proceso de Join/Leave de un Nodo**: Ilustra cómo un nodo se une y abandona la red.
- **Búsqueda de Archivos en la Red P2P**: Demuestra cómo se buscan archivos distribuidos entre los diferentes nodos.
- **Almacenamiento y Recuperación de Archivos**: Implementación de las operaciones `put(file)` y `get(file)` desde el cliente.
- **Transferencia de Archivos**: Simula el proceso de envío y recepción de archivos, sin realizar una transmisión real, pero mostrando la arquitectura de transferencia.
- **Comunicación entre Peers con gRPC**: Los peers utilizan el protocolo gRPC para la comunicación y permiten la concurrencia de múltiples peticiones.

## Arquitectura General
Este sistema está diseñado bajo un enfoque de microservicios en el que cada nodo ejecuta un servidor que soporta varios servicios. Los clientes pueden conectarse a cualquier nodo para buscar, almacenar o recuperar archivos.

## Funcionalidades Implementadas

### 1. Join/Leave de un Nodo
- Cuando un nodo se une a la red, se registra en un tracker central y se le asigna una lista de nodos disponibles.
- Cuando un nodo deja la red, sus archivos deben ser replicados en otros nodos disponibles para garantizar la redundancia y evitar la pérdida de datos.

### 2. Búsqueda de Archivos
- Los archivos son buscados en toda la red a través del tracker, que mantiene el índice de qué nodos tienen qué archivos.

### 3. Almacenamiento y Recuperación de Archivos
- A través de la operación `put(file)`, un nodo puede enviar un archivo a otros nodos de la red.
- La operación `get(file)` permite descargar un archivo desde un nodo disponible que lo tenga almacenado.

### 4. Transferencia Dummy
- Aunque se implementó la transferencia de archivos reales, el sistema simula la replicación mediante la comunicación gRPC entre nodos.

### 5. Concurrencia de Múltiples Peticiones
- El servidor está diseñado para manejar múltiples peticiones concurrentes, lo que permite que varios nodos interactúen entre sí al mismo tiempo.

## Estructura del Proyecto

- **Dockerfile**: Archivo para crear la imagen de Docker con las configuraciones necesarias para el proyecto.
- **big_file.txt**: Archivo de ejemplo usado para probar la transferencia y almacenamiento de archivos grandes en la red P2P.
- **client.py**: Módulo del cliente que implementa las operaciones `put(file)` y `get(file)` para subir y descargar archivos.
- **docker-compose.yml**: Archivo de configuración para levantar múltiples contenedores Docker (tracker, nodos) de manera sencilla.
- **p2p.proto**: Definición de la API de gRPC utilizada para la comunicación entre nodos en la red P2P.
- **p2p_pb2.py**: Código generado automáticamente por `protoc` a partir de `p2p.proto`, contiene las definiciones de mensajes de gRPC.
- **p2p_pb2_grpc.py**: Código generado automáticamente por `protoc`, contiene las definiciones de los servicios gRPC y sus stubs.
- **requirements.txt**: Lista de dependencias Python necesarias para ejecutar el proyecto (gRPC).
- **server.py**: Módulo del servidor (PServidor) que maneja las operaciones de almacenamiento, búsqueda y recuperación de archivos.
- **tracker.py**: Componente central que actúa como tracker para coordinar la distribución y búsqueda de archivos en la red P2P.

## Diagramas

### 1. Diagrama de Arquitectura General del Sistema P2P
![Diagrama de Arquitectura General](img/diagrama.png)

Este diagrama ilustra la vista general del sistema, mostrando los diferentes componentes y cómo se comunican entre ellos.

**Elementos clave**:
- **Tracker**: Actúa como el coordinador de la red.
- **Nodos/Peers**: Cada uno representa un proceso en la red que puede almacenar o recuperar archivos.
- **Cliente (PCliente)**: Módulo que interactúa con el servidor de nodos para subir/descargar archivos.
- **gRPC**: Protocolo de comunicación entre nodos y con el tracker.

**Funcionamiento**:
- Los nodos se comunican con el tracker para registrarse o abandonar la red.
- Los clientes se conectan a los nodos a través de gRPC para realizar las operaciones `put(file)` y `get(file)`.

### 2. Diagrama de Proceso de Join/Leave
![Diagrama de Join/Leave](img/diagrama-join-leave.png)

Este diagrama describe el flujo de cómo un nodo se une a la red y cómo la abandona.

**Funcionamiento del Join**:
1. El nodo se inicia.
2. Se comunica con el tracker usando gRPC para enviar una solicitud de "join".
3. El tracker registra el nodo en su lista de nodos activos.
4. El tracker devuelve una confirmación y una lista de archivos o nodos relevantes.

**Funcionamiento del Leave**:
1. El nodo notifica al tracker que desea salir de la red.
2. El tracker elimina el nodo de su lista de nodos activos.

### 3. Diagrama de Proceso de Búsqueda de Archivos
![Diagrama de Búsqueda](img/diagrama-busqueda.png)

Este diagrama explica cómo funciona la búsqueda de archivos en la red P2P.

**Funcionamiento**:
- El cliente envía una solicitud al nodo para buscar un archivo (usando `GetFileRequest`).
- Si el archivo no está en ese nodo, el nodo puede consultar otros nodos o el tracker.
- Si se encuentra el archivo, se devuelve una respuesta con la ubicación del archivo.

### 4. Diagrama de Proceso de Almacenamiento de Archivos
![Diagrama de Almacenamiento](img/diagrama-put-file.png)

Este diagrama ilustra el proceso de subir un archivo a la red P2P.

**Funcionamiento**:
1. El cliente envía un archivo al nodo mediante una petición `PutFileRequest`.
2. El nodo almacena el archivo en su sistema.
3. El nodo notifica al tracker sobre el nuevo archivo disponible.
4. El tracker actualiza su lista de archivos disponibles en la red.

### 5. Diagrama de Proceso de Recuperación de Archivos
![Diagrama de Recuperación](img/diagrama-get-file.png)

Este diagrama describe cómo se recupera un archivo de la red.

**Funcionamiento**:
1. El cliente envía una solicitud al nodo para obtener un archivo (`GetFileRequest`).
2. Si el archivo está en el nodo, este lo devuelve al cliente.
3. Si el archivo no está, el nodo puede reenviar la solicitud a otros nodos.
4. El cliente recibe el archivo y lo descarga.

### 6. Diagrama de Transferencia de Archivos
![Diagrama de Transferencia](img/diagrama-transferencia.png)

Este diagrama describe cómo un archivo fluye desde un nodo hasta otro o desde un nodo al cliente. Se puede mostrar el proceso dummy, donde la arquitectura del sistema se estructura para la transferencia, pero no se realiza la transmisión real del archivo.

### 7. Diagrama de Comunicación Concurrente
![Diagrama de Comunicación Concurrente](img/diagrama-concurrencia.png)

Este diagrama ilustra cómo un nodo puede manejar múltiples peticiones concurrentes desde varios clientes o nodos.

**Funcionamiento**:
- Cada nodo actúa como un servidor gRPC que puede recibir múltiples peticiones al mismo tiempo.
- Se ilustra cómo los procesos de `PutFile` y `GetFile` pueden ejecutarse de manera simultánea sin bloquearse, utilizando hilos o asincronía.

## Instalación y Ejecución

Abrir una instancia EC2 en AWS donde se desplegarán los nodos y el tracker mediante Docker. Para ello, se configuró EC2 con varias pautas de seguridad para permitir el tráfico en los puertos necesarios para el tracker y los nodos. Luego se ejecutaron los siguientes comandos:

```bash
sudo apt update -y
sudo apt install python3-pip
sudo apt install docker.io -y
sudo usermod -a -G docker ubuntu
sudo systemctl enable docker
sudo apt install -y git
git clone https://github.com/Nicorenox/sr0263
cd sr0263
/sr0263$ sudo systemctl start docker
/sr0263$ pip install -r requirements.txt --break-system-packages
/sr0263$ sudo docker-compose up --build  # O sudo docker-compose up -d para ejecutarlos en segundo plano
/sr0263$ sudo docker ps  # Verificación de los contenedores en ejecución
/sr0263$ python client.py --uploaod big_file.txt
/sr0263$ python client.py --download big_file.txt prueba1.txt 


