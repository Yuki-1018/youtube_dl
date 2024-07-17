from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    youtube_videoid = request.args.get('youtube_videoid')
    videoid_audioonly = request.args.get('videoid_audioonly')
    
    if youtube_videoid:
        return get_video_url(youtube_videoid)
    elif videoid_audioonly:
        return get_audio_url(videoid_audioonly)
    else:
        return jsonify({"error": "No videoid provided"}), 400

def get_video_url(videoid):
    youtube_url = f'https://www.youtube.com/watch?v={videoid}'
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
                return jsonify({"error": "Could not retrieve video URL"}), 500

        return jsonify({"video_url": video_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_audio_url(videoid):
    youtube_url = f'https://www.youtube.com/watch?v={videoid}'
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            audio_url = info_dict.get('url', None)
            if not audio_url:
                return jsonify({"error": "Could not retrieve audio URL"}), 500

        return jsonify({"audio_url": audio_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
