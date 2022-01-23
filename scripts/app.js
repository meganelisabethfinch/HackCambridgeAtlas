var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

var messageChatBox = document.getElementById("chatbox");

function startRecording() {
	console.log("recordButton clicked");

	/*
		Simple constraints object, for more advanced audio features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/
    
    var constraints = { audio: true, video:false }

 	/*
    	Disable the record button until we get a success or fail from getUserMedia() 
	*/

	recordButton.disabled = true;
	stopButton.disabled = false;
	pauseButton.disabled = false

	/*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device
		*/
		audioContext = new AudioContext();


		/*  assign to gumStream for later use  */
		gumStream = stream;
		
		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);

		/* 
			Create the Recorder object and configure to record mono sound (1 channel)
			Recording 2 channels  will double the file size
		*/
		rec = new Recorder(input,{numChannels:1})

		//start the recording process
		rec.record()

		console.log("Recording started");

	}).catch(function(err) {
	  	//enable the record button if getUserMedia() fails
    	recordButton.disabled = false;
    	stopButton.disabled = true;
    	pauseButton.disabled = true
	});
}

function pauseRecording(){
	console.log("pauseButton clicked rec.recording=",rec.recording );
	if (rec.recording){
		//pause
		rec.stop();
		pauseButton.innerHTML="Resume";
	}else{
		//resume
		rec.record()
		pauseButton.innerHTML = "Pause";

	}
}

function stopRecording() {
	console.log("stopButton clicked");

	//disable the stop button, enable the record too allow for new recordings
	stopButton.disabled = true;
	recordButton.disabled = false;
	pauseButton.disabled = true;

	//reset button just in case the recording is stopped while paused
	pauseButton.innerHTML = "Pause";
	
	//tell the recorder to stop the recording
	rec.stop();

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to upload
	rec.exportWAV(upload);
}

function upload(blob) {
	//name of .wav file to use during upload (without extension)
	var filename = new Date().toISOString();
	
	// Upload
	var xhr = new XMLHttpRequest();
	xhr.onload = function(e) {
		if(this.readyState === 4) {
			console.log("Server returned: ", e.target.responseText);
			var decoded_string = JSON.parse(e.target.responseText);
			addToChat(decoded_string.ai, decoded_string.time, decoded_string.user);
		}
	};
	var fd = new FormData();
	fd.append("audio_data", blob, filename);
	xhr.open("POST","../../upload",true);
	xhr.send(fd);
}

function addToChat(response, time, user_input=undefined) {
	if(user_input) {
		let userDiv = document.createElement("div");
		let userA = document.createElement("a");
		userDiv.className = "text-right mb-2"
		userA.className = "bg-primary text-white rounded rounded-pill py-2 px-4";
		userA.innerHTML = user_input;
		userDiv.appendChild(userA);
		messageChatBox.appendChild(userDiv);
	}

	let botDiv = document.createElement("div");
	let botA = document.createElement("a");
    botDiv.className = "text-left mb-2";
	botA.className = "bg-secondary text-white rounded rounded-pill py-2 px-4";
    botA.innerHTML = response;
	botDiv.appendChild(botA);
    messageChatBox.appendChild(botDiv);

	var audio = new Audio('../temp/tts'+time+'.wav');
	audio.play();
}

document.addEventListener('DOMContentLoaded', function() {
    var xhr = new XMLHttpRequest();
	xhr.onload = function(e) {
		if(this.readyState === 4) {
			var decoded_string = JSON.parse(e.target.responseText);
			addToChat(decoded_string.ai);
		}
	};
	var fd = new FormData();
	xhr.open("POST","../../initial_prompt",true);
	xhr.send(fd);
}, false);
