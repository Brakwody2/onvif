import cv2
from onvif import ONVIFCamera

# Konfiguracja kamery
IP = "10.12.10.58"
PORT = 80
USER = "admin"  # Domyślna nazwa użytkownika
PASS = "Borsuk44"  # Domyślne hasło

# Inicjalizacja kamery ONVIF
mycam = ONVIFCamera(IP, PORT, USER, PASS)

# Pobieranie adresu strumienia RTSP
media_service = mycam.create_media_service()
profiles = media_service.GetProfiles()
token = profiles[0].token
stream_uri = media_service.GetStreamUri({'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': 'RTSP'}, 'ProfileToken': token})

# Otwarcie strumienia RTSP
cap = cv2.VideoCapture(stream_uri.Uri)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Nie można odczytać strumienia wideo")
        break

    # Wyświetlanie obrazu
    cv2.imshow('Podgląd kamery', frame)

    # Przerwanie pętli po naciśnięciu klawisza 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zwolnienie zasobów
cap.release()
cv2.destroyAllWindows()