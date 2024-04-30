import cv2
import os
import matplotlib

siniflandirici  = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

videoCam = cv2.VideoCapture(0)

if not videoCam.isOpened():
    print("kamera bulunamadı")
    exit()

#########################################

basilirsa = False
while (basilirsa == False):
    ret, cerceve = videoCam.read()

    if ret == True:
        grilestirme = cv2.cvtColor(cerceve, cv2.COLOR_BGR2GRAY)
        yuz = siniflandirici.detectMultiScale(grilestirme, scaleFactor = 1.3, minNeighbors = 2)

        for (x, y, w, h) in yuz:
            cv2.rectangle(cerceve, (x, y), (x + w, y + h), (0, 255, 0), 2)

        ekran_yazisi = "Bulunan Yuz = " + str(len(yuz))

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(cerceve, ekran_yazisi, (0, 30), font, 1, (255, 0, 0), 1)

        cv2.imshow("sonuc", cerceve)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            basilirsa = True
            break

videoCam.release()
cv2.destroyAllWindows()