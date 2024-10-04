from flask import Flask, render_template, send_from_directory, url_for
import os
import markdown
from natsort import natsorted

app = Flask(__name__)

# 동영상 및 이미지 파일이 저장된 디렉터리 경로 설정
BASE_VIDEO_DIR = os.path.join(app.root_path, 'static', 'videos')

def get_directory_content(path, parent_md_content=None):
    directories = []
    files = []
    md_content = parent_md_content
    for item in natsorted(os.listdir(path)):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            directories.append(item)
        elif os.path.isfile(full_path):
            if item.endswith('.md'):
                with open(full_path, 'r', encoding='utf-8') as f:
                    md_content = markdown.markdown(f.read())
            elif item.endswith('.mp4') or item.endswith('.gif') or item.endswith('.jpg') or item.endswith('.jpeg') or item.endswith('.png'):
                files.append(item)
    return directories, files, md_content

@app.route('/')
def index():
    titles = natsorted([title for title in os.listdir(BASE_VIDEO_DIR) if os.path.isdir(os.path.join(BASE_VIDEO_DIR, title))])[::-1]
    return render_template('index.html', titles=titles)

@app.route('/browse/<path:subpath>')
def browse(subpath):
    
    parts = subpath.split('/')
    current_md_content = None
    
    # 최상위 디렉터리부터 현재 경로까지의 각 레벨에서 .md 파일 확인
    for i in range(len(parts)):
        current_path = os.path.join(BASE_VIDEO_DIR, *parts[:i+1])
        _, _, current_md_content = get_directory_content(current_path, current_md_content)

    # 현재 디렉터리의 내용을 불러옴
    current_path = os.path.join(BASE_VIDEO_DIR, subpath)
    directories, files, md_content = get_directory_content(current_path, current_md_content)

    return render_template('browse.html', subpath=subpath, directories=directories, files=files, md_content=md_content)

@app.route('/videos/<path:filename>')
def get_video(filename):
    return send_from_directory(BASE_VIDEO_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9724)
