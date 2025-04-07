import os

from model import Ocr_Model
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename


model = Ocr_Model()

UPLOAD_FOLDER = '/mmocr/workspace/data'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/load_file', methods=['GET', 'POST'])
def get_image():
    if 'file' not in request.files:
        return {'message': 'No file part'}, 400
    file = request.files['file']
    if file.filename == '':
        return {'message': 'No selected part'}, 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('send_res', name=filename))


@app.route('/get_res/<string:name>')
def send_res(name):
    return {'res': model.pred(os.path.join(app.config['UPLOAD_FOLDER'], name))}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
