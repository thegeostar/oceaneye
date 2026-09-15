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

    // contrast enhancement on/off. Default OFF — measured to cost detections in clear
    // water and to rescue them once the water is stirred up. See predict_video.enhance().
    document.getElementById('btn-enhance').addEventListener('click', function() {
        const btn = this;
        fetch('/enhance', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                btn.textContent = 'Enhancement: ' + (data.enhance ? 'ON' : 'OFF');
                btn.style.backgroundColor = data.enhance ? '#2a7d5a' : '';
            })
            .catch(error => console.error('Enhance toggle failed:', error));
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
                // OceanEye: was a console.error, so a rejected upload looked on stage like
                // the button simply doing nothing. Say so where the operator can see it.
                alert('Detection failed: ' + (data.error || 'no image returned'));
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
    
    // OceanEye: a login-modal block used to sit here — #login-btn, #loginForm, #loginModal,
    // #logout-btn, .close-button. None of those elements exist in index.html, which is the
    // only page that loads this file, so getElementById returned null and the very first
    // line threw a TypeError on every page load, killing every handler registered below it.
    // The real login lives in its own inline script in templates/login.html. Deleted.

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

    // OceanEye: an updateStream() refresh loop used to sit here, wired to #btn-live and
    // #btn-stop. It built an <img> src out of a Jinja url_for tag written inline in this
    // file — but Flask serves static/ verbatim and never renders it, so the browser asked
    // for that literal tag text. On requestAnimationFrame that is a 404 at 60 Hz.
    // #btn-stop, #live-stream, #latency and #resolution do not exist either. Deleted; the
    // video tab streams through #live-video, set in uploadFile() above.
    // test_dom_ids.py now fails if either mistake comes back.
});
