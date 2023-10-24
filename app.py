## flask app for removing noises from images

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import numpy as np
import pandas as pd
import cv2
import base64
import os

app=Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/romove_noise', methods=['POST'])
@cross_origin()
def noiseRemovalRoute():

    imgstring = request.json['image']
    imgdata = base64.b64decode(imgstring)
    with open('static/images/noisy_img.jpg', 'wb') as f:
        f.write(imgdata)
        f.close()
    
    # Load the input image
    noisy_image = cv2.imread("static/images/noisy_img.jpg")

    # Denoise the image
    denoised_image = cv2.GaussianBlur(noisy_image, (5,5), 0)

    # Save the denoised image
    cv2.imwrite('static/images/denoised_img.jpg', denoised_image)

    noisy_image_path = os.path.join('static/images','noisy_img.jpg')
    denoised_image_path = os.path.join('static/images','denoised_img.jpg')

    return jsonify({'noisy_image': noisy_image_path, 'denoised_image':denoised_image_path})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)