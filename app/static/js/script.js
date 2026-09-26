document.addEventListener('DOMContentLoaded', function () {
    const intro = document.querySelectorAll('.hero-content h2, .hero-content p');
    const panels = ['live-preview', 'image-preview', 'camera-preview'];

    function showPanel(id) {
        intro.forEach(el => el.classList.add('hidden'));
        panels.forEach(p => document.getElementById(p).classList.toggle('hidden', p !== id));
    }

    document.getElementById('btn-live').addEventListener('click', () => showPanel('live-preview'));
    document.getElementById('btn-image').addEventListener('click', () => showPanel('image-preview'));
    document.getElementById('btn-camera').addEventListener('click', () => showPanel('camera-preview'));

    document.getElementById('btn-source').addEventListener('click', () => {
        document.getElementById('videoUpload').click();
    });
    document.getElementById('btn-choose-image').addEventListener('click', () => {
        document.getElementById('imageUpload').click();
    });
    document.getElementById('videoUpload').addEventListener('change', event => {
        uploadFile(event.target.files[0], '/upload-video');
    });
    document.getElementById('imageUpload').addEventListener('change', event => {
        uploadFile(event.target.files[0], '/upload-image');
    });

    document.getElementById('btn-camera-start').addEventListener('click', () => {
        const feed = document.createElement('img');
        feed.id = 'camera-video';
        feed.src = '/camera_feed?camera_index=' + document.getElementById('camera-select').value;
        document.getElementById('camera-output').replaceChildren(feed);
    });

    // The recording exists only after the whole video has played, so check before downloading.
    document.getElementById('btn-download-video').addEventListener('click', event => {
        event.preventDefault();
        fetch('/download-video?check=1')
            .then(response => response.json())
            .then(data => data.ready ? window.location.assign('/download-video') : alert(data.message))
            .catch(error => console.error('Download check failed:', error));
    });

    document.getElementById('btn-download-image').addEventListener('click', function (event) {
        if (!this.getAttribute('href')) {
            event.preventDefault();
            alert('Detect an image first.');
        }
    });

    document.getElementById('btn-enhance').addEventListener('click', function () {
        fetch('/enhance', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                this.textContent = 'Enhancement: ' + (data.enhance ? 'ON' : 'OFF');
                this.style.backgroundColor = data.enhance ? '#2a7d5a' : '';
            })
            .catch(error => console.error('Enhance toggle failed:', error));
    });

    const clock = document.getElementById('current-time');
    const tick = () => { clock.textContent = new Date().toLocaleTimeString(); };
    tick();
    setInterval(tick, 1000);

    function uploadFile(file, url) {
        const formData = new FormData();
        formData.append('file', file);
        fetch(url, { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Upload failed: ' + data.error);
                } else if (url === '/upload-video') {
                    // A fresh query string restarts the stream when the same URL is reused.
                    document.getElementById('live-video').src = '/video_feed?t=' + Date.now();
                } else {
                    showImage(data.url);
                }
            })
            .catch(error => console.error('Upload failed:', error));
    }

    function showImage(url) {
        document.getElementById('img-put').src = url;
        const link = document.getElementById('btn-download-image');
        link.href = url;
        link.download = url.split('/').pop();
    }
});
