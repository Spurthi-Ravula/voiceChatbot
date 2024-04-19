import streamlit as st
import speech_recognition as sr
from main import genai_engine
import pyttsx3

st.title("AI-Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Voice Input
st.sidebar.title("Voice Input")

def record_audio(filename):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.sidebar.write("Recording...")
        audio = r.listen(source)
        st.sidebar.write("Finished Recording!")

        try:
            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())
            return True
        except Exception as e:
            st.sidebar.write(f"Error: {e}")
            return False

record_button = st.sidebar.button("Record Voice")

if record_button:
    st.session_state.messages.append({"role": "user", "content": "Voice Input"})
    success = record_audio("input_audio.wav")
    if not success:
        st.sidebar.write("Error recording audio. Please check your microphone.")
    else:
        # If voice recording is successful, process the audio
        r = sr.Recognizer()
        with sr.AudioFile("input_audio.wav") as source:
            audio_data = r.record(source)
        try:
            user_input = r.recognize_google(audio_data)
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = genai_engine(user_input)

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Generate audio output
            try:
                engine = pyttsx3.init()
                engine.save_to_file(response, "output_audio.wav")
                engine.runAndWait()
            except Exception as e:
                st.sidebar.write(f"Error generating audio output: {e}")
        except sr.UnknownValueError:
            st.sidebar.write("Could not understand audio")
        except sr.RequestError as e:
            st.sidebar.write(f"Error fetching results; {e}")

# Chat Input
if prompt := st.text_input("Type a message:"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = genai_engine(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Generate audio output
    try:
        engine = pyttsx3.init()
        engine.save_to_file(response, "output_audio.wav")
        engine.runAndWait()
    except Exception as e:
        st.sidebar.write(f"Error generating audio output: {e}")

# Voice Output
st.sidebar.title("Voice Output")

play_button = st.sidebar.button("Play Voice Output")

if play_button:
    try:
        with open("output_audio.wav", "rb") as audio_file:
            audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/wav")
    except FileNotFoundError:
        st.sidebar.write("No voice output available.")
