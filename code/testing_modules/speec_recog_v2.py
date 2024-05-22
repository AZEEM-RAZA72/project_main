from flask import Flask, Response, render_template,Request, request, jsonify
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from gramformer import Gramformer
import spacy
import json
import time
from threading import Thread    
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


app = Flask(__name__)

q = queue.Queue()

recording = False
# Global variable to track the last time audio was received
last_audio_time = time.time()   # Initialize the last_audio_time variable with the current time


gf = Gramformer(models=1,use_gpu=False) # 0 = detector, 1 = highlighter, 2 = corrector, 3 = all
nlp=spacy.load('en_core_web_lg')

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, timestamp, status):
    """This is called (from a separate thread) for each audio block."""
    global last_audio_time
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))
    last_audio_time = time.time()  # Update last_audio_time each time audio data is received

def list_audio_devices():
    """List available audio devices and exit."""
    print(sd.query_devices())
    sys.exit(0)

    

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

                    # yield result
                    corrected_text = get_grammar_correction(result)  # Send the recorded text for grammar correction
                    if len(corrected_text) > 0:
                        yield corrected_text # Yield the result and corrected text as a server-sent event
                    else:
                        yield result
                
                if time.time() - last_audio_time > 10:
                    print("Silence detected, stopping recording...")
                    recording = False
                    break
                '''if not recording:
                    print("Recording stopped")
                    break
                if dump_fn is not None:
                    dump_fn.write(data)'''

    except KeyboardInterrupt:
        print("\nDone")
        sys.exit(0)
    except Exception as e:
        print('Error in setup_recording:', e)
        return jsonify({'error': str(e)})

@app.route('/correct-grammar', methods=['POST'])
def correct_grammar():
    try:
        data = request.json.get('text')
        corrected_text = get_grammar_correction(data)
        return jsonify({'original_text': data, 'corrected_text': corrected_text})
    except Exception as e:
        return jsonify({'error': str(e)})

def get_grammar_correction(text):
    try:
        print('Correcting grammar...')
        text = json.loads(text).get('text')
        for token in nlp(text):
            if token.text.lower() == 'i':
                text = text.replace(token.text, 'I')
        corrected_text = gf.correct(text)
        return corrected_text
    except Exception as e:
        print(e)
        print('Error in get_grammar_correction:')
        return text

    
@app.route('/stream_audio')
def stream_audio():
    global recording
    print('Starting audio stream')
    recording = True
    # Thread(target=setup_recording).start() # Start recording in a separate thread
    try:
        #return Response(setup_recording(), content_type='text/event-stream')
        recording_generator = setup_recording()
        return Response(recording_generator, content_type='text/event-stream')
    except Exception as e:
        print('Error in stream_audio:', e)
        return jsonify({'error': str(e)})

@app.route('/stop_recording')
def stop_recording():
    global recording
    recording = False  # Stop recording
    return 'Recording stopped'

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)
