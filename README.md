# RingtoneWala.com

A professional web application for converting YouTube videos to MP3 audio files and creating custom ringtones with an advanced waveform editor.

## Features

### 🎵 MP3 Converter

- Convert YouTube videos to MP3 format
- High-quality audio output (up to 320kbps)
- Direct browser download (no redirects)
- Fast and reliable conversion
- No registration required

### 📱 Advanced Ringtone Maker

- **Waveform Visualizer**: Visual audio editor with interactive waveform
- **Precise Selection**: Click-to-select start/end points
- **Multiple Formats**: MP3 and M4A support
- **Quality Options**: High, Medium, Low bitrate settings
- **File Upload**: Create ringtones from your own MP3 files
- **Real-time Preview**: Preview your ringtone before download

### 🚀 Production Ready

- SEO optimized with meta tags and structured data
- Blog system for content marketing
- Railway deployment ready
- Responsive design for all devices
- Professional UI/UX

### 📝 Blog & SEO

- Educational blog posts about audio conversion
- SEO-friendly URLs and meta tags
- Sitemap and robots.txt for search engines
- Open Graph and Twitter Card support

## Prerequisites

Before running the application, make sure you have the following installed:

1. **Python 3.7+**
2. **FFmpeg** - Required for audio conversion

### Installing FFmpeg

#### macOS (using Homebrew):

```bash
brew install ffmpeg
```

#### Ubuntu/Debian:

```bash
sudo apt update
sudo apt install ffmpeg
```

#### Windows:

1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract and add to your PATH environment variable

## Installation

1. Clone or download this repository
2. Navigate to the project directory:

   ```bash
   cd /Users/ringtonewala-flask
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:

   ```bash
   python app.py
   ```

2. Open your web browser and go to:

   ```
   http://localhost:8000
   ```

3. Paste a YouTube video URL into the input field

4. Click "Convert to Audio" and wait for the conversion to complete

5. Click "Download MP3" to save the audio file to your device

## How It Works

1. **Input**: User provides a YouTube video URL
2. **Processing**: The application uses yt-dlp to download the video and FFmpeg to extract audio
3. **Conversion**: Video is converted to high-quality MP3 format (192 kbps)
4. **Download**: User can download the converted audio file

## Technical Details

- **Backend**: Flask (Python web framework)
- **Video Processing**: yt-dlp (YouTube downloader)
- **Audio Conversion**: FFmpeg (via yt-dlp)
- **Frontend**: Bootstrap 5 with custom CSS
- **Temporary Storage**: Files are stored in system temp directory

## File Structure

```
AIAgents/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── templates/
    └── index.html     # Main web interface
```

## Security Notes

- The application uses temporary files that are automatically cleaned up
- Files are stored in the system's temporary directory
- Consider implementing file cleanup for production use
- Change the secret key in production

## Troubleshooting

### Common Issues:

1. **FFmpeg not found**: Make sure FFmpeg is installed and in your PATH
2. **Permission errors**: Ensure the application has write access to the temp directory
3. **Conversion fails**: Check if the YouTube URL is valid and accessible

### Error Messages:

- "Error converting video": Usually indicates an invalid URL or network issue
- "File not found": Temporary file was not created properly
- "Audio file was not created properly": FFmpeg conversion failed

## Deployment

### Railway Deployment

This application is ready for deployment on Railway. Follow these steps:

1. **Prepare your repository:**

   - Ensure all files are committed to GitHub
   - Verify `requirements.txt` and `Procfile` are present

2. **Deploy to Railway:**

   - Sign up at [railway.app](https://railway.app)
   - Create a new project from GitHub
   - Set environment variables:
     ```
     SECRET_KEY=your-random-secret-key
     DEBUG=False
     ```
   - Deploy automatically

3. **Custom Domain (Optional):**
   - Add your domain in Railway settings
   - Update DNS records as instructed

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Environment Variables

| Variable     | Description              | Default  |
| ------------ | ------------------------ | -------- |
| `SECRET_KEY` | Flask secret key         | Required |
| `DEBUG`      | Enable debug mode        | `False`  |
| `PORT`       | Port for the application | `8000`   |

## SEO Features

- **Meta Tags**: Optimized title, description, and keywords
- **Open Graph**: Social media sharing optimization
- **Twitter Cards**: Enhanced Twitter sharing
- **Structured Data**: JSON-LD schema markup
- **Sitemap**: XML sitemap at `/sitemap.xml`
- **Robots.txt**: Search engine directives at `/robots.txt`
- **Blog System**: Content marketing for SEO

## License

This project is for educational purposes. Please respect YouTube's Terms of Service and copyright laws when using this application.

## Contributing

Feel free to submit issues and enhancement requests!
