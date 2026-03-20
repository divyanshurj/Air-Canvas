# Air-Canvas
# Air Canvas 🎨✨

A real-time computer vision application that allows users to draw on a digital canvas simply by moving their hands in the air. 

By leveraging hand-tracking technology, this project translates physical finger movements into digital strokes on the screen, creating an interactive and touchless drawing experience.

##Features
* **Real-Time Hand Tracking:** Accurately detects and tracks hand landmarks with zero noticeable latency.
* **Air Drawing:** Uses the tip of the index finger as a virtual pen to draw on the screen.
* **Color Palette Selection:** Seamlessly switch between different colors by hovering over the on-screen palette.
* **Modular Architecture:** Separates the core tracking logic from the UI rendering for improved performance, accuracy, and maintainability.

##Project Structure
* `canvas.py`: The main application script that renders the OpenCV interface, manages the webcam feed, and handles the drawing logic.
* `HandTrackingModule.py`: A dedicated backend module processing MediaPipe's hand landmark detection to ensure high accuracy and clean code separation.

## 🛠️ Tech Stack
* **Language:** Python
* **Libraries:** * `OpenCV` (for image processing and UI)
  * `MediaPipe` (for robust hand tracking and landmark detection)
  * `NumPy` (for matrix operations and handling image arrays)
