import pyttsx3

def speak_ssml(ssml):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust the speech rate if needed
    engine.say(ssml)
    engine.runAndWait()

ssml = """
<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/10/synthesis http://www.w3.org/TR/speech-synthesis/synthesis.xsd" version="1.0">
  <p>This is a paragraph with <emphasis level="strong">strong emphasis</emphasis>.</p>
  <p>This is a paragraph with <emphasis level="moderate">moderate emphasis</emphasis>.</p>
  <p>This is a paragraph with <emphasis level="reduced">reduced emphasis</emphasis>.</p>
  <p>This is a paragraph with <prosody pitch="high">high pitch</prosody>.</p>
  <p>This is a paragraph with <prosody rate="fast">fast rate</prosody>.</p>
  <p>This is a paragraph with <prosody volume="loud">loud volume</prosody>.</p>
</speak>
"""

speak_ssml(ssml)

