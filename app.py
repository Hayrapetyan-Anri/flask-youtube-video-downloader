from flask import Flask, render_template, request, send_from_directory
from pytube import YouTube
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.abspath('downloads/')  # Use absolute path to downloads directory
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER  # Set the download path to Flask's configuration

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_link = request.form['youtube_link']
        quality = 'high'  # assuming you have a quality select form
        video_info, filename = get_video_info_and_download(youtube_link, quality)
        if 'error' in video_info:
            return render_template('result.html', video_info=video_info)
        else:
            return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)
    return render_template('index.html')

def get_video_info_and_download(youtube_link, quality):
    try:
        yt = YouTube(youtube_link)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        if quality == 'high':
            selected_stream = stream.first()
        else:  # assuming 'low' is the only other option
            selected_stream = stream.last()
        filename = selected_stream.default_filename
        selected_stream.download(output_path=app.config['DOWNLOAD_FOLDER'])
        video_info = {
            'title': yt.title,
            'thumbnail_url': yt.thumbnail_url,
            'duration': yt.length,
            'author': yt.author,
            'views': yt.views,
        }
        return video_info, filename
    except Exception as e:
        return {'error': str(e)}, None

if __name__ == '__main__':
    app.run(debug=True)
