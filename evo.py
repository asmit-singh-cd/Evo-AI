import speech_recognition as sr
import os
import datetime
import webbrowser
import tkinter as tk
import cv2
import face_recognition
import threading
import http.client
import json

# 🔑 RAPID API KEY
API_KEY = "YOUR_API"

# 🔊 SPEAK
def speak(text):
    os.system(f'espeak-ng -s 140 -p 20 -v en-us "{text}" 2>/dev/null')
    if "output_label" in globals():
        output_label.config(text="Evo: " + text)
        root.update()

# 🎤 LISTEN
def listen():
    r = sr.Recognizer()

    def animate():
        colors = ["#38bdf8", "#22c55e", "#facc15"]
        for i in range(6):
            mic_btn.config(bg=colors[i % 3])
            root.update()
            root.after(200)

    threading.Thread(target=animate).start()

    with sr.Microphone() as source:
        status_label.config(text="🎤 Listening...")
        root.update()

        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language='en-IN')
        user_label.config(text="You: " + command)
        return command.lower()
    except:
        return ""

# 🧠 AI USING RAPID API
def ask_ai(question):
    try:
        conn = http.client.HTTPSConnection("chatgpt-42.p.rapidapi.com")

        payload = json.dumps({
            "messages": [{"role": "user", "content": question}],
            "system_prompt": "",
            "temperature": 0.9,
            "top_k": 5,
            "top_p": 0.9,
            "max_tokens": 256,
            "web_access": False
        })

        headers = {
            'x-rapidapi-key': "YOUR_KEY",
            'x-rapidapi-host': "chatgpt-42.p.rapidapi.com",
            'Content-Type': "application/json"
        }

        conn.request("POST", "/conversationgpt4-2", payload, headers)
        res = conn.getresponse()
        data = res.read()

        response = json.loads(data.decode("utf-8"))

        # Extract reply safely
        return response.get("result", "Sorry, I didn't understand.")

    except Exception as e:
        print(e)
        return "AI error. Please check internet."

# 📷 FACE UNLOCK
def face_unlock():
    cam = cv2.VideoCapture(0)

    try:
        known_image = face_recognition.load_image_file("user1.jpg")
        known_encoding = face_recognition.face_encodings(known_image)[0]
    except:
        speak("Face data not found")
        return False

    while True:
        ret, frame = cam.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, faces)

        for face_encoding in encodings:
            match = face_recognition.compare_faces([known_encoding], face_encoding)

            if match[0]:
                cam.release()
                cv2.destroyAllWindows()
                return True

        cv2.imshow("Evo Face Lock", frame)

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    return False

# 🚀 COMMANDS
def process(command):

    if "time" in command:
        t = datetime.datetime.now().strftime("%H:%M")
        speak(f"Abhi time hai {t}")

    elif "youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("YouTube khol raha hoon")

    elif "google" in command:
        webbrowser.open("https://google.com")
        speak("Google open kar raha hoon")

    elif "chrome" in command:
        os.system("google-chrome")
        speak("Chrome open kar raha hoon")

    elif "firefox" in command:
        os.system("firefox")
        speak("Firefox open kar raha hoon")

    elif "file manager" in command:
        os.system("nemo")
        speak("File manager khol raha hoon")

    elif "calculator" in command:
        os.system("gnome-calculator")
        speak("Calculator open kar raha hoon")

    elif "terminal" in command:
        os.system("gnome-terminal")
        speak("Terminal open kar raha hoon")

    elif "vs code" in command:
        os.system("code")
        speak("VS Code open kar raha hoon")

    elif "volume up" in command:
        os.system("amixer -D pulse sset Master 10%+")
        speak("Volume badha diya")

    elif "volume down" in command:
        os.system("amixer -D pulse sset Master 10%-")
        speak("Volume kam kar diya")

    elif "mute" in command:
        os.system("amixer -D pulse sset Master toggle")
        speak("Mute kar diya")

    elif "shutdown" in command:
        speak("System band kar raha hoon")
        os.system("shutdown now")

    elif "restart" in command:
        speak("System restart kar raha hoon")
        os.system("reboot")

    elif "lock" in command:
        os.system("gnome-screensaver-command -l")
        speak("System lock kar diya")

    elif "exit" in command:
        speak("Goodbye Asmit")
        root.quit()

    else:
        answer = ask_ai(command)
        speak(answer)

# 🎤 BUTTON
def start_listening():
    command = listen()
    process(command)
    mic_btn.config(bg="#38bdf8")

# 🔐 FACE CHECK
speak("Hello Asmit. I am Evo. Scanning your face.")

if not face_unlock():
    speak("Face not recognized. Access denied.")
    exit()

# 🖥️ UI
root = tk.Tk()
root.title("EVO AI")
root.geometry("500x400")
root.configure(bg="#0f172a")

title = tk.Label(root, text="EVO", font=("Arial", 24, "bold"),
                 fg="#38bdf8", bg="#0f172a")
title.pack(pady=10)

status_label = tk.Label(root, text="Ready",
                        fg="white", bg="#0f172a")
status_label.pack()

user_label = tk.Label(root, text="You:",
                      wraplength=400,
                      fg="#22c55e", bg="#0f172a")
user_label.pack(pady=10)

output_label = tk.Label(root, text="Evo:",
                        wraplength=400,
                        fg="#facc15", bg="#0f172a")
output_label.pack(pady=10)

mic_btn = tk.Button(root, text="🎤",
                    command=start_listening,
                    font=("Arial", 20),
                    bg="#38bdf8", fg="black",
                    padx=20, pady=10)
mic_btn.pack(pady=30)

def start():
    speak("Access granted. How can I help you today?")

root.after(1000, start)

root.mainloop()
