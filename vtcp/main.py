import azure.cognitiveservices.speech as speechsdk
import pyperclip
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
        self.is_terminal = sys.stdout.isatty()
        
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.subscription_key, 
            region=self.region
        )
        self.speech_config.speech_recognition_language = "es-ES"
        
        self.sound_path = os.path.join(os.path.dirname(__file__), 'assets', 'chord.wav')

    def handle_signal(self, signum, frame):
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
            console.print("\n🎤 [bold green]Escuchando...[/]")
            console.print("   Habla ahora. Ctrl+C para cancelar")


        audio_config = speechsdk.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, 
            audio_config=audio_config
        )

        # Configurar manejo de resultados parciales
        recognized_text = ""
        
        def recognizing_handler(evt):
            nonlocal recognized_text
            if evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
                recognized_text = evt.result.text
                if self.is_terminal:
                    console.print(f"🔍 [dim]{evt.result.text}[/]", end="\r")

        recognizer.recognizing.connect(recognizing_handler)

        #play sound to star talking
        self.play_sound()
        try:
            result = recognizer.recognize_once_async().get()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                pyperclip.copy(result.text)
                self.play_sound()
                if self.is_terminal:
                    console.print(f"\n✨ [bold blue]Copiado:[/] {result.text}")
            elif result.reason == speechsdk.ResultReason.NoMatch:
                if self.is_terminal:
                    console.print("\n🟠 [bold yellow]No se detectó voz[/]")
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                if self.is_terminal:
                    console.print(f"\n🔴 [bold red]Error:[/] {cancellation_details.error_details}")

        except KeyboardInterrupt:
            if self.is_terminal:
                console.print("\n🟡 [bold yellow]Operación cancelada[/]")
            return

def main():
    try:
        stt = Vtcp()
        stt.capture_and_copy()
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        if sys.stdout.isatty():
            console.print(f"[bold red]{error_msg}[/]")
        else:
            print(error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()
