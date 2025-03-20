import cv2

# Adres IP kamery
IP = "10.12.10.60"
USER = "admin"  # Domyślna nazwa użytkownika
PASS = "Borsuk44"  # Domyślne hasło

# Lista standardowych ścieżek RTSP do przetestowania
rtsp_paths = [
    "/stream",
    "/live",
    "/video",
    "/media",
    "/Streaming/Channels/101",
    "/cam/realmonitor?channel=1&subtype=0"
]

# Funkcja do wyświetlania strumienia RTSP
def display_rtsp_stream(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print(f"Nie można otworzyć strumienia RTSP: {rtsp_url}")
        return False

    print(f"Połączono z: {rtsp_url}")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Nie można odczytać klatki")
            break

        cv2.imshow('Podgląd kamery 59 ', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return True

# Przetestuj każdą ścieżkę RTSP
for path in rtsp_paths:
    rtsp_url = f"rtsp://{USER}:{PASS}@{IP}{path}"
    print(f"Próba połączenia z: {rtsp_url}")
    if display_rtsp_stream(rtsp_url):
        break
else:
    print("Nie udało się połączyć z kamerą. Sprawdź ustawienia lub dokumentację.")