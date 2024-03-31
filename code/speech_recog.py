from flask import Flask, Response, render_template, request, jsonify
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import warnings
import time
import json
from gramformer import Gramformer

app = Flask(__name__)

# Initialize Gramformer and other variables
gf = Gramformer(models=2, use_gpu=False)  # Initialize LLAMA 2 for grammar correction
q = queue.Queue()
recording = False
last_audio_time = time.time()   # Initialize the last_audio_time variable with the current time

def callback(indata, frames, timestamp, status):
    """This is called (from a separate thread) for each audio block."""
    global last_audio_time
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))
    last_audio_time = time.time()  # Update last_audio_time each time audio data is received

# Function to correct grammar using Gramformer (LLAMA 2)
def get_grammar_correction(text):
    try:
        print('Correcting grammar...')
        corrected_text = gf.correct(text)
        return corrected_text
    except Exception as e:
        print('Error in get_grammar_correction:', e)
        return text

# Function to set up recording parameters and start recording loop
def setup_recording(filename=None, device=None, samplerate=None, model_lang="en-us"):
    """Set up recording parameters and start recording loop."""
    global last_audio_time
    try:        
        if samplerate is None:
            device_info = sd.query_devices(device, "input")
            samplerate = int(device_info["default_samplerate"])

        model = Model(lang=model_lang)

        if filename:
            dump_fn = open(filename, "wb")
        else:
            dump_fn = None

        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                               dtype="int16", channels=1, callback=callback):
            print("#" * 80)
            print("Press Ctrl+C to stop the recording")
            print("#" * 80)

            rec = KaldiRecognizer(model, samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()

                    # Correct text using Gramformer (LLAMA 2)
                    corrected_text = get_grammar_correction(result)  
                    if len(corrected_text) > 0:
                        yield corrected_text 
                    else:
                        yield result
                
                if time.time() - last_audio_time > 10:
                    print("Silence detected, stopping recording...")
                    recording = False
                    break
    except KeyboardInterrupt:
        print("\nDone")
        sys.exit(0)
    except Exception as e:
        print('Error in setup_recording:', e)
        return jsonify({'error': str(e)})

# Route to stream audio
@app.route('/stream_audio')
def stream_audio():
    global recording
    print('Starting audio stream')
    recording = True
    try:
        recording_generator = setup_recording()
        return Response(recording_generator, content_type='text/event-stream')
    except Exception as e:
        print('Error in stream_audio:', e)
        return jsonify({'error': str(e)})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():  # Wrap operations that require the application context
        app.run(debug=True)
