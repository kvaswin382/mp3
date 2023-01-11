import os
import random
import string
import moviepy.editor as mp
import urllib.parse as ulib
from flask import Flask,jsonify,request


app = Flask(__name__)

def filename(ext,length=16):
  res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
  return f'{res}.{ext}'
    

@app.route('/mp3',methods = ['GET','POST'])
def mp3conv():
  url = ulib.unquote(request.args.get('url',1))
  print(url)
  vid = mp.VideoFileClip(rf'{url}')
  fname = filename('mp3')
  print(fname)
  vid.audio.write_audiofile(rf'/{fname}')
  path = os.path.abspath(f'/{fname}')
  data = {
    'ok': True,
    'mp3': path
  }
  return jsonify(data)
  

  
if __name__ == '__main__':
  app.run(debug=True)
  
