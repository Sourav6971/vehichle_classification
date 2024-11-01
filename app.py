from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
from predict import predict

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder to store uploaded images
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload_and_predict():
    if 'image' not in request.files:
        return "No file part", 400
    
    file = request.files['image']
    
    if file.filename == '':
        return "No selected file", 400
    
    # Save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Predict the category
    prediction = predict(file_path)

    # Render the result in the template
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
