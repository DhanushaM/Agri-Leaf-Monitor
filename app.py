from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

healthy_folder = 'static/healthy'
diseased_folder = 'static/diseased'

# Sample tips
healthy_tips = [
    "Water the plants regularly but avoid waterlogging.",
    "Provide adequate sunlight daily.",
    "Use balanced fertilizer every month.",
    "Remove weeds around the plant.",
    "Prune old and yellowing leaves.",
    "Keep the garden clean.",
    "Avoid chemical pesticides excessively.",
    "Maintain proper soil pH.",
    "Use mulch to retain soil moisture.",
    "Monitor for pests weekly."
]

diseased_tips = [
    "Remove affected leaves immediately.",
    "Avoid overhead watering.",
    "Use organic fungicides if necessary.",
    "Improve air circulation around plants.",
    "Disinfect tools after use.",
    "Maintain proper spacing between plants.",
    "Ensure proper soil drainage.",
    "Avoid excessive nitrogen fertilizers.",
    "Rotate crops each season.",
    "Monitor and isolate infected plants."
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_leaf_health(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return 'invalid'
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Green mask
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([95, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = cv2.countNonZero(mask_green) / (image.shape[0]*image.shape[1])

    # Yellow/Brown/Black mask (simplified)
    lower_yellow = np.array([10, 40, 40])
    upper_yellow = np.array([30, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    lower_brown = np.array([0, 40, 40])
    upper_brown = np.array([20, 255, 200])
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    diseased_ratio = (cv2.countNonZero(mask_yellow) + cv2.countNonZero(mask_brown) + cv2.countNonZero(mask_black)) / (image.shape[0]*image.shape[1])

    if green_ratio > 0.6 and diseased_ratio < 0.05:
        return 'healthy'
    elif diseased_ratio > 0.05:
        return 'diseased'
    else:
        return 'invalid'

@app.route('/')
def index():
    healthy_images = os.listdir(healthy_folder)
    diseased_images = os.listdir(diseased_folder)
    return render_template('index.html',
                           healthy_images=healthy_images,
                           diseased_images=diseased_images,
                           healthy_tips=healthy_tips,
                           diseased_tips=diseased_tips)

@app.route('/upload', methods=['POST'])
def upload():
    if 'leaf' not in request.files:
        return redirect(url_for('index'))
    file = request.files['leaf']
    if file.filename == '':
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        result = detect_leaf_health(save_path)
        return render_template('upload_result.html', result=result, filename=filename)
    else:
        return render_template('upload_result.html', result='invalid', filename='')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
