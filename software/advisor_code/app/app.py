from flask import Flask, request, jsonify, render_template, session, url_for, Response
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
app.config['SECRET_KEY'] = 'your_secret_key'  # replace with a real secret
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
@app.route('/login', methods=['GET', 'POST'])
def login():
    # POST: the submitted credentials
    if request.method == 'POST':
        # read the JSON body
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # user verification would go here
        # assumed to pass
        session['username'] = username
        return jsonify({'success': True})

    # GET: render the login page
    return render_template('login.html')

# register a new user
@app.route('/register', methods=['POST'])
def register():
    # read the JSON body
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # user registration would go here
    return jsonify({'success': True, 'message': 'Registration successful'})

# reset a password
@app.route('/reset_password', methods=['POST'])
def reset_password():
    # read the JSON body
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')

    # password reset would go here
    return jsonify({'success': True})

# render the login page
# Looks redundant with login() above, which already renders this on GET — but it is a named
# endpoint: register.html and reset_password.html both link via url_for('login_page').
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

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        global_last_uploaded_video_path = file_path
        return jsonify({'message': 'Video uploaded successfully, ready for streaming'})
    
    return jsonify({'error': 'No file uploaded'}), 400

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