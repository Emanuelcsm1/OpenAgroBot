# AgroProtoLab

AgroProtoLab is an open-source Cartesian robot designed for agricultural research and prototyping.  
It integrates Arduino + CNC Shield hardware with stepper motors, a Flask-based web interface, and YOLOv8 for weed detection.  
This project serves as a didactic platform for experimentation, prototyping, and learning in digital agriculture.

## Features
- Cartesian robot controlled by Arduino UNO + CNC Shield + A4988 drivers
- NEMA 17 stepper motors for X and Y movement
- Integrated computer vision system (YOLOv8)
- Flask-based web interface with control buttons
- Serial communication system to trigger actuators
- Open dataset and training configuration
- Results available with training logs and evaluation metrics

## Repository Structure
```
AgroProtoLab/
│── app.py              # Flask web server
│── detect.py           # YOLO detection script
│── static/             # CSS, JS and frontend assets
│── templates/          # HTML templates for Flask
│── dataset/            # Dataset YAML and images
│── runs/               # YOLO training outputs
│── arduino/            # Arduino sketch for CNC Shield + relay
│── results/            # Training logs and graphs
│── README.md           # Documentation
```

## Installation
```bash
# Clone repository
git clone https://github.com/<your-user>/AgroProtoLab.git
cd AgroProtoLab

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

## Training YOLO Model
```bash
yolo detect train     data=dataset/dataset.yaml     model=yolov8n.pt     imgsz=416     batch=16     epochs=50     name=buva_only_model
```

## Running Web Application
```bash
python app.py
```
Then access via [http://localhost:5000](http://localhost:5000)

## Arduino Upload
Upload the Arduino sketch in `/arduino` to your Arduino UNO.  
It manages stepper motors via CNC Shield and triggers relay outputs.

## Example Workflow
1. Prepare dataset (Tetila soybean dataset or custom images)
2. Train YOLOv8 model
3. Run `app.py` to start detection + web control
4. Arduino receives serial commands and activates actuators
5. System stops on weed detection and triggers relay

## Results
Training logs and plots are available in `results/`.  
Metrics: mAP@50, precision, recall.  
Example: `Precision=0.786, Recall=0.491, mAP50=0.579`

## License
MIT License
