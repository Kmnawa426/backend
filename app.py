from flask import Flask, request, send_file, jsonify
from stegano import lsb
import os

app = Flask(__name__)

@app.route('/encode', methods=['POST'])
def encode():
    if 'image' not in request.files or 'message' not in request.form:
        return "Invalid request", 400

    image = request.files['image']
    message = request.form['message']

    # Save the uploaded image
    image_path = 'uploaded_image.png'
    image.save(image_path)

    # Encode the message into the image
    secret = lsb.hide(image_path, message)
    encoded_image_path = 'encoded_image.png'
    secret.save(encoded_image_path)

    # Return the encoded image
    return send_file(encoded_image_path, as_attachment=True)

@app.route('/decode', methods=['POST'])
def decode():
    if 'image' not in request.files:
        return "Invalid request", 400

    image = request.files['image']

    # Save the uploaded image
    image_path = 'uploaded_encoded_image.png'
    image.save(image_path)

    # Decode the message from the image
    message = lsb.reveal(image_path)

    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True)