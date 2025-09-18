import streamlit as st
import speech_recognition as sr
import pyttsx3 as pt
import random
import webbrowser
import urllib.parse
import base64

recognizer = sr.Recognizer()

# --- add local background ---
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("data:image/jpg;base64,{encoded}");
             background-attachment: fixed;
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_local(r"C:\Users\nikhi\PycharmProjects\NARESH_IT\PROJECTS_NARESH_IT\Speech_Recognition\wallpaperflare.com_wallpaper.jpg")

# --- init engine once, set female voice ---
engine = pt.init()
voices = engine.getProperty("voices")
female_voice = None
for v in voices:
    if "female" in v.name.lower() or "zira" in v.name.lower():
        female_voice = v.id
        break
if female_voice:
    engine.setProperty("voice", female_voice)

def speak(text: str):
    engine.say(text)
    engine.runAndWait()

# witty responses
witty_replies = {
    "play": [
        "Lyra here, firing up {song}.",
        "Alright, {song} coming right up.",
        "Spinning up {song}."
    ],
    "fallback": [
        "Lyra heard: {cmd}. Not sure what to do with that, but hey, I’m trying.",
        "So you said: {cmd}. Either that was deep… or my circuits are confused.",
        "Heard you loud and clear: {cmd}. No idea what to do with it though."
    ],
    "error": [
        "Uh oh, Lyra didn’t catch that. Try again, slower this time.",
        "I can’t process silence. Speak up!",
        "Either you said nothing, or my ears glitched. Let’s try again."
    ]
}

def witty_choice(category, **kwargs):
    return random.choice(witty_replies[category]).format(**kwargs)

# open YouTube search directly
def play_song(song: str):
    query = urllib.parse.quote(song)
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)   # opens in default browser
    return url

def hear():
    cmd = ""
    try:
        with sr.Microphone() as mic:
            st.info("🎤 Listening... (say: 'Lyra play ...')")
            voice = recognizer.listen(mic, timeout=5, phrase_time_limit=5)
            cmd = recognizer.recognize_google(voice).lower()
            if "lyra" in cmd:
                cmd = cmd.replace("lyra", "").strip()
    except Exception as e:
        cmd = f"Error: {e}"
    return cmd

def process_command(cmd: str):
    st.write(f"Command: `{cmd}`")

    if "play" in cmd:
        song = cmd.replace("play", "").strip()
        url = play_song(song)                       # open YouTube first
        response = witty_choice("play", song=song)
        speak(response)                             # then speak
        st.success(f"▶ {response}")
        st.markdown(f"[Open YouTube for {song}]({url})")

    elif cmd.startswith("Error"):
        response = witty_choice("error")
        speak(response)
        st.error(response)

    elif cmd:
        response = witty_choice("fallback", cmd=cmd)
        speak(response)
        st.info(response)

# --- Streamlit UI ---
st.title("🎧 Lyra - Voice Assistant")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎙️ Start Listening"):
        cmd = hear()
        process_command(cmd)

with col2:
    user_cmd = st.text_input("Or type a command (e.g., 'Lyra play despacito'):")
    if st.button("▶ Run Text Command"):
        if "lyra" in user_cmd.lower():
            cmd = user_cmd.lower().replace("lyra", "").strip()
            process_command(cmd)
        else:
            st.warning("Command must include 'Lyra'")
