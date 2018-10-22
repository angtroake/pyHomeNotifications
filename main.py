from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import time
import pychromecast
import json
import datetime
import _thread
import os

app = Flask(__name__)


speaker = None

# {text, time, filename}
que = []


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
    global que

    time = datetime.datetime.now()

    filename = time.strftime("static/%f%S%M%H%d%m%Y.mp3")

    text = request.json["text"]
    tts = gTTS(str(text), lang='en')
    tts.save(filename)

    
    """
    if(speaker != None):
        castTo(speaker)
    
    """

    que.append((text, time, filename))


    return jsonify("success")

def castTo(cc, filename):
    cc.wait()
    
    mc = cc.media_controller
    mc.play_media("http://192.168.2.24:2020/" + filename, "audio/*")
    mc.block_until_active()

    mc.pause()
    time.sleep(5)
    mc.play()



def castLoop():
    global speaker

    while True:
        global que
        if(len(que) > 0):
            castTo(speaker, que[0][2])
            print("played " + que[0][2])
            _thread.start_new_thread(deleteFile, (que[0][2],))
            del que[0]
        time.sleep(3)

def deleteFile(file):
    time.sleep(5)
    os.remove(file)


if __name__ == "__main__":
    _thread.start_new_thread(castLoop, ())
    app.run(debug = True, host='0.0.0.0', port='2020')
    