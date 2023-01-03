import os
import random
import string
import moviepy as mp
from pythonping import ping 
from flask import Flask,jsonify,request


app = Flask(__name__)

def filename(ext,length=16):
  res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
  return f'{res}.{ext}'
    
@app.route('/ping',methods = ['GET','POST'])
def checkPing():
  ms = ping('194.32.76.100')
  data = {
    'ok': True,
    'ping': ms
  }
  return jsonify(data)

@app.route('/mp3',methods = ['GET','POST'])
def mp3conv():
  url = request.args.get('url',1)
  print(url)
  vid = mp.VideoFileClip(rf'{url}')
  fname = filename('mp3',16)
  vid.audio.write_audiofile(rf'{fname}')
  path = os.path.join(fname)
  data = {
    'ok': True,
    'mp3': path
  }
  return jsonify(data)
  
if __name__ == '__main__':
  app.run(debug=True)
  
