import cv2
from onvif import ONVIFCamera
import tensorflow as tf
from deep_sort_realtime.deepsort_tracker import DeepSort
from collections import deque

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

# Inicjalizacja detektora obiektów (np. TensorFlow SSD, YOLO lub Faster R-CNN)
model_path = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/saved_model'

# Załaduj model
model = tf.saved_model.load(model_path)

# Inicjalizacja DeepSORT
deepsort = DeepSort()

# Funkcja do wykrywania obiektów za pomocą modelu TensorFlow
def detect_objects(frame):
    input_tensor = tf.convert_to_tensor(frame)
    input_tensor = input_tensor[tf.newaxis,...]
    detections = model(input_tensor)
    return detections

# Funkcja do śledzenia obiektów
def track_objects(frame, detections):
    # Przekazujemy wykryte obiekty do DeepSORT
    tracks = deepsort.update_tracks(detections)
    return tracks


while True:
    ret, frame = cap.read()
    if not ret:
        print("Nie można odczytać strumienia wideo")
        break
    print("Odczytano klatkę")

# Wykrywanie obiektów
    detections = detect_objects(frame)
    
    # Formatowanie wyników detekcji (bounding boxes)
    detection_boxes = []
    for detection in detections['detection_boxes']:
        detection_boxes.append([detection[0].numpy(), detection[1].numpy()])
    
    # Śledzenie obiektów
    tracks = track_objects(frame, detection_boxes)

    # Rysowanie wyników na obrazie
    for track in tracks:
        if track.is_confirmed():
            x1, y1, x2, y2 = track.to_tlbr()  # Pobieramy koordynaty
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  # Rysujemy prostokąt
            cv2.putText(frame, f"ID: {track.track_id}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)



    # Wyświetlanie obrazu 
    cv2.imshow('Podgląd kamery', frame)

    # Przerwanie pętli po naciśnięciu klawisza 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zwolnienie zasobów
cap.release()
cv2.destroyAllWindows()