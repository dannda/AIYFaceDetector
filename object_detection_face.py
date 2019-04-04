"""Deteccion de rostros para vigilancia y alerta por medio de correo electronico
	
"""
from picamera import PiCamera, Color
from PIL import Image, ImageDraw
import time

from aiy.vision import inference
from aiy.vision.models import custom_object_detection
from aiy.leds import Leds,Color,Pattern

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#direccion en donde se guardaran las imagenes tomadas
capturepath='/home/pi/AIY-projects-python/src/examples/vision/Survaile/captures_face'

#Funcion para enviar correo electronico con fotos adjuntas
def sendImages():
    global capturepath
    #definicion de correo que envia el mensaje y correo que recibe el mensaje
    #emailTrans-direccion de correo que enviara el mensaje
    #emailTransPass-password de la direccion de correo que enviara el mensaje
    #emailRec-direccion de correo que recibira el mensaje
    emailTrans='anonimo@gmail.com'
    emailTransPass='anonimo'
    emailRec='anonimo@hotmail.com'

    #log-in al servidor del correos, dependiendo de que tipo de cuenta uses para mandar los correos este puede cambiar
    #para gmail usa server=smtplib.SMTP('smtp.gmail.com',587)
    #para hotmail usa server=smtplib.SMTP('smtp.live.com',587)
    #para outlook usa server=smtplib.SMTP('smtp-mail.outlook.com',587)
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    
    msg=MIMEMultipart()
    msg['From']=emailTrans
    msg['To']=emailRec
    msg['Subject']='Te estan robando!'
    msg.attach(MIMEText('imagenes','plain'))

    filename=capturepath+'/image01.jpg'
    imagedata=open(filename,'rb').read()
    attachment=MIMEImage(imagedata)
    msg.attach(attachment)
    
    filename=capturepath+'/image02.jpg'
    imagedata=open(filename,'rb').read()
    attachment=MIMEImage(imagedata)
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(emailTrans,emailTransPass)
    server.sendmail(emailTrans, emailRec, msg.as_string())
    server.quit()


def main():
    global capturepath
    fileN=0
    print('led blue')
    leds = Leds()
    leds.pattern = Pattern.blink(500)
    leds.update(Leds.rgb_pattern(Color.BLUE))
    time.sleep(15)
    leds.update(Leds.rgb_on(Color.BLUE))
    with PiCamera(resolution=(1640, 1232)) as camera:
        with inference.CameraInference(custom_object_detection.model()) as camera_inference:
            for result in camera_inference.run(None):
                objects = custom_object_detection.get_objects(result, args.threshold)
                for i, obj in enumerate(objects):
                    print('Object #%d: %s' % (i, obj))
                if len(objects)>0:
                    leds.update(Leds.rgb_pattern(Color.RED))
                    try:
                        for i, filename in enumerate(camera.capture_continuous(capturepath+'/image{counter:02d}.jpg')):
                            print(filename)
                            time.sleep(5)
                            if i>0:
                                break
                        print('sendimages')
                        leds.update(Leds.rgb_pattern(Color.GREEN))
                        sendImages()
                        print('done')
                    except Exception as e:
                           print(e)
                           
                    leds.update(Leds.rgb_on(Color.BLUE))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        leds = Leds()
        leds.update(Leds.rgb_off())
