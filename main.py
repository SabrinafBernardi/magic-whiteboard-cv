import os
import tempfile
import urllib.request
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = os.path.join(tempfile.gettempdir(), "hand_landmarker.task")
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

if not os.path.exists(MODEL_PATH):
    print("Baixando modelo do MediaPipe...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=1
)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

CORES = [
    (128, 0, 128),   # Roxo
    (203, 192, 255), # Rosa Claro
    (0, 0, 255),     # Vermelho
    (255, 255, 255)  # Branco 
]
cor_atual = CORES[0]
espessura = 5

xp, yp = 0, 0  
canvas = None  

print("\n--- CONTROLES ---")
print(" Apenas indicador: Desenhar")
print(" Indicador + Médio: Mover sem desenhar e Selecionar Cor")
print("Teclas: 'c' = Limpar tela | '+' e '-' = Espessura | 'q' = Sair\n")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
 
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    result = detector.detect(mp_image)
  
    cv2.rectangle(frame, (20, 10), (120, 60), CORES[0], -1)
    cv2.rectangle(frame, (140, 10), (240, 60), CORES[1], -1)
    cv2.rectangle(frame, (260, 10), (360, 60), CORES[2], -1)
    cv2.rectangle(frame, (380, 10), (480, 60), CORES[3], -1)
    
    cv2.rectangle(frame, (500, 10), (600, 60), (100, 100, 100), -1)
    cv2.putText(frame, "LIMPAR", (510, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    if result.hand_landmarks:
        landmarks = result.hand_landmarks[0]
 
        x_ind, y_ind = int(landmarks[8].x * w), int(landmarks[8].y * h)
        x_med, y_med = int(landmarks[12].x * w), int(landmarks[12].y * h)
 
        indicador_up = landmarks[8].y < landmarks[6].y
        medio_up = landmarks[12].y < landmarks[10].y

        if indicador_up and medio_up:
            xp, yp = 0, 0
            cv2.circle(frame, (x_ind, y_ind), 15, cor_atual, cv2.FILLED)
    
            if y_ind < 60:
                if 20 < x_ind < 120:
                    cor_atual = CORES[0]
                elif 140 < x_ind < 240:
                    cor_atual = CORES[1]
                elif 260 < x_ind < 360:
                    cor_atual = CORES[2]
                elif 380 < x_ind < 480:
                    cor_atual = CORES[3]
                elif 500 < x_ind < 600:
                    canvas = np.zeros((h, w, 3), dtype=np.uint8)
       
        elif indicador_up and not medio_up:
            cv2.circle(frame, (x_ind, y_ind), espessura, cor_atual, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x_ind, y_ind

            cv2.line(canvas, (xp, yp), (x_ind, y_ind), cor_atual, espessura)
            xp, yp = x_ind, y_ind

        else:
            xp, yp = 0, 0

    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 10, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, img_inv)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("Lousa Magica", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
    elif key == ord('+') or key == ord('='):
        espessura += 2
    elif key == ord('-'):
        espessura = max(1, espessura - 2)

cap.release()
cv2.destroyAllWindows()