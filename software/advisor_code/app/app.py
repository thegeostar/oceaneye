from flask import Flask, request, jsonify, send_file, render_template, session, url_for, Response
from flask_session import Session
import os
import cv2

# supporting modules
from werkzeug.utils import secure_filename
import predict_img
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
roi_points = None

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
    output_path = predict_img.detect(file_path)
    # URL of the annotated image
    output_url = url_for('static', filename=os.path.basename(output_path), _external=True)
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

# set the region of interest
@app.route('/set_roi', methods=['POST'])
def set_roi():
    global roi_points
    data = request.get_json()
    roi_points = data.get('roi')
    return jsonify({'message': 'ROI set successfully'})

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
'''
@app.route('/camera_feed')
def camera_feed():
    """Video stream route."""
    # camera argument: either a numeric index or an RTSP URL
    camera_source = request.args.get(
        'camera_index', 
)
    
    # work out which one it is
    if isinstance(camera_source, str) and camera_source.isdigit():
        camera_source = int(camera_source)
    elif camera_source.startswith("rtsp://"):
        pass  # use the RTSP URL as-is
    else:
        return jsonify({"error": "Invalid camera source"}), 400
    
    # hand off to the camera handler
    return Response(
        run_camera_processing(camera_source),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
'''
# run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)