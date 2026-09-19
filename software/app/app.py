from flask import (Flask, request, jsonify, render_template, session, url_for, Response,
                   send_file)
from flask_session import Session
import os

# supporting modules
from werkzeug.utils import secure_filename
import predict_img
import predict_video  # imported as a module so /enhance can flip its ENHANCE flag
from predict_video import run_video_processing
from predict_camera import run_camera_processing  # camera handler

# create the Flask app
# OceanEye: paths were hardcoded to E:/URPC/... on the author's Windows machine.
# Derived from __file__ so the app runs wherever the folder is copied.
APP_DIR = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(APP_DIR, 'templates')
static_dir = os.path.join(APP_DIR, 'static')
app = Flask(__name__, static_folder=static_dir,
            template_folder=template_dir)
# session secret and storage
# OceanEye: was the literal string 'your_secret_key'. A random one per start is fine
# here — sessions live on disk for one run and nobody needs to stay logged in across a
# restart. Set OCEANEYE_SECRET to keep sessions alive across restarts.
app.config['SECRET_KEY'] = os.environ.get('OCEANEYE_SECRET') or os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
# where uploads are saved
app.config['UPLOAD_FOLDER'] = os.path.join(APP_DIR, 'upload')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# start the session store
Session(app)

# path of the most recently uploaded video
global_last_uploaded_video_path = None

# home page
@app.route('/')
def index():
    # is the user logged in?
    if 'username' in session:
        # logged in: render the home page with their name
        return render_template('index.html', username=session['username'])
    else:
        # not logged in: render the login page
        return render_template('login.html')

# login
# OceanEye: was methods=['GET', 'POST'], which registered a second handler for GET /login
# on top of login_page() below. Werkzeug matched whichever was registered first, so the
# GET branch here was unreachable. One method, one handler.
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # There is no user database. Any username is accepted and the password is ignored —
    # the login screen is part of the advisor's original UI, not a security boundary.
    session['username'] = data.get('username')
    return jsonify({'success': True})

# register a new user — accepted and discarded, for the same reason as login()
@app.route('/register', methods=['POST'])
def register():
    return jsonify({'success': True, 'message': 'Registration successful'})

# reset a password — accepted and discarded, for the same reason as login()
@app.route('/reset_password', methods=['POST'])
def reset_password():
    return jsonify({'success': True})

# render the login page. register.html and reset_password.html link here by name,
# via url_for('login_page').
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# render the register page
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# render the reset-password page
@app.route('/reset_password', methods=['GET'])
def reset_password_page():
    return render_template('reset_password.html')

# log out
@app.route('/logout')
def logout():
    # drop the username from the session
    session.pop('username', None)
    # back to the login page
    return render_template('login.html')

# image upload
@app.route('/upload-image', methods=['POST'])
def upload_image():
    # was a file sent?
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    # the uploaded file
    file = request.files['file']
    # reject an empty filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # save it
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # run detection on it
    # OceanEye: an undecodable upload (HEIC, a renamed .txt) used to reach the model as
    # None and raise, which the page showed as nothing happening at all. Report it instead.
    try:
        output_path = predict_img.detect(file_path)
    except Exception as exc:
        return jsonify({'error': str(exc)})
    # URL of the annotated image, wherever under static/ detect() chose to put it
    output_url = url_for('static', filename=os.path.relpath(output_path, static_dir),
                         _external=True)
    # return that URL
    return jsonify({'url': output_url})

# video upload
@app.route('/upload-video', methods=['POST'])
def upload_video():
    global global_last_uploaded_video_path
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # OceanEye: this body was wrapped in `if file:` with an unreachable error return
    # after it — a FileStorage past the two checks above is always truthy.
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    global_last_uploaded_video_path = file_path
    return jsonify({'message': 'Video uploaded successfully, ready for streaming'})

# video stream
@app.route('/video_feed')
def video_feed():
    global global_last_uploaded_video_path
    if global_last_uploaded_video_path is None:
        return "No video available", 404

    return Response(
        run_video_processing(global_last_uploaded_video_path),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# download the annotated copy of the video that was last uploaded
# predict_video writes it while the stream plays and only names it on the last frame,
# so anything this route can find is a full-length copy of the upload.
@app.route('/download-video')
def download_video():
    if global_last_uploaded_video_path is None:
        ready, message = False, 'Choose a video first.'
    else:
        path = predict_video.export_path(global_last_uploaded_video_path)
        ready = os.path.exists(path)
        message = '' if ready else (
            'Not ready yet. Let the video play through to its last frame — the file is '
            'saved only once the whole video has been processed, so that the download is '
            'never shorter than what you uploaded.')

    # the page asks with ?check first, so clicking too early is an alert on the page
    # rather than the browser navigating off the demo
    if request.args.get('check'):
        return jsonify({'ready': ready, 'message': message})
    if not ready:
        return message, 404
    return send_file(path, as_attachment=True, download_name=os.path.basename(path))

# contrast enhancement on/off — the before/after moment when the water is stirred up
@app.route('/enhance', methods=['POST'])
def toggle_enhance():
    # set on the module, not on an imported name, or enhance() would not see it
    predict_video.ENHANCE = not predict_video.ENHANCE
    return jsonify({'enhance': predict_video.ENHANCE})

@app.route('/camera_feed')
def camera_feed():
    # camera index from the query string
    camera_index = request.args.get('camera_index', type=int)

    # validate it (OceanEye: was `not 0 <= camera_index <= 3` — TypeError when the
    # parameter is missing or non-numeric, because request.args.get returns None)
    if camera_index is None or not 0 <= camera_index <= 3:  # at most 4 cameras
        return "Invalid camera index", 400
        
    return Response(
        run_camera_processing(camera_index),  # pass the camera index through
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
# run the app
if __name__ == '__main__':
    # OceanEye: debug=True turns on the auto-reloader, which restarts the server when any
    # file under it changes — mid-demo that means a 139 MB checkpoint reloading on stage.
    # It also imports torch twice at startup. Off for the demo; errors still print here.
    app.run(host='0.0.0.0', port=8080)