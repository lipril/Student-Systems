const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('capture');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.srcObject = stream; })
    .catch(err => console.error('Error accessing webcam:', err));

captureBtn.addEventListener('click', () => {
    const ctx = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);
    const imageData = canvas.toDataURL('image/png');
    // Send to server
    const form = document.getElementById('loginForm');
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'image_data';
    input.value = imageData;
    form.appendChild(input);
    form.submit();
});