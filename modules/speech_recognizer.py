import speech_recognition as sr

class SpeechRecognizer:
    def __init__(
        self, 
        language="en-US", 
        verbose=True    
    ):
        self.verbose = verbose   # Toggle for debug messages
        self.is_listening = True # Toggle to turn on and off the recognizer
        self.language = language # Recognizer language

        # Create a recognizer and microphone instance
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Queue of recognized speech messages
        self.speech_queue = []

        # Listen in the background stop function
        self.stop_listen_in_background = False

    def process_audio(self, _, audio):
        try:
            # Recognize the speech using Google's Speech Recognition API
            recognized_speech = self.recognizer.recognize_google(audio, language=self.language)
            self.speech_queue.append(recognized_speech)

        except sr.UnknownValueError:
            if self.verbose: print("Sorry, I didn't catch that. Can you repeat?")

        except sr.RequestError:
            if self.verbose: print(f"Could not request results from Google Speech Recognition service")

    def start_listening(self):
        # Use the microphone as the audio source
        with self.microphone as source:
            # Adjust for ambient noise
            if self.verbose: print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
        # Start listening
        if self.verbose: print("Listening for speech...")
        self.stop_listen_in_background = self.recognizer.listen_in_background(self.microphone, self.process_audio)

    def stop_listening(self):
        if self.stop_listen_in_background:
            # Stop listen_in_background and toggle its function flag to false
            self.stop_listen_in_background()
            self.stop_listen_in_background = False

            if self.verbose: print("Stopped listening.")

    def get_speech(self):
        # Delete and return the first element of the queue
        if self.speech_queue:
            return self.speech_queue.pop()
        
        # Return an empty string if the queue is empty
        else:
            return ""