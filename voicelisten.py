import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get the available voices
voices = engine.getProperty('voices')

# List all available voices and their properties
for index, voice in enumerate(voices):
    print(f"Voice {index}: {voice.name} ({voice.languages})")

# Select a voice based on its index or properties (e.g., a female voice)
# For example, selecting the second voice (index 1) which could be Zara or another female voice
engine.setProperty('voice', voices[1].id)

# Adjust speech rate and volume
engine.setProperty('rate', 140)  # Speed of speech
engine.setProperty('volume', 0.5)  # Volume (0.0 to 1.0)

# Test the selected voice
engine.say("Hello! This is the voice you selected.")
engine.runAndWait()
