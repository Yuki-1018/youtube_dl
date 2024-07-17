from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    youtube_videoid = request.args.get('youtube_videoid')
    if not youtube_videoid:
        return jsonify({"error": "No youtube_videoid provided"}), 400

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
                return jsonify({"error": "Could not retrieve video URL"}), 500

        return jsonify({"video_url": video_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
