import cv2
import tensorflow as tf
from deep_sort_realtime.deepsort_tracker import DeepSort
from collections import deque

# Inicjalizacja detektora obiektów (np. TensorFlow SSD, YOLO lub Faster R-CNN)
model = tf.saved_model.load('ssd_mobilenet_v2_coco/saved_model')  # Przykład modelu SSD

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

# Ustawienia kamery
camera_url = "http://admin:Borsuk44@10.12.10.59:80/Streaming/Channels/1"  # Przykładowy adres HTTP
cap = cv2.VideoCapture(camera_url)
camera_url = "rtsp://admin:Borsuk44@10.12.10.59:554/Streaming/Channels/1"  # Przykładowy adres RTSP
cap = cv2.VideoCapture(camera_url)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
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
    cv2.imshow('Tracking', frame)

    # Wyjście po naciśnięciu 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
