import paho.mqtt.client as paho
import json
import time
from dotenv import dotenv_values

config = dotenv_values()

broker = config["BROKER"]
port = int(config["PORT"])


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Mqtt conectado")
    else:
        print(f"Mqtt connection faild, error code={rc}")


def controlador(client, actuador, valor):
    
    if actuador == "luces":
        topico= "actuadores/luces/1"
        valor = int(input("Ingrese 1 para prende o 0 para apagar la luz: "))

    elif actuador == "volar":
        topico= "actuadores/volar"
        valor = int(input("Ingrese 1 para iniciar o 0 para finalizar el vuelo: "))
    
    elif actuador == "motores":
        motor = int(input("Ingrese el motor a controlar 1,2,3 o 4: "))
        topico= "actuadores/motores/" + str(motor)
        valor = int(input("Ingrese 1 para encender o 0 para apagar el motor: "))
    
    elif actuador == "joystick":
        while True:
            eje_x = float(input("Ingrese movimiento en eje x(-1 a 1): "))
            if eje_x > 1 or eje_x < -1:
                print("Valor incorrecto, reingrase:") 
            else:
                break

        while True:
            eje_y = float(input("Ingrese movimiento en eje y(0 a 1): "))
            if eje_y > 1 or eje_y < 0:
                print("Valor incorrecto, reingrase:") 
            else:
                break

        topico= "actuadores/joystick"
        axes= {"x": eje_x, "y": eje_y}
        valor = json.dumps(axes)
      
    else:
        print("Actuador desconocido")
        return

    client.publish(topico, valor)

  
if __name__ == "__main__":

    print("Drone Mock: Sistema controlador de actuadores")

    # Aquí conectarse a MQTT
    client = paho.Client("controlador")
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    time.sleep(1)

    while True:
        actuador = input("Ingrese que actuador desea controlar, o escriba FIN para salir: ").lower()
        if actuador == "fin":
            break
    
        valor = 0 
        controlador(client, actuador, valor)


    client.disconnect()
    client.loop_stop()
    print("Mqtt desconectado")