'''
Inove Drone Mock Python IoT
---------------------------
Autor: Inove Coding School
Version: 1.0
 
Descripcion:
Se utiliza Flask para crear un generador de datos
de telemetría simulando un Drone:
- Motores
- Luz ON/OFF

Ejecución: Lanzar el programa y abrir en un navegador la siguiente dirección URL
http://IP:5007/
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.0"

import traceback
import json

from flask import Flask, request, jsonify, render_template, redirect
from flask_socketio import SocketIO
from flask_socketio import send, emit

app = Flask(__name__)
app.secret_key = 'ptSecret'
app.config['SECRET_KEY'] = 'ptSecret'
socketio = SocketIO(app)

# ---- MQTT ----
import paho.mqtt.client as mqtt
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("MQTT Conectado")
    # Alumno
    # Suscribierse al topico relativo al sistema de vuelo
    # Suscribierse al topico relativo a la luz
    # Suscribierse al topico relativo al sistema de motores
    client.subscribe("actuadores/volar")
    client.subscribe("actuadores/luces/1")
    client.subscribe("actuadores/motores/#")
    client.subscribe("actuadores/joystick")
    
def mqtt_connect():
    if client.is_connected() is False:
        try:
            client.connect("localhost", 1883, 10)
            print("Conectado al servidor MQTT")
            client.loop_start()
        except:
            print("No pudo conectarse")


def on_message(client, userdata, msg):
    topic = str(msg.topic)
    value = str(msg.payload.decode("utf-8"))
    if topic == "actuadores/volar":
        socketio.emit('volar', int(value))
    
    # NOTA: Podría mejorarse el manejo del ID
    # utilizando regular expression (re)
    # Se deja de esta manera para que se vea
    # facil para el alumno
    if topic == "actuadores/luces/1":
        socketio.emit('luz_1', int(value))
    if topic == "actuadores/motores/1":
        socketio.emit('motor_1', int(value))
    if topic == "actuadores/motores/2":
        socketio.emit('motor_2', int(value))
    if topic == "actuadores/motores/3":
        socketio.emit('motor_3', int(value))
    if topic == "actuadores/motores/4":
        socketio.emit('motor_4', int(value))
    


# ---- Endpoints ----
@app.route('/')
def home():
    mqtt_connect()
    return render_template('index.html')


# ---- Web sockets contra el frontend ----
@socketio.on('luz_event')
def ws_luz_event(data):
    # Alumno: data posee el estado de la luz actualizado
    # desde la interfaz web
    # data --> estado de la luz_1 (0 o 1), pasar a int
    # Realizar el publish de data al topico correspondiente
    # Colocar un breakpoint dentro de esta funcion si lo requiere
    # para debuggear como llega la información de data
    client.publish("actuadores/luces/1", int(data))


@socketio.on('volar_event')
def ws_volar_event(data):
    # Alumno: data posee el estado de volar actualizado
    # desde la interfaz web
    # data --> estado de la volar (0 o 1), pasar a int
    # Realizar el publish de data al tópico correspondiente
    # Colocar un breakpoint dentro de esta funcion si lo requiere
    # para debuggear como llega la información de data
    client.publish("actuadores/volar", int(data))


@socketio.on('motores_event')
def ws_motores_event(data):
    # Alumno: data posee el estado de los cuatro motores actualizado
    # desde la interfaz web en formato de lista
    # data --> lista de estado de los motores, pasar a int c/u
    # Realizar el publish de data al tópico correspondiente
    # Deberá realizar un bucle para enviar el dato corespondiente
    # de cada motor a su respectivo tópico.
    # Colocar un breakpoint dentro de esta funcion si lo requiere
    # para debuggear como llega la información de data
    client.publish("actuadores/motores/1", int(data[0]))
    client.publish("actuadores/motores/2", int(data[1]))
    client.publish("actuadores/motores/3", int(data[2]))
    client.publish("actuadores/motores/4", int(data[3]))


@socketio.on('joystick_event')
def ws_joystick_event(data):
    # Alumno: data posee el estado del joystick actualizado
    # desde la interfaz web en formato de JSON
    # data --> diccionario de estado del joystick, enviar como JSON string
    # Realizar el publish de data al tópico correspondiente
    # Deberá realizar un JSON dumps para transformar el JSON
    # en JSTON String
    # Colocar un breakpoint dentro de esta funcion si lo requiere
    # para debuggear como llega la información de data    
    valor = json.dumps(data)
    print(valor)
    client.publish("actuadores/joystick", valor)
    

if __name__ == "__main__":

    client.on_connect = on_connect
    client.on_message = on_message

    app.run(debug=True, host="0.0.0.0", port=5007)
