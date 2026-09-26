import os

from flask import (Flask, Response, jsonify, redirect, render_template, request, send_file,
                   session, url_for)
from flask_session import Session
from werkzeug.utils import secure_filename

import predict_img
import predict_video
from predict_camera import run_camera_processing

APP_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(APP_DIR, 'static')
UPLOAD_DIR = os.path.join(APP_DIR, 'upload')
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__, static_folder=STATIC_DIR,
            template_folder=os.path.join(APP_DIR, 'templates'))
# A random key signs everyone out on restart. Set OCEANEYE_SECRET to keep sessions.
app.config['SECRET_KEY'] = os.environ.get('OCEANEYE_SECRET') or os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

last_video_path = None


def save_upload():
    """Save the file from the current request and return its path, or None if there is none."""
    file = request.files.get('file')
    if file is None or file.filename == '':
        return None
    path = os.path.join(UPLOAD_DIR, secure_filename(file.filename))
    file.save(path)
    return path


def mjpeg_response(frames):
    return Response(frames, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    if 'username' not in session:
        return render_template('login.html')
    return render_template('index.html', username=session['username'])


@app.route('/login', methods=['POST'])
def login():
    # ponytail: placeholder login with no user store; add real auth before exposing the app
    session['username'] = request.get_json().get('username')
    return jsonify({'success': True})


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/upload-image', methods=['POST'])
def upload_image():
    path = save_upload()
    if path is None:
        return jsonify({'error': 'No file selected'})
    try:
        output_path = predict_img.detect(path)
    except Exception as exc:
        return jsonify({'error': str(exc)})
    return jsonify({'url': url_for('static', filename=os.path.relpath(output_path, STATIC_DIR))})


@app.route('/upload-video', methods=['POST'])
def upload_video():
    global last_video_path
    path = save_upload()
    if path is None:
        return jsonify({'error': 'No file selected'})
    last_video_path = path
    return jsonify({'message': 'Video uploaded'})


@app.route('/video_feed')
def video_feed():
    if last_video_path is None:
        return 'No video uploaded', 404
    return mjpeg_response(predict_video.run_video_processing(last_video_path))


@app.route('/download-video')
def download_video():
    if last_video_path is None:
        ready, message = False, 'Choose a video first.'
    else:
        path = predict_video.export_path(last_video_path)
        ready = os.path.exists(path)
        message = '' if ready else 'The video is still processing. Let it play to the end.'

    # The page asks with ?check=1 first, so an early click shows a message instead of an error page.
    if request.args.get('check'):
        return jsonify({'ready': ready, 'message': message})
    if not ready:
        return message, 404
    return send_file(path, as_attachment=True)


@app.route('/enhance', methods=['POST'])
def toggle_enhance():
    predict_video.ENHANCE = not predict_video.ENHANCE
    return jsonify({'enhance': predict_video.ENHANCE})


@app.route('/camera_feed')
def camera_feed():
    camera_index = request.args.get('camera_index', type=int)
    if camera_index is None or camera_index < 0:
        return 'Invalid camera index', 400
    return mjpeg_response(run_camera_processing(camera_index))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
