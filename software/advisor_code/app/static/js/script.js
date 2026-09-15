document.addEventListener('DOMContentLoaded', function() {
    const mainTitle = document.querySelector('.content h2');
    const mainDescription = document.querySelector('.content p');

    // click handler for the'Choose Image'button
    document.getElementById('btn-choose-image').addEventListener('click', function() {
        // trigger the hidden image file input
        document.getElementById('imageUpload').click();
    });

    // a video file was chosen
    document.getElementById('videoUpload').addEventListener('change', function(event) {
        // upload it
        uploadFile(event.target.files[0], '/upload-video', 'live-output');
    });

    // an image file was chosen
    document.getElementById('imageUpload').addEventListener('change', function(event) {
        // upload it
        uploadFile(event.target.files[0], '/upload-image', 'image-output');
    });

    // switch to the live monitoring panel
    document.getElementById('btn-live').addEventListener('click', function() {
        mainTitle.classList.add('hidden');
        mainDescription.classList.add('hidden');
        // show the live monitoring panel
        togglePreview('live-preview');
        // hide the image detection panel
        hidePreview('image-preview');
        // hide the camera detection panel
        hidePreview('camera-preview');
        // start the live video stream
        startLiveVideo();
    });

    // switch to the image detection panel
    document.getElementById('btn-image').addEventListener('click', function() {
        mainTitle.classList.add('hidden');
        mainDescription.classList.add('hidden');
        // show the image detection panel
        togglePreview('image-preview');
        // hide the live monitoring panel
        hidePreview('live-preview');
        // hide the camera detection panel
        hidePreview('camera-preview');
        // stop the live video stream
        stopLiveVideo();
    });

    // click handler for the'Choose Video'button
    document.getElementById('btn-source').addEventListener('click', function() {
        // trigger the hidden video file input
        document.getElementById('videoUpload').click();
    });

    // switch to the camera detection panel
    document.getElementById('btn-camera').addEventListener('click', function() {
        mainTitle.classList.add('hidden');
        mainDescription.classList.add('hidden');
        // show the camera detection panel
        togglePreview('camera-preview');
        // hide the live monitoring panel
        hidePreview('live-preview');
        // hide the image detection panel
        hidePreview('image-preview');
        // stop the live video stream
        stopLiveVideo();
    });

    // start camera detection
    document.getElementById('btn-camera-start').addEventListener('click', function() {
        // which camera was selected
        const cameraIndex = document.getElementById('camera-select').value;
        // start detecting on it
        startCameraFeed(cameraIndex);
    });

    // show the clock now, then tick it every second
    updateCurrentTime();        
    setInterval(updateCurrentTime, 1000);

    // start live playback
    function startLiveVideo() {
        // the live video element
        let liveVideo = document.getElementById('live-video');
        // if a source is set, show it and play
        if (liveVideo.src) {
            liveVideo.classList.remove('hidden');
            liveVideo.play();
        }
    }

    // stop live playback
    function stopLiveVideo() {
        // the live video element
        let liveVideo = document.getElementById('live-video');
        // pause if the element exists
        if (liveVideo) {
            liveVideo.pause();
        }
    }

    // update the clock
    function updateCurrentTime() {
        // now
        const now = new Date();
        // as a local time string
        const timeStr = now.toLocaleTimeString();
        // write it to the page
        document.getElementById('current-time').innerText = timeStr;
    }

    // toggle a preview area
    function togglePreview(previewId) {
        // the named preview element
        let preview = document.getElementById(previewId);
        // flip its visibility
        preview.classList.toggle('hidden');
    }

    // hide a preview area
    function hidePreview(previewId) {
        // the named preview element
        let preview = document.getElementById(previewId);
        // only if it is currently visible
        if (!preview.classList.contains('hidden')) {
            preview.classList.add('hidden');
        }
    }

    // shared upload helper
    function uploadFile(file, url, outputId) {
        // build the form data
        let formData = new FormData();
        // attach the file
        formData.append('file', file);
    
        // POST it to the server
        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // video upload
            if (url === '/upload-video') {
                // the live video element
                let liveVideo = document.getElementById('live-video');
                // point the player at the stream
                liveVideo.src = '/video_feed';
                // show the player
                liveVideo.classList.remove('hidden');
            } else if (data.url) {
                // image upload: show the returned image
                displayImage(data.url, 'img-put');
            } else {
                console.error('No URL returned from server');
            }
        })
        .catch(error => console.error('Error:', error));
    }
    
    // show an uploaded image
    function displayImage(imageUrl, imageElementId) {
        // the img element
        let imageElement = document.getElementById(imageElementId);
        // point it at the returned URL
        imageElement.src = imageUrl;
        // show it
        imageElement.classList.remove('hidden');
    }   
    
    // open the login dialog
    document.getElementById('login-btn').addEventListener('click', function() {
        document.getElementById('loginModal').style.display = 'block';
    });

    // login form submit
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        // stop the form submitting normally
        event.preventDefault();
        // read the username and password
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // POST to the login endpoint
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            // logged in
            if (data.success) {
                // show the username
                document.getElementById('username-display').textContent = username;
                // swap the log-in button for the log-out button
                document.getElementById('user-info').classList.remove('hidden');
                document.getElementById('login-btn').classList.add('hidden');
                document.getElementById('logout-btn').classList.remove('hidden');
                // close the dialog
                document.getElementById('loginModal').style.display = 'none';
            } else {
                // otherwise show the error
                alert('Login failed: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Login error:', error);
        });
    });

    // log out
    document.getElementById('logout-btn').addEventListener('click', function() {
        // call the logout endpoint
        fetch('/logout')
        .then(response => {
            // reload once logged out
            window.location.reload();
        });
    });

    // close the login dialog
    document.getElementsByClassName('close-button')[0].addEventListener('click', function() {
        document.getElementById('loginModal').style.display = 'none';
    });

    // start the camera stream
    function startCameraFeed(cameraIndex) {
        const cameraOutput = document.getElementById('camera-output');
        cameraOutput.innerHTML = ''; // clear the previous stream

        const cameraVideo = document.createElement('img');
        cameraVideo.id = 'camera-video';
        cameraVideo.src = `/camera_feed?camera_index=${cameraIndex}`;
        cameraVideo.classList.remove('hidden');

        cameraOutput.appendChild(cameraVideo);
    }
    
    // added to script.js
    let lastFrameTime = 0;
    let streamActive = true;
    
    function updateStream() {
        const streamImg = document.getElementById('live-stream');
        
        // cache-bust the stream URL
        streamImg.src = "{{ url_for('video_feed') }}?t=" + Date.now();
        
        // performance readout
        const now = Date.now();
        if (lastFrameTime > 0) {
            document.getElementById('latency').textContent = now - lastFrameTime;
        }
        lastFrameTime = now;
        
        // refresh the resolution readout
        streamImg.onload = () => {
            document.getElementById('resolution').textContent = 
                `${streamImg.naturalWidth}x${streamImg.naturalHeight}`;
        };
        
        if(streamActive) {
            requestAnimationFrame(updateStream);
        }
    }
    
    // start the refresh loop
    document.getElementById('btn-live').addEventListener('click', () => {
        streamActive = true;
        updateStream();
    });
    
    // stop button
    document.getElementById('btn-stop').addEventListener('click', () => {
        streamActive = false;
        document.getElementById('live-stream').src = '';
    });

});
