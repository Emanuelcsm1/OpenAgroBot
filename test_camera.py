import cv2

cap = cv2.VideoCapture(0)  # tente também 1 ou 2 se necessário

if not cap.isOpened():
    print("❌ Não foi possível acessar a câmera.")
else:
    print("✅ Câmera acessada com sucesso.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Teste Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
