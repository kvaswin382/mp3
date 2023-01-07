import os
import random
import string
import moviepy.editor as mp
from pythonping import ping 
import urllib.parse as ulib
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
  url = ulib.unquote(request.args.get('url',1))
  print(url)
  vid = mp.VideoFileClip(rf'{url}')
  fname = filename('mp3',16)
  if not os.path.exists('/Audios'):
    os.mkdir('/Audios')
  vid.audio.write_audiofile(rf'/Audios/{fname}')
  path = os.path.abspath(f'/Audios/{fname}')
  data = {
    'ok': True,
    'mp3': path
  }
  return jsonify(data)
  
@app.route('/sendFile',methods = ['GET','POST'])
def sendFile():
  url = ulib.unquote(request.args.get('url',1))
  chat_id = request.args.get('chat_id',1)
  token = request.args.get('token',1)
  print(url)
  api_url = f'https://api.telegram.org/bot{token}/sendVideo'
  video_data = open(url,'rb')
  data = {
    'chat_id': chat_id,
    'video': video_data
  }
  headers = {
    'Content-type': 'multipart/form-data'
  }
  response = requests.post(api_url,headers=headers,data=data)
  try:
    print(response.status_code)
  except:
    print('Cant print status code')
  res = response.json()
  print(res['ok'])
  video_data.close()
  
if __name__ == '__main__':
  app.run(debug=True)
  
