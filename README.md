# 🎬 Video Downloader

Download videos from YouTube and 1,000+ sites in maximum quality, with a clean GUI.

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-green) ![License](https://img.shields.io/badge/license-MIT-purple)

## Preview

Simple interface with multi-format support, destination folder picker, and real-time progress bar.

## Requirements

- Python 3.8+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases) (required to merge video and audio streams)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/video-downloader.git
cd video-downloader
```

2. Install the dependency:

```bash
pip install yt-dlp
```

3. Download ffmpeg from [this link](https://github.com/BtbN/FFmpeg-Builds/releases) and extract it on your PC.

4. Open `downlower.py` and edit the ffmpeg path line:

```python
FFMPEG_PATH = r'C:\path\to\your\ffmpeg\bin'
```

## Usage

```bash
python downlower.py
```

1. Paste the video URL
2. Choose a format (MP4 4K/1080p, 720p, 480p, or audio-only MP3)
3. Select the destination folder
4. Click **Download**

## Available Formats

| Format | Description |
|--------|-------------|
| MP4 (best quality) | Highest available resolution (up to 4K) |
| MP4 720p | Standard HD |
| MP4 480p | Medium resolution, smaller file size |
| Audio only MP3 | Extracts audio at 192kbps |

## Supported Sites

YouTube, Vimeo, Twitter/X, Instagram, TikTok, Facebook, Twitch, and 1,000+ more. Full list at [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Project Structure

```
video-downloader/
├── downloader_gui.py   # Main app with GUI
├── README.md
└── LICENSE
```

## Notes

- tkinter is bundled with Python — no extra install needed.
- ffmpeg is required for best quality downloads (merges separate video and audio streams).
- Without ffmpeg, change the format to `best` in the code to download without it (quality limited to 720p on YouTube).

## License

MIT — free to use.
