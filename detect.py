import cv2
import numpy as np
from ultralytics import YOLO
from serial_comm import send_command

# Modelo YOLO (somente para visualização)
model = YOLO("runs/detect/buva_only_model9/weights/best.pt")

# HSV verde + zona central
LOWER_GREEN = (35, 70, 70)
UPPER_GREEN = (85, 255, 255)
CENTER_ZONE_RATIO = 0.20  # 20% central
MIN_CONTOUR_AREA = 1000    # ignora manchas muito pequenas
YOLO_CONF = 0.30           # só para mostrar caixas

def detect_in_frame(frame):
    # Padroniza resolução (mantém leve e previsível)
    frame = cv2.resize(frame, (640, 480))
    h_img, w_img = frame.shape[:2]

    # Máscara de verde
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)

    # Limpa ruído leve
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Zona central de disparo
    cx_min = int(w_img * (0.5 - CENTER_ZONE_RATIO / 2))
    cx_max = int(w_img * (0.5 + CENTER_ZONE_RATIO / 2))
    cy_min = int(h_img * (0.5 - CENTER_ZONE_RATIO / 2))
    cy_max = int(h_img * (0.5 + CENTER_ZONE_RATIO / 2))
    cv2.rectangle(frame, (cx_min, cy_min), (cx_max, cy_max), (255, 255, 0), 2)

    detected = False

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < MIN_CONTOUR_AREA:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        cx, cy = x + w // 2, y + h // 2

        # Visual do verde
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)

        # Disparo por verde centralizado
        if cx_min < cx < cx_max and cy_min < cy < cy_max:
            cv2.putText(frame, "STOP: Verde centralizado", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            print("🛑 Verde centralizado detectado! Enviando 'stop'")
            send_command("stop")
            detected = True

        # ---------- YOLO SÓ PARA VISUALIZAÇÃO ----------
        # ROI quadrada ao redor do centro do contorno, com margem
        size = int(max(w, h) * 1.4)  # margem para dar contexto ao YOLO
        x1 = max(cx - size // 2, 0)
        y1 = max(cy - size // 2, 0)
        x2 = min(cx + size // 2, w_img)
        y2 = min(cy + size // 2, h_img)

        # Garante ROI válida (evita erro no slicing)
        if x2 - x1 < 5 or y2 - y1 < 5:
            continue

        roi = frame[y1:y2, x1:x2]
        if roi.size == 0:
            continue

        # Redimensiona para o tamanho “esperado” pelo modelo (simula escala do dataset)
        roi_resized = cv2.resize(roi, (416, 416), interpolation=cv2.INTER_LINEAR)

        # Predição YOLO na ROI
        results = model.predict(roi_resized, conf=YOLO_CONF, verbose=False)[0]

        # Desenha caixas do YOLO mapeando de volta à escala original
        if results.boxes is not None and len(results.boxes) > 0:
            scale_x = (x2 - x1) / 416.0
            scale_y = (y2 - y1) / 416.0

            # Converte para numpy para evitar operações "in-place" em tensores
            boxes_xyxy = results.boxes.xyxy.cpu().numpy()
            confs = results.boxes.conf.cpu().numpy()
            clss = results.boxes.cls.cpu().numpy().astype(int)

            for (bx1, by1, bx2, by2), conf, c in zip(boxes_xyxy, confs, clss):
                # Remapeia para a imagem completa
                X1 = int(bx1 * scale_x) + x1
                Y1 = int(by1 * scale_y) + y1
                X2 = int(bx2 * scale_x) + x1
                Y2 = int(by2 * scale_y) + y1

                cv2.rectangle(frame, (X1, Y1), (X2, Y2), (0, 0, 255), 2)
                label = model.names.get(c, str(c))
                cv2.putText(frame, f"{label} {conf:.2f}", (X1, Y1 - 6),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        # -----------------------------------------------

    return frame, detected
