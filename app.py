from flask import Flask, render_template, send_from_directory, url_for
import os
from natsort import natsorted

app = Flask(__name__)

# 동영상 파일이 저장된 디렉터리 경로 설정
BASE_VIDEO_DIR = os.path.join(app.root_path, 'static', 'videos')

def get_titles():
    return natsorted([title for title in os.listdir(BASE_VIDEO_DIR) if os.path.isdir(os.path.join(BASE_VIDEO_DIR, title))])

def get_subtitles(title):
    title_path = os.path.join(BASE_VIDEO_DIR, title)
    return natsorted([subtitle for subtitle in os.listdir(title_path) if os.path.isdir(os.path.join(title_path, subtitle))])

def get_videos(title, subtitle):
    subtitle_path = os.path.join(BASE_VIDEO_DIR, title, subtitle)
    # return natsorted([video for video in os.listdir(subtitle_path) if os.path.isfile(os.path.join(subtitle_path, video)) and (video.endswith('.mp4') or video.endswith('.gif'))])
    return natsorted([video for video in os.listdir(subtitle_path) if os.path.isfile(os.path.join(subtitle_path, video)) and (video.endswith('.mp4'))])

@app.route('/')
def index():
    titles = get_titles()
    return render_template('index.html', titles=titles)

@app.route('/<title>')
def title_page(title):
    subtitles = get_subtitles(title)
    return render_template('subtitles.html', title=title, subtitles=subtitles)

@app.route('/<title>/<subtitle>')
def subtitle_page(title, subtitle):
    videos = get_videos(title, subtitle)
    return render_template('videos.html', title=title, subtitle=subtitle, videos=videos)

@app.route('/videos/<path:filename>')
def get_video(filename):
    return send_from_directory(BASE_VIDEO_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9724)
