from flask import Flask, render_template, Response, redirect, url_for
import cv2
from detect import detect_in_frame
from serial_comm import send_command


app = Flask(__name__)

# Captura de vídeo da câmera USB
cap = cv2.VideoCapture(1)  # Tente 1 se não for a câmera correta

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Aplica detecção com YOLO
        annotated, has_weed = detect_in_frame(frame)

        # Se detectar erva daninha, envia comando ao Arduino
        if has_weed:
            print("Erva daninha detectada!")
            send_command("stop")

        # Codifica frame para JPEG
        _, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Rota para comandos enviados pelos botões HTML
@app.route('/command/<cmd>')
def send_robot_command(cmd):
    send_command(cmd.upper())  # "START", "STOP", "GO_HOME", etc.
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
