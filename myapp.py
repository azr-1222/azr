import kivy
kivy.require('2.3.0')  # Ensure you are using Kivy 2.3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation
import speech_recognition as sr
import pyttsx3

class VoiceAssistantApp(App):
    def build(self):
        # Initialize voice recognition and text-to-speech engine
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

        # Create layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Status label
        self.status_label = Label(
            text="Press 'Listen' to start speaking",
            size_hint_y=None,
            height=44
        )
        layout.add_widget(self.status_label)

        # Listen button
        self.listen_button = Button(
            text="listen",
            size_hint_y=None,
            height=44
        )
        self.listen_button.bind(on_press=self.on_listen_button_press)
        layout.add_widget(self.listen_button)

        return layout

    def on_listen_button_press(self, instance):
        # Animate the button on press
        animation = Animation(size=(200, 50), duration=0.2) + Animation(size=(150, 44), duration=0.2)
        animation.start(self.listen_button)
        
        # Update the status label and process voice command
        self.status_label.text = "Listening..."
        command = self.listen()
        if command:
            if "stop" in command.lower():
                self.speak("Goodbye!")
                self.status_label.text = "Goodbye! Closing app."
                self.stop()
            else:
                response = f"You said: {command}"
                self.speak(response)
                self.status_label.text = response
        else:
            self.status_label.text = "Sorry, I did not understand that."

    def listen(self):
        # Capture and recognize speech
        with sr.Microphone() as source:
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio)
                return command
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                return None

    def speak(self, text):
        # Convert text to speech
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    VoiceAssistantApp().run()
