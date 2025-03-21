import cv2
import subprocess
import numpy as np

# Parametry kamery
IP = "10.12.10.58"
USER = "admin"
PASS = "admin"
rtsp_url = f"rtsp://{USER}:{PASS}@{IP}:554/Streaming/Channels/101"

# Uruchamiamy FFmpeg jako konwerter H.265 → H.264
ffmpeg_cmd = [
    f"C:\FF\ffmpeg20250320\bin\ffmpeg", "-rtsp_transport", "tcp", "-i", rtsp_url,
    "-an", "-c:v", "libx264", "-preset", "ultrafast", "-f", "rawvideo",
    "-pix_fmt", "bgr24", "-"
]

process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)

width, height = 1920, 1080  # Dopasuj do rozdzielczości kamery

while True:
    raw_frame = process.stdout.read(width * height * 3)  # Odczytujemy surową ramkę (RGB)
    if not raw_frame:
        break

    frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((height, width, 3))

    cv2.imshow("Podgląd kamery (H.264)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

process.terminate()
cv2.destroyAllWindows()
