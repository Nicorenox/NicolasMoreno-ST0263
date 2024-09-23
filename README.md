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

### 4. Transferencia
- Aunque se implementó la transferencia de archivos reales, el sistema simula la replicación mediante la comunicación gRPC entre nodos.

### 5. Concurrencia de Múltiples Peticiones
- El servidor está diseñado para manejar múltiples peticiones concurrentes, lo que permite que varios nodos interactúen entre sí al mismo tiempo.

### 6. Algoritmo de Replicación Implementado:

Cuando un archivo necesita ser replicado, el tracker identifica los nodos disponibles en la red.  
El archivo se replica en uno o más nodos, siempre y cuando estos nodos no lo posean ya.

Para replicar un archivo:

1. El tracker identifica los nodos donde el archivo ya está almacenado.
2. Se seleccionan nodos adicionales para la replicación del archivo.
3. El archivo se recupera del nodo original utilizando la operación `GetFile` vía gRPC.
4. Luego, el archivo es transferido a otros nodos utilizando la operación `PutFile`, asegurando que el archivo esté replicado en múltiples ubicaciones.

### Explicación del Código (Replicación Automática):

El método `ReplicateFiles` verifica si un archivo está presente en un nodo y luego lo replica en otros nodos disponibles de la siguiente manera:

1. Primero, se verifica si el archivo ya está replicado en algún nodo dentro de la red. Si no, el archivo es recuperado mediante `GetFile`.
2. A continuación, el archivo es replicado en otros nodos utilizando `PutFile`, asegurando que no se replique en el nodo de origen.
3. Cada vez que el archivo se replica exitosamente, se muestra un mensaje de confirmación (`File {filename} replicated to {target_node}`).

Este algoritmo garantiza que, si un nodo se desconecta, los archivos almacenados en él puedan ser replicados en otros nodos activos, manteniendo la disponibilidad del archivo en la red.

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
![Cleinte](https://github.com/user-attachments/assets/7901bb81-d2dd-483a-addc-8924888a9041)

Este diagrama ilustra la vista general del sistema, mostrando los diferentes componentes y cómo se comunican entre ellos.

**Elementos clave**:
- **Tracker**: Actúa como el coordinador de la red.
- **Nodos/Peers**: Cada uno representa un proceso en la red que puede almacenar o recuperar archivos.
- **Cliente (PCliente)**: Módulo que interactúa con el servidor de nodos para subir/descargar archivos.
- **gRPC**: Protocolo de comunicación entre nodos y con el tracker.

**Funcionamiento**:
- Los nodos se comunican con el tracker para registrarse o abandonar la red.
- Los clientes se conectan a los nodos a través de gRPC para realizar las operaciones `put(file)` y `get(file)`.

### 2. Diagramas de Proceso de Join/Leave

![Leave-Join](https://github.com/user-attachments/assets/71c26662-6dd2-4d98-941a-e044435951b4)
![Funcionameinto-Tracker-y-comunicacion](https://github.com/user-attachments/assets/754a1870-2c89-488a-ac7f-4cc3990705bd)

Estos diagramas describen el flujo de cómo un nodo se une a la red y cómo la abandona.

**Funcionamiento del Join**:
- El nodo se inicia.
- Se comunica con el tracker usando gRPC para enviar una solicitud de "join".
- El tracker registra el nodo en su lista de nodos activos.
- El tracker devuelve una confirmación y una lista de archivos o nodos relevantes.

**Funcionamiento del Leave**:
- El nodo notifica al tracker que desea salir de la red.
- El tracker elimina el nodo de su lista de nodos activos.
![leave-network](https://github.com/user-attachments/assets/169267b6-f55d-461b-988c-eb7cf799bc18)


### 3. Diagrama de replicación de archivos
Este diagrama muesta cómo se replica un archivo cuando un nodo se desconecta, asegurando que el archivo no se pierda.
![Replicacion](https://github.com/user-attachments/assets/16347125-68a9-43c3-bb42-178aac8124fe)

**Funcionamiento**:
- Desconexión de nodo: El nodo envía una solicitud LeaveNetwork al tracker.
- El tracker revisa qué archivos estaban en el nodo desconectado.
- El tracker selecciona un nuevo nodo y usa gRPC para replicar el archivo.


## Instalación y Ejecución

Abrir una instancia EC2 en AWS donde se desplegarán los nodos y el tracker mediante Docker. Para ello, se configuró EC2 con varias pautas de seguridad para permitir el tráfico en los puertos necesarios para el tracker y los nodos. Luego se ejecutaron los siguientes comandos:

```bash
sudo apt update -y
sudo apt install python3-pip
sudo apt install docker.io -y
sudo usermod -a -G docker ubuntu
sudo systemctl enable docker
sudo apt install -y git
git clone https://github.com/Nicorenox/NicolasMoreno-ST0263
cd sr0263
/sr0263$ sudo systemctl start docker
/sr0263$ pip install -r requirements.txt --break-system-packages
/sr0263$ sudo docker-compose up --build  # O sudo docker-compose up -d para ejecutarlos en segundo plano
/sr0263$ sudo docker ps  # Verificación de los contenedores en ejecución
/sr0263$ python client.py --uploaod big_file.txt
/sr0263$ python client.py --download big_file.txt prueba1.txt 
```
- Vista del Funcionamiento del Tracker/Nodos y Prueba de Subida y Descarga de Archivos
![Vista del Funcionamiento del Tracker/Nodos y Prueba de Subida y Descarga de Archivos](https://github.com/user-attachments/assets/99e2f757-f568-42a2-b186-e7fb9680d535)

## Video explicativo
https://1drv.ms/v/s!AgcSjM0T0apChQQZsO28745O6i1h?e=ofgAEa

## Author

- Developed by [Nicolas Moreno Lopez](https://github.com/Nicorenox)

