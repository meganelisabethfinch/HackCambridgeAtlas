const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');

const handleSuccess = function(stream) {
  const options = {mimeType: 'audio/webm'};
  const recordedChunks = [];
  const mediaRecorder = new MediaRecorder(stream, options);

  mediaRecorder.addEventListener('dataavailable', function(e) {
    if (e.data.size > 0) recordedChunks.push(e.data);
  });

  mediaRecorder.addEventListener('stop', function() {
    console.log(URL.createObjectURL(new Blob(recordedChunks)));
  });

  startButton.addEventListener('click', function() {
    mediaRecorder.start();
  });

  stopButton.addEventListener('click', function() {
    mediaRecorder.stop();
  });
  
};

navigator.mediaDevices.getUserMedia({ audio: true, video: false })
    .then(handleSuccess);
