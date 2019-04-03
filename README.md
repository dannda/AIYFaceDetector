# Sistema de Vigilancia basado en un Google AIY

Un problema al que nos encontramos fue tener que disponer de un sistema para emitir una alerta temprana cuando hubiera intrusiones a espacios, tales como oficinas o laboratorios, fuera de horarios de operación. Para resolver este problema construimos una solución basada en aprendizaje profundo, alrededor de la plataforma [Google AIY Vision Kit](https://aiyprojects.withgoogle.com/vision/), que envía un mensaje de email cuando detecta un rostro humano. Este documento describe como reproducir este sistema y como solucionar algunos de los problemas que enfrentamos durante su desarrollo.

Nuestra decisión de construir nuestra solución alrededor de aprendizaje profundo se basa en el hecho de este conjunto de técnicas ha mostrado proporcionar los mejores niveles de desempeño en tareas de [detección](http://cocodataset.org/#detection-leaderboard). Por su parte, nuestro interés en utilizar el Google AIY Vision tuvo que ver con la exploración de las capacidades de una plataforma de bajo costo que reciéntemente fue introducida en el mercado.


## Introducción
Detección de Rostros
De las aplicaciones para detección de objetos, una aplicación interesante es la detección de rostros, en la que a partir de un banco de fotografías (base de datos), se procesan para entrenar a un sistema que realice el reconocimiento de los objetos dentro de la imagen.
Existen aplicaciones en las que a partir de la lectura de una imagen (archivo), se identifica un rostro y emoción como se muestra en Ilustración 1 y el sistema realiza el procesamiento, generando el objeto y emoción que identifico y la probabilidad de certeza.
 
Ilustración 1. Detección de Rostros
(Tomado de https://webrtchacks.com/aiy-vision-kit-uv4l-web-server/, 2018-mar)
¿Cómo se da el procesamiento de imágenes?
De manera general en Deep Learning, se analiza la imagen a través de las siguientes etapas:
1)	Adquirir una imagen
2)	Procesar la imagen en Redes Convolucionales (calcula el % de certeza) 
a.	Entrenamiento de un modelo
b.	Utilizar un modelo Deep Learning entrenado previamente
3)	Define el objeto que ha reconocido
Aplicaciones 
1)	Reconocimiento de objetos con Vision Kit Aiy, se muestra en Ilustración 2 la captura de la imagen con la cámara de Vision Kit Aiy y en la interfaz se despliega “73% Joy detected”
 
Ilustración 2. Implementación de Vision Kit AIY 
(Tomado de https://www.analyticsindiamag.com/behind-googles-aiy-kits/, 2018-may)
2)	Búho mostrado en la Ilustración 2, desarrollado por Alex Glow en el que utiliza Google Vision Kit para análisis de imágenes, como reconocer emociones de una cara y reconocer objetos. 
 
Ilustración 3. Búho
(Tomado de https://blog.bricogeek.com/noticias/diy/buho-impreso-en-3d-que-usa-google-vision-kit-para-analisis-de-imagen/, 2018-nov)

## Aplicación

## [Requerimientos](https://github.com/dannda/AIYFaceDetector/blob/master/requirements.md)
## [Entrenamiento](https://github.com/dannda/AIYFaceDetector/blob/master/training.md)
## [Código fuente](https://github.com/dannda/AIYFaceDetector/blob/master/code.md)

## Pruebas

## Discusión
