import azure.cognitiveservices.speech as speechsdk
import pyperclip
import numpy as np
import sounddevice as sd
from rich.console import Console
import time
from dotenv import load_dotenv
import os
import signal
import simpleaudio as sa
import sys

console = Console()

class Vtcp:
    def __init__(self):
        load_dotenv()
        
        self.subscription_key = os.getenv('AZURE_SPEECH_KEY')
        self.region = os.getenv('AZURE_SPEECH_REGION')
        
        if not self.subscription_key or not self.region:
            print("Error: Falta configurar AZURE_SPEECH_KEY o AZURE_SPEECH_REGION en .env")
            sys.exit(1)
            
        self.should_stop = False
        self.silence_threshold = 0.1
        self.silence_duration = 2.0
        self.last_sound_time = time.time()
        self.is_terminal = sys.stdout.isatty()
        
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.subscription_key, 
            region=self.region
        )
        self.speech_config.speech_recognition_language = "es-ES"
        
        self.sound_path = os.path.join(os.path.dirname(__file__), 'assets', 'chord.wav')

    def handle_signal(self, signum, frame):
        self.should_stop = True

    def audio_callback(self, indata, frames, time_info, status):
        volume_norm = np.linalg.norm(indata) / frames
        if volume_norm > self.silence_threshold:
            self.last_sound_time = time.time()
        elif time.time() - self.last_sound_time > self.silence_duration:
            self.should_stop = True

    def play_sound(self):
        try:
            if not os.path.exists(self.sound_path):
                return
            wave_obj = sa.WaveObject.from_wave_file(self.sound_path)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        except Exception:
            pass
        
    def capture_and_copy(self):
        self.should_stop = False
        
        if self.is_terminal:
            signal.signal(signal.SIGINT, self.handle_signal)
        
       
        
        with sd.InputStream(callback=self.audio_callback):
            audio_config = speechsdk.AudioConfig(use_default_microphone=True)
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config, 
                audio_config=audio_config
            )
            if self.is_terminal:
                console.print("🎤 [bold green]Grabando...[/]")
                console.print("   Ctrl+C para terminar o espera 2s de silencio")
            
            self.play_sound()
            while not self.should_stop:
                result = recognizer.recognize_once_async().get()
                
                if result.text:
                    pyperclip.copy(result.text)
                    self.play_sound()
                    if self.is_terminal:
                        console.print(f"✨ [bold blue]Copiado:[/] {result.text}")
                    break

def main():
    try:
        stt = Vtcp()
        stt.capture_and_copy()
    except KeyboardInterrupt:
        if sys.stdout.isatty():
            console.print("\n[yellow]Grabación cancelada[/]")
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        if sys.stdout.isatty():
            console.print(f"[bold red]{error_msg}[/]")
        else:
            print(error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()