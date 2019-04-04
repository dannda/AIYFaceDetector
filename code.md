# Code
Para implementar el Detector en el Vision Kit se necesitan 2 programas. custom_object_detection.py y object_detection_face.py
1) El primero es una version modificada del modulo de deteccion de objetos que viene por defualt, se le cambia la cantidad de clases a solo 2: background y face y la direccion del protobinary que utiliza.
2) El segundo es el programa que hace la inferencia y manda la alerta por correo electronico. Se debe colocar en /home/pi/AIY-projects-python/src/examples/vision/Survaile/

# Correr programa desde boot
Por default el kit de visión corre un demo de detección de alegría al inicio. Para esto se usa un servicio systemd que está definido en un archivo de configuración .service ubicado en ~/AIY-projects-python/src/examples/vision/joy/joy_detection_demo.service. Para que corra nuestro programa en el inicio hay que definir un .service similar a este.
Para crear el servicio puede copiar el .service anterior y cambiarle en ExecStart para que apunte hacia la ubicación de tu archivo Python y Descripcion para describir tu programa.
Después tendrías que poner este archivo en /lib/systemd/system/ pero en vez de eso puede crear un link simbólico en /lib/systemd/system/ que apunte hacia tu archivo. Para eso corre el siguiente código sustituyendo ~/Programs/my_program.service por la dirección de tu archivo .service

## crea el link simbolico
sudo ln -s ~/Programs/my_program.service /lib/systemd/system

## recarga la lista de servicios
sudo systemctl daemon-reload

## indicar para correr el servicio en el incicio
sudo systemctl enable my_program.service

## Para correr el programa puedes usar el siguiente comando cambiando my_program por el nombre de tu servicio.
sudo service my_program start
## Para que el servicio ya no se ejecute al inicio, utiliza:
sudo systemctl disable my_program.service
## Para detener el servicio, utiliza.
sudo service my_program stop
