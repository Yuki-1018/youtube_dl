from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    youtube_videoid = request.args.get('youtube_videoid')
    if not youtube_videoid:
        return "No youtube_videoid provided", 400

    youtube_url = f'https://www.youtube.com/watch?v={youtube_videoid}'
    try:
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            video_url = info_dict.get('url', None)
            if not video_url:
                return "Could not retrieve video URL", 500

        # Write the URL to a text file
        filename = f"{youtube_videoid}.txt"
        with open(filename, 'w') as f:
            f.write(video_url)

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
