from flask import Flask, render_template, request
from gtts import gTTS
import time
import pychromecast
import json

app = Flask(__name__)


speaker = None

cc = pychromecast.get_chromecasts(timeout=0.5)
for c in cc:
    if "home" in str(c.model_name).lower():
        speaker = c


@app.route("/")
def indexPage():
    return render_template("index.html")



@app.route("/notify", methods=["POST"])
def notify():
    global speaker
    text = request.json
    print(text)
    text = text["text"]
    print(text)
    tts = gTTS(str(text), lang='en')
    tts.save("static/out.mp3")

    
    
    if(speaker != None):
        castTo(speaker)
    

    return render_template("index.html")

def castTo(cc):
    cc.wait()
    
    mc = cc.media_controller
    mc.play_media("http://192.168.2.24:2020/static/out.mp3", "audio/*")
    mc.block_until_active()

    print(mc.status)

    mc.pause()
    time.sleep(5)
    mc.play()


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port='2020')

