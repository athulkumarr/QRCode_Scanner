# Import the required libraries
import cv2
import time
import webbrowser
import simpleaudio 
from pyzbar import pyzbar

# Function to read QR code
def read_QR(frame):
    x, y, w, h = 0, 0, 0, 0
    QR_info = None
    QRs = pyzbar.decode(frame)

    for QR in QRs:
        x, y , w, h = QR.rect
        QR_info = QR.data.decode('utf-8')
        

    return x, y, w, h, QR_info

# Main function
def main():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    
    while ret:
        # Read a frame from the camera feed
        ret, frame = camera.read()

        # find the coordinates and the height and width of the QR code
        x, y,w, h, link = read_QR(frame)

        if link:
            print('Opening Link: '+ link)

            # Adding a rectangle around the recognized QR code
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, link, (100,50), cv2.FONT_HERSHEY_DUPLEX, 2.0, (0, 0, 255), 5)
            cv2.imshow('QR code reader', cv2.resize(frame, (480, 360)))
            
            if cv2.waitKey(1) & 0xFF == 27:
                break

            # Playing a beep sound when a QR code is detected.
            wave_obj = simpleaudio.WaveObject.from_wave_file("QR.wav")
            play_obj = wave_obj.play()
            play_obj.wait_done()
            
            # Sleep for 1 s
            time.sleep(1)

            # Open the recognized link in the default web browser.
            webbrowser.open(link)
            break

        cv2.imshow('QR code reader', cv2.resize(frame, (480, 360)))
        
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
