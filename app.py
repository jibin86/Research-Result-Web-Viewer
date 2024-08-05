from flask import Flask, render_template, send_from_directory, url_for
import os
from natsort import natsorted

app = Flask(__name__)

# 동영상 및 이미지 파일이 저장된 디렉터리 경로 설정
BASE_VIDEO_DIR = os.path.join(app.root_path, 'static', 'videos')

def get_directory_content(path):
    directories = []
    files = []
    for item in natsorted(os.listdir(path)):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            directories.append(item)
        elif os.path.isfile(full_path) and (item.endswith('.mp4') or item.endswith('.gif') or item.endswith('.jpg') or item.endswith('.jpeg') or item.endswith('.png')):
            files.append(item)
    return directories, files

@app.route('/')
def index():
    titles = natsorted([title for title in os.listdir(BASE_VIDEO_DIR) if os.path.isdir(os.path.join(BASE_VIDEO_DIR, title))])
    return render_template('index.html', titles=titles)

@app.route('/browse/<path:subpath>')
def browse(subpath):
    current_path = os.path.join(BASE_VIDEO_DIR, subpath)
    directories, files = get_directory_content(current_path)
    return render_template('browse.html', subpath=subpath, directories=directories, files=files)

@app.route('/videos/<path:filename>')
def get_video(filename):
    return send_from_directory(BASE_VIDEO_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9724)
