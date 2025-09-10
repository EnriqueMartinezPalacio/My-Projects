# 🖐️ Sign Language Recognition System  

A **real-time sign language recognition system** built with **YOLOv8**, **OAK-D camera**, **Tkinter interfaces**, and **MQTT communication**.  
This project translates hand gestures into structured commands for **smart environments** such as home automation.  

---

## 🚀 Features  

- **YOLOv8-based gesture recognition** (custom models).  
- **Tkinter GUIs** for real-time visualization and phrase display.  
- **Dataset collection pipeline** using OAK-D and threaded saving.  
- **False positive reduction** with buffer-based filtering.  
- **Command flow pipeline**: Activation → Action → Location/Time.  
- **MQTT integration** for IoT communication.  
- **Countdown timers** with real-time MQTT publishing.  

---

## 📂 Project Structure  

```
.
├── yolo_interface.py      # GUI with YOLO hand detection
├── image_capture.py       # Collect dataset images with OAK-D
├── phrase_display.py      # Display final phrase with timer
├── full_pipeline.py       # Main project: YOLO + MQTT + Timers
├── models/                # Trained YOLOv8 models (not included)
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

---

## 🛠️ Requirements  

- Python 3.9+  
- OpenCV  
- Tkinter  
- Pillow  
- DepthAI SDK  
- Ultralytics YOLOv8  
- Paho MQTT  

Install all dependencies:  

```bash
pip install -r requirements.txt
```

**requirements.txt** example:  

```
ultralytics
opencv-python
pillow
depthai
paho-mqtt
```

---

## 📖 Modules Overview  

| Module              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| **yolo_interface.py** | Tkinter GUI with YOLO model: displays detections, classes, confidences.   |
| **image_capture.py**  | Collects labeled gesture images with OAK-D; saves efficiently with threads. |
| **phrase_display.py** | GUI showing final phrase, MQTT message, and countdown timer (MM:SS).       |
| **full_pipeline.py**  | Complete system: YOLO models + MQTT + Timers; builds structured commands. |

---

## ⚡ Workflow  

1. **User performs "Atención" gesture** → system activates.  
2. **Action detection** → e.g., *Abrir, Cerrar, LuzOn*.  
3. **Location or time detection** → e.g., *Cocina, Sala, 10 segundos*.  
4. **Final phrase built** → displayed on GUI.  
5. **MQTT message sent**:  

```
Topic: Cocina
Message: Abrir
```

---

## ▶️ Usage  

Run modules individually or the full pipeline:  

```bash
# GUI with YOLO detections
python yolo_interface.py  

# Collect dataset images
python image_capture.py  

# Display final phrase
python phrase_display.py  

# Full system with MQTT
python full_pipeline.py  
```

---

## 📌 Notes  

- YOLO `.pt` models are **not included** (train your own or request access).  
- Recommended hardware: **OAK-D Lite** camera.  
- Default MQTT broker: `broker.emqx.io:8883` (configurable).  

---

## 🔮 Future Improvements  

- Expand dataset for more robust recognition.  
- Multi-language sign support.  
- Cloud deployment for distributed recognition.  
- Edge deployment (Jetson Nano, Raspberry Pi).  
- Integration with robotics platforms.  

---


