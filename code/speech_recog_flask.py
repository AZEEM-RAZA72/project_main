from flask import Flask, Response, render_template
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer

app = Flask(__name__)

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def list_audio_devices():
    """List available audio devices and exit."""
    print(sd.query_devices())
    sys.exit(0)

def setup_recording(filename=None, device=None, samplerate=None, model_lang="en-us"):
    """Set up recording parameters and start recording loop."""
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
                    print(result)
                    yield f"data: {result}\n\n"  # Yield the result as a server-sent event
                else:
                    partial_result = rec.PartialResult()
                    print(partial_result)
                    yield f"data: {partial_result}\n\n"  # Yield the partial result
                if dump_fn is not None:
                    dump_fn.write(data)

    except KeyboardInterrupt:
        print("\nDone")
        sys.exit(0)
    except Exception as e:
        sys.exit(type(e).__name__ + ": " + str(e))

@app.route('/stream_audio')
def stream_audio():
    print('Starting audio stream')
    return Response(setup_recording(), content_type='text/event-stream')

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)
