import cv2
import numpy as np
import pyfirmata
from cvzone.FaceDetectionModule import FaceDetector

cap = cv2.VideoCapture(0)
ws, hs = 1280, 720
cap.set(3, ws)
cap.set(4, hs)

if not cap.isOpened():
    print("Kamera Bulunamadi")
    exit()  #kapatt

port = "COM9"   # arduino için kullanılacak port
board = pyfirmata.Arduino(port)
servo_pinX = board.get_pin('d:9:s')     #Arduino için pin 9 u
servo_pinY = board.get_pin('d:10:s')    #Arduino için pin 10 u

detector = FaceDetector()  # tespit edici
#servodurus = [640, 640]
servodurus = [90, 90]     # Servonun başlangıç konumu

while True:
    success, img = cap.read()
    img, bboxs = detector.findFaces(img, draw=False)

    if bboxs:
            # x ve y koordinatlarını çekme
        fx, fy = bboxs[0]["merkez"][0], bboxs[0]["merkez"][1]
        durus = [fx, fy]

            # çekilen koordinatin servo için dönüştürülmesi
        servoX = np.interp(fx, [0, ws], [0, 180])
        servoY = np.interp(fy, [0, hs], [0, 180])

        if servoX < 0:
            servoX = 0
        elif servoX > 180:
            servoX = 180
        if servoY < 0:
            servoY = 0
        elif servoY > 180:
            servoY = 180

        servodurus[0] = servoX
        servodurus[1] = servoY


        cv2.circle(img, (fx, fy), 80, (0, 0, 255), 2)
        cv2.putText(img, str(durus), (fx+15, fy-15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2 )
        cv2.line(img, (0, fy), (ws, fy), (0, 0, 0), 2)  # x eskenidir
        cv2.line(img, (fx, hs), (fx, 0), (0, 0, 0), 2)  # y eksenidir
        cv2.circle(img, (fx, fy), 15, (0, 0, 255), cv2.FILLED)
        cv2.putText(img, "Hedefe Kitlendi", (850, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3 )

    else:
        cv2.putText(img, "Hedef Bulunamadi", (880, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        cv2.circle(img, (640, 360), 80, (0, 0, 255), 2)
        cv2.circle(img, (640, 360), 15, (0, 0, 255), cv2.FILLED)
    # x ekseni
        cv2.line(img, (0, 360), (ws, 360), (0, 0, 0), 2)
    # y ekseni
        cv2.line(img, (640, hs), (640, 0), (0, 0, 0), 2)


    cv2.putText(img, f'Servo X: {int(servodurus[0])} deg', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.putText(img, f'Servo Y: {int(servodurus[1])} deg', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    servo_pinX.write(servodurus[0])
    servo_pinY.write(servodurus[1])

    goruntu = image
    cv2.imshow("image", img)
    cv2.waitKey(1)