import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import langid

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

def detect_language(text):
    # Used langid library to detect language
    lang, _ = langid.classify(text)
    return lang

def setup_recording(filename=None, device=None, samplerate=None, supported_languages=["en", "hi"]):
    """Set up recording parameters and start recording loop."""
    try:
        if samplerate is None:
            device_info = sd.query_devices(device, "input")
            samplerate = int(device_info["default_samplerate"])


        if filename:
            dump_fn = open(filename, "wb")
        else:
            dump_fn = None

        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                               dtype="int16", channels=1, callback=callback):
            print("#" * 80)
            print("Press Ctrl+C to stop the recording")
            print("#" * 80)

            while True:
                data = q.get()
                # Detect language of the speech
                detected_lang = detect_language(data)

                if detected_lang in supported_languages:
                    model = Model(lang=detected_lang)
                    rec = KaldiRecognizer(model, samplerate)

                    if rec.AcceptWaveform(data):
                        print(rec.Result())
                    else:
                        print(rec.PartialResult())
                if dump_fn is not None:
                    dump_fn.write(data)

    except KeyboardInterrupt:
        print("\nDone")
        sys.exit(0)
    except Exception as e:
        sys.exit(type(e).__name__ + ": " + str(e))

if __name__ == "__main__":
    # Example usage
    setup_recording()
