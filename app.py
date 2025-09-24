from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import os
import yt_dlp
import tempfile
import uuid
from werkzeug.utils import secure_filename
import subprocess
import json
import time
from datetime import datetime
import shutil

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Configuration
DOWNLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a'}

# Check FFmpeg availability
def check_ffmpeg():
    """Check if FFmpeg is available and return path"""
    ffmpeg_path = shutil.which('ffmpeg')
    if not ffmpeg_path:
        # Try common paths
        common_paths = [
            '/usr/bin/ffmpeg',
            '/usr/local/bin/ffmpeg',
            '/opt/homebrew/bin/ffmpeg',
            '/usr/local/bin/ffmpeg'
        ]
        for path in common_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
        return None
    return ffmpeg_path

# Get FFmpeg path
FFMPEG_PATH = check_ffmpeg()
if not FFMPEG_PATH:
    print("WARNING: FFmpeg not found. Audio processing will not work properly.")
    print("Please ensure FFmpeg is installed and available in PATH.")
else:
    print(f"✅ FFmpeg found at: {FFMPEG_PATH}")

def get_ffmpeg_cmd(base_cmd):
    """Get FFmpeg command with proper path"""
    if not FFMPEG_PATH:
        raise RuntimeError("FFmpeg is not installed or not found in PATH")
    return [FFMPEG_PATH] + base_cmd

# Blog data
BLOG_POSTS = [
    {
        'slug': 'how-to-convert-youtube-to-mp3',
        'title': 'How to Convert YouTube Videos to MP3: Complete Guide',
        'excerpt': 'Learn the best methods to convert YouTube videos to MP3 format with our comprehensive guide. Get high-quality audio downloads in minutes.',
        'keywords': 'youtube to mp3, convert youtube video, mp3 download, audio converter',
        'date': '2024-01-15',
        'read_time': 5,
        'content': '''
            <h2>Introduction to YouTube to MP3 Conversion</h2>
            <p>Converting YouTube videos to MP3 format is one of the most popular audio conversion tasks. Whether you want to create a playlist of your favorite songs or extract audio from educational content, our guide will help you achieve the best results.</p>
            
            <h3>Why Convert YouTube to MP3?</h3>
            <ul>
                <li><strong>Offline Listening:</strong> Enjoy your favorite content without an internet connection</li>
                <li><strong>Storage Efficiency:</strong> MP3 files are smaller than video files</li>
                <li><strong>Compatibility:</strong> MP3 format works on all devices and music players</li>
                <li><strong>Audio Quality:</strong> Focus on crystal-clear audio without video distractions</li>
            </ul>
            
            <h3>Best Practices for YouTube to MP3 Conversion</h3>
            <p>To get the best results when converting YouTube videos to MP3:</p>
            <ol>
                <li><strong>Choose High-Quality Sources:</strong> Select videos with good audio quality</li>
                <li><strong>Use the Right Settings:</strong> 320kbps for music, 128kbps for speech</li>
                <li><strong>Check Copyright:</strong> Only convert content you have permission to download</li>
                <li><strong>Verify Output:</strong> Always test the converted file before saving</li>
            </ol>
            
            <div class="highlight-box">
                <h4><i class="fas fa-lightbulb me-2"></i>Pro Tip</h4>
                <p>For music videos, use 320kbps bitrate for the best quality. For podcasts or speeches, 128kbps is usually sufficient and creates smaller files.</p>
            </div>
            
            <h3>Common Issues and Solutions</h3>
            <p>Here are some common problems you might encounter and how to solve them:</p>
            <ul>
                <li><strong>Conversion Fails:</strong> Check your internet connection and try a different video</li>
                <li><strong>Poor Audio Quality:</strong> Ensure the original video has good audio quality</li>
                <li><strong>File Won't Play:</strong> Try converting to a different format or check your media player</li>
            </ul>
        '''
    },
    {
        'slug': 'create-perfect-ringtone-guide',
        'title': 'Create the Perfect Custom Ringtone: Step-by-Step Guide',
        'excerpt': 'Learn how to create professional-quality ringtones using our advanced waveform editor. Tips for choosing the best audio segments and optimizing for mobile devices.',
        'keywords': 'custom ringtone, ringtone maker, mobile ringtone, audio editing',
        'date': '2024-01-10',
        'read_time': 7,
        'content': '''
            <h2>Creating the Perfect Custom Ringtone</h2>
            <p>Your ringtone is your personal signature sound. With our advanced ringtone maker, you can create professional-quality custom ringtones that stand out and reflect your personality.</p>
            
            <h3>Choosing the Right Audio Segment</h3>
            <p>The key to a great ringtone is selecting the perfect audio segment. Here's what to look for:</p>
            <ul>
                <li><strong>Catchy Melody:</strong> Choose a memorable and recognizable part of the song</li>
                <li><strong>Strong Beat:</strong> A clear rhythm helps the ringtone cut through background noise</li>
                <li><strong>Appropriate Length:</strong> 15-30 seconds is ideal for most ringtones</li>
                <li><strong>Clear Audio:</strong> Avoid segments with too much bass or distortion</li>
            </ul>
            
            <h3>Using the Waveform Editor</h3>
            <p>Our advanced waveform editor makes it easy to select the perfect segment:</p>
            <ol>
                <li><strong>Upload Your Audio:</strong> Choose a high-quality MP3 file</li>
                <li><strong>Analyze the Waveform:</strong> Look for peaks that indicate the chorus or hook</li>
                <li><strong>Set Start and End Points:</strong> Use the sliders to precisely select your segment</li>
                <li><strong>Preview Your Selection:</strong> Listen to make sure it sounds perfect</li>
                <li><strong>Choose Format:</strong> M4A for iPhone, MP3 for Android</li>
            </ol>
            
            <div class="highlight-box">
                <h4><i class="fas fa-mobile-alt me-2"></i>Mobile Optimization Tips</h4>
                <p>For the best results on mobile devices, keep ringtones between 15-30 seconds and use high-quality source material. Test your ringtone on your device before setting it as your default.</p>
            </div>
            
            <h3>Ringtone Best Practices</h3>
            <ul>
                <li><strong>Test Volume Levels:</strong> Ensure your ringtone is audible but not too loud</li>
                <li><strong>Consider Your Environment:</strong> Choose ringtones appropriate for work or social settings</li>
                <li><strong>Backup Your Ringtones:</strong> Save your custom creations in multiple locations</li>
                <li><strong>Regular Updates:</strong> Change your ringtone periodically to keep it fresh</li>
            </ul>
        '''
    },
    {
        'slug': 'audio-quality-settings-explained',
        'title': 'Audio Quality Settings Explained: MP3 vs M4A vs WAV',
        'excerpt': 'Understand the differences between audio formats and quality settings. Learn which format is best for different use cases and how to optimize file size vs quality.',
        'keywords': 'audio quality, mp3 vs m4a, bitrate, audio formats, file size',
        'date': '2024-01-05',
        'read_time': 6,
        'content': '''
            <h2>Understanding Audio Quality Settings</h2>
            <p>Choosing the right audio format and quality settings is crucial for getting the best results. This guide explains the differences between popular formats and helps you make informed decisions.</p>
            
            <h3>Audio Format Comparison</h3>
            
            <h4>MP3 Format</h4>
            <ul>
                <li><strong>Compatibility:</strong> Works on all devices and platforms</li>
                <li><strong>File Size:</strong> Smaller files, good compression</li>
                <li><strong>Quality:</strong> Good quality at higher bitrates (320kbps)</li>
                <li><strong>Best For:</strong> General use, sharing, storage</li>
            </ul>
            
            <h4>M4A Format</h4>
            <ul>
                <li><strong>Compatibility:</strong> Excellent on Apple devices</li>
                <li><strong>File Size:</strong> Better compression than MP3</li>
                <li><strong>Quality:</strong> Superior quality at same bitrate</li>
                <li><strong>Best For:</strong> iPhone/iPad users, high-quality audio</li>
            </ul>
            
            <h3>Bitrate Explained</h3>
            <p>Bitrate determines the amount of data used per second of audio:</p>
            <ul>
                <li><strong>64kbps:</strong> Low quality, very small files - suitable for speech only</li>
                <li><strong>128kbps:</strong> Standard quality, good for most music</li>
                <li><strong>192kbps:</strong> High quality, noticeable improvement over 128kbps</li>
                <li><strong>320kbps:</strong> Highest quality, near-CD quality</li>
            </ul>
            
            <div class="highlight-box">
                <h4><i class="fas fa-chart-line me-2"></i>Quality vs File Size</h4>
                <p>Higher bitrates mean better quality but larger files. For most users, 128kbps MP3 or 128kbps M4A provides the best balance of quality and file size.</p>
            </div>
            
            <h3>Choosing the Right Settings</h3>
            <p>Here's a quick guide for different use cases:</p>
            <ul>
                <li><strong>Music Collection:</strong> 320kbps MP3 or 256kbps M4A</li>
                <li><strong>Podcasts:</strong> 128kbps MP3</li>
                <li><strong>Ringtones:</strong> 128kbps M4A (iPhone) or 128kbps MP3 (Android)</li>
                <li><strong>Storage Limited:</strong> 128kbps MP3</li>
                <li><strong>Archival:</strong> 320kbps MP3 or lossless formats</li>
            </ul>
        '''
    }
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/robots.txt')
def robots_txt():
    return send_file('static/robots.txt', mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://ringtonewala.com/</loc>
        <lastmod>2025-01-23</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://ringtonewala.com/blog</loc>
        <lastmod>2025-01-23</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>'''
    
    for blog in BLOG_POSTS:
        sitemap_content += f'''
    <url>
        <loc>https://ringtonewala.com/blog/{blog['slug']}</loc>
        <lastmod>{blog['date']}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>'''
    
    sitemap_content += '''
</urlset>'''
    
    return sitemap_content, 200, {'Content-Type': 'application/xml'}

@app.route('/convert', methods=['POST'])
def convert_video():
    youtube_url = request.form.get('youtube_url')
    
    if not youtube_url:
        return jsonify({'success': False, 'error': 'Please enter a YouTube URL'})
    
    if not FFMPEG_PATH:
        return jsonify({'success': False, 'error': 'FFmpeg is not installed. Audio processing is not available.'})
    
    try:
        # Create a unique filename for the audio file
        audio_filename = f"audio_{uuid.uuid4().hex}.mp3"
        audio_path = os.path.join(DOWNLOAD_FOLDER, audio_filename)
        
        # Configure yt-dlp options for audio extraction with better error handling
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': audio_path.replace('.mp3', '.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',  # Reduced quality for speed
                'nopostoverwrites': False,
            }],
            'extractaudio': True,
            'audioformat': 'mp3',
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'no_warnings': False,
            'extract_flat': False,
            'writeinfojson': False,
            'writethumbnail': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'cookiesfrombrowser': None,
            'sleep_interval': 0,  # Reduced sleep for faster downloads
            'max_sleep_interval': 1,  # Reduced max sleep
            'socket_timeout': 30,  # Faster timeout
            'retries': 3,  # Fewer retries for speed
            'fragment_retries': 3,  # Fewer fragment retries
            'http_chunk_size': 10485760,  # Larger chunk size for faster downloads
        }
        
        # Download and convert the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
            
        # Find the actual output file (yt-dlp might add extension)
        actual_audio_path = audio_path
        if not os.path.exists(actual_audio_path):
            # Try with .mp3 extension
            actual_audio_path = audio_path.replace('.mp3', '.mp3')
        
        # Check if file exists
        if not os.path.exists(actual_audio_path):
            return jsonify({
                'success': False, 
                'error': 'Audio file was not created properly. This might be due to YouTube restrictions or network issues.'
            })
        
        # Create a clean MP3 file for better compatibility
        fixed_audio_filename = f"fixed_audio_{uuid.uuid4().hex}.mp3"
        fixed_audio_path = os.path.join(DOWNLOAD_FOLDER, fixed_audio_filename)
        
        # Use FFmpeg to create a clean MP3 file with proper headers
        ffmpeg_fix_cmd = get_ffmpeg_cmd([
            '-y',  # Overwrite output file
            '-i', actual_audio_path,
            '-c:a', 'libmp3lame',
            '-b:a', '128k',
            '-ac', '2',  # Stereo
            '-ar', '44100',  # Sample rate
            '-write_xing', '1',  # Write Xing header for better compatibility
            '-id3v2_version', '0',  # Use ID3v2.3 for better compatibility
            '-map_metadata', '-1',  # Remove all metadata to avoid container issues
            '-f', 'mp3',  # Force MP3 format
            '-q:a', '2',  # High quality
            fixed_audio_path
        ])
        
        fix_result = subprocess.run(ffmpeg_fix_cmd, capture_output=True, text=True)
        
        if fix_result.returncode != 0:
            # If fix fails, use original file
            print(f"MP3 fix failed, using original file: {fix_result.stderr}")
            final_audio_path = actual_audio_path
        else:
            # Clean up original file and use fixed version
            if os.path.exists(actual_audio_path):
                os.remove(actual_audio_path)
            final_audio_path = fixed_audio_path
        
        # Validate the final file
        if not os.path.exists(final_audio_path):
            return jsonify({
                'success': False, 
                'error': 'Audio file processing failed.'
            })
            
        # Return the file directly for download
        return send_file(
            final_audio_path,
            as_attachment=True,
            download_name='converted_audio.mp3',
            mimetype='audio/mpeg'
        )
        
    except yt_dlp.DownloadError as e:
        error_msg = str(e).lower()
        if '403' in error_msg or 'forbidden' in error_msg:
            error_message = 'YouTube blocked the request. This video may be restricted or YouTube is temporarily blocking downloads. Please try again later or with a different video.'
        elif '400' in error_msg or 'bad request' in error_msg:
            error_message = 'Invalid YouTube URL or video is not available. Please check the URL and try again.'
        elif 'precondition check failed' in error_msg:
            error_message = 'YouTube is currently blocking download requests. This is a temporary issue. Please try again in a few minutes.'
        else:
            error_message = f'Download error: {str(e)}'
        return jsonify({'success': False, 'error': error_message})
    except Exception as e:
        error_msg = str(e).lower()
        if 'http error 403' in error_msg or 'forbidden' in error_msg:
            error_message = 'YouTube blocked the request. Please try again later or with a different video.'
        elif 'http error 400' in error_msg:
            error_message = 'Invalid URL or video not available. Please check the YouTube link.'
        else:
            error_message = f'Error converting video: {str(e)}'
        return jsonify({'success': False, 'error': error_message})

@app.route('/create_ringtone', methods=['POST'])
def create_ringtone():
    try:
        data = request.get_json()
        youtube_url = data.get('youtube_url')
        start_time = float(data.get('start_time', 0))
        duration = float(data.get('duration', 30))
        quality = data.get('quality', 'high')
        format_type = data.get('format', 'mp3')
        
        if not youtube_url:
            return jsonify({'success': False, 'error': 'Please enter a YouTube URL'})
        
        if not FFMPEG_PATH:
            return jsonify({'success': False, 'error': 'FFmpeg is not installed. Audio processing is not available.'})
        
        # Create a unique filename for the ringtone
        extension = 'm4a' if format_type == 'm4a' else 'mp3'
        ringtone_filename = f"ringtone_{uuid.uuid4().hex}.{extension}"
        ringtone_path = os.path.join(DOWNLOAD_FOLDER, ringtone_filename)
        
        # Configure yt-dlp options for ringtone extraction
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio/best',
            'outtmpl': ringtone_path.replace(f'.{extension}', '.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',  # Reduced quality for speed
            }],
            'extractaudio': True,
            'audioformat': 'mp3',
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'no_warnings': False,
            'extract_flat': False,
            'writeinfojson': False,
            'writethumbnail': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'cookiesfrombrowser': None,
            'sleep_interval': 0,  # Reduced sleep for faster downloads
            'max_sleep_interval': 1,  # Reduced max sleep
            'socket_timeout': 30,  # Faster timeout
            'extractor_retries': 3,
            'fragment_retries': 3,  # Fewer fragment retries
            'http_chunk_size': 10485760,  # Larger chunk size for faster downloads
        }
        
        # Download and convert the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        
        # Find the actual output file
        actual_audio_path = ringtone_path.replace(f'.{extension}', '.mp3')
        if not os.path.exists(actual_audio_path):
            # Try with other possible extensions
            for ext in ['.mp3', '.m4a', '.webm']:
                test_path = ringtone_path.replace(f'.{extension}', ext)
                if os.path.exists(test_path):
                    actual_audio_path = test_path
                    break
        
        if not os.path.exists(actual_audio_path):
            return jsonify({
                'success': False, 
                'error': 'Audio file was not created properly.'
            })
        
        # Create trimmed ringtone using FFmpeg
        # Use a different filename for output to avoid in-place editing error
        final_ringtone_filename = f"final_ringtone_{uuid.uuid4().hex}.{extension}"
        final_ringtone_path = os.path.join(DOWNLOAD_FOLDER, final_ringtone_filename)
        
        # Set bitrate based on quality
        bitrate_map = {'high': '128k', 'medium': '96k', 'low': '64k'}
        bitrate = bitrate_map.get(quality, '128k')
        
        if format_type == 'm4a':
            # M4A format for better macOS compatibility
            ffmpeg_cmd = get_ffmpeg_cmd([
                '-i', actual_audio_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:a', 'aac',
                '-b:a', bitrate,
                '-ac', '2',  # Stereo audio
                '-ar', '44100',  # Sample rate 44.1kHz
                '-movflags', '+faststart',
                '-profile:a', 'aac_low',  # Use AAC-LC profile for compatibility
                '-map_metadata', '-1',  # Remove all metadata
                '-avoid_negative_ts', 'make_zero',
                '-fflags', '+bitexact',
                '-f', 'mp4',
                '-y',  # Overwrite output file
                final_ringtone_path
            ])
        else:
            # MP3 format optimized for Mac compatibility
            ffmpeg_cmd = get_ffmpeg_cmd([
                '-i', actual_audio_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:a', 'libmp3lame',
                '-b:a', bitrate,
                '-ac', '2',  # Stereo audio
                '-ar', '44100',  # Sample rate 44.1kHz
                '-ss', '0',  # Force start time to 0
                '-fflags', '+bitexact',  # Ensure consistent output
                '-write_xing', '1',  # Write Xing header for better compatibility
                '-id3v2_version', '0',  # Use ID3v2.3
                '-map_metadata', '-1',  # Remove all metadata
                '-f', 'mp3',  # Force MP3 format
                '-y',  # Overwrite output file
                final_ringtone_path
            ])
            
            print(f"FFmpeg command: {' '.join(ffmpeg_cmd)}")
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        print(f"FFmpeg return code: {result.returncode}")
        print(f"FFmpeg stdout: {result.stdout}")
        print(f"FFmpeg stderr: {result.stderr}")
        
        if result.returncode != 0:
            return jsonify({
                'success': False, 
                'error': f'FFmpeg error: {result.stderr}'
            })
        
        # Clean up temporary files
        if os.path.exists(actual_audio_path):
            os.remove(actual_audio_path)
        
        if not os.path.exists(final_ringtone_path):
            return jsonify({
                'success': False, 
                'error': 'Ringtone file was not created properly.'
            })
        
        # Validate the audio file with FFmpeg
        validate_cmd = get_ffmpeg_cmd(['-v', 'error', '-i', final_ringtone_path, '-f', 'null', '-'])
        validate_result = subprocess.run(validate_cmd, capture_output=True, text=True)
        
        if validate_result.returncode != 0:
            return jsonify({
                'success': False, 
                'error': f'Created audio file is corrupted or invalid: {validate_result.stderr}'
            })
        
        # Additional validation - check file size and basic properties
        file_size = os.path.getsize(final_ringtone_path)
        if file_size < 1024:  # Less than 1KB is suspicious
            return jsonify({
                'success': False, 
                'error': f'Created audio file is too small ({file_size} bytes) and likely corrupted.'
            })
        
        # Debug: Log file info
        print(f"Created ringtone: {final_ringtone_path}, Size: {file_size} bytes, Format: {format_type}")
        
        # Return the ringtone file directly for download
        download_name = f'custom_ringtone.{extension}'
        mimetype = 'audio/mp4' if format_type == 'm4a' else 'audio/mpeg'
        
        # Send the file and clean up afterwards
        response = send_file(
            final_ringtone_path,
            as_attachment=True,
            download_name=download_name,
            mimetype=mimetype
        )
        
        # Clean up the temporary final file after sending
        try:
            if os.path.exists(final_ringtone_path):
                os.remove(final_ringtone_path)
        except Exception as e:
            print(f"Warning: Could not clean up final ringtone file: {e}")
        
        return response
        
    except yt_dlp.DownloadError as e:
        error_msg = str(e).lower()
        if '403' in error_msg or 'forbidden' in error_msg:
            error_message = 'YouTube blocked the request. Please try again later or with a different video.'
        elif '400' in error_msg or 'bad request' in error_msg:
            error_message = 'Invalid YouTube URL or video is not available.'
        else:
            error_message = f'Download error: {str(e)}'
        return jsonify({'success': False, 'error': error_message})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error creating ringtone: {str(e)}'})

@app.route('/create_ringtone_from_file', methods=['POST'])
def create_ringtone_from_file():
    try:
        # Check if file was uploaded
        if 'mp3_file' not in request.files:
            return jsonify({'success': False, 'error': 'No MP3 file uploaded'})
        
        file = request.files['mp3_file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Get form data
        start_time = float(request.form.get('start_time', 0))
        duration = float(request.form.get('duration', 30))
        quality = request.form.get('quality', 'high')
        format_type = request.form.get('format', 'mp3')
        
        # Validate file extension
        if not file.filename.lower().endswith('.mp3'):
            return jsonify({'success': False, 'error': 'Please upload an MP3 file only'})
        
        # Create a unique filename for the uploaded file
        upload_filename = f"upload_{uuid.uuid4().hex}.mp3"
        upload_path = os.path.join(DOWNLOAD_FOLDER, upload_filename)
        
        # Save uploaded file
        file.save(upload_path)
        
        if not os.path.exists(upload_path):
            return jsonify({'success': False, 'error': 'Failed to save uploaded file'})
        
        # Create trimmed ringtone using FFmpeg
        extension = 'm4a' if format_type == 'm4a' else 'mp3'
        ringtone_filename = f"ringtone_{uuid.uuid4().hex}.{extension}"
        ringtone_path = os.path.join(DOWNLOAD_FOLDER, ringtone_filename)
        
        # Set bitrate based on quality
        bitrate_map = {'high': '128k', 'medium': '96k', 'low': '64k'}
        bitrate = bitrate_map.get(quality, '128k')
        
        if format_type == 'm4a':
            # M4A format for better macOS compatibility
            ffmpeg_cmd = get_ffmpeg_cmd([
                '-i', upload_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:a', 'aac',
                '-b:a', bitrate,
                '-ac', '2',  # Stereo audio
                '-ar', '44100',  # Sample rate 44.1kHz
                '-movflags', '+faststart',
                '-profile:a', 'aac_low',  # Use AAC-LC profile for compatibility
                '-map_metadata', '-1',  # Remove all metadata
                '-avoid_negative_ts', 'make_zero',
                '-fflags', '+bitexact',
                '-f', 'mp4',
                '-y',  # Overwrite output file
                ringtone_path
            ])
        else:
            # MP3 format optimized for Mac compatibility
            ffmpeg_cmd = get_ffmpeg_cmd([
                '-i', upload_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:a', 'libmp3lame',
                '-b:a', bitrate,
                '-ac', '2',  # Stereo audio
                '-ar', '44100',  # Sample rate 44.1kHz
                '-ss', '0',  # Force start time to 0
                '-fflags', '+bitexact',  # Ensure consistent output
                '-write_xing', '1',  # Write Xing header for better compatibility
                '-id3v2_version', '0',  # Use ID3v2.3
                '-map_metadata', '-1',  # Remove all metadata
                '-f', 'mp3',  # Force MP3 format
                '-y',  # Overwrite output file
                ringtone_path
            ])
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        # Clean up uploaded file
        if os.path.exists(upload_path):
            os.remove(upload_path)
        
        if result.returncode != 0:
            return jsonify({
                'success': False, 
                'error': f'FFmpeg error: {result.stderr}'
            })
        
        if not os.path.exists(ringtone_path):
            return jsonify({
                'success': False, 
                'error': 'Ringtone file was not created properly.'
            })
        
        # Validate the MP3 file with FFmpeg
        validate_cmd = get_ffmpeg_cmd(['-v', 'error', '-i', ringtone_path, '-f', 'null', '-'])
        validate_result = subprocess.run(validate_cmd, capture_output=True, text=True)
        
        if validate_result.returncode != 0:
            return jsonify({
                'success': False, 
                'error': 'Created MP3 file is corrupted or invalid.'
            })
        
        # Return the ringtone file directly for download
        download_name = f'custom_ringtone.{extension}'
        mimetype = 'audio/mp4' if format_type == 'm4a' else 'audio/mpeg'
        
        return send_file(
            ringtone_path,
            as_attachment=True,
            download_name=download_name,
            mimetype=mimetype
        )
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error creating ringtone: {str(e)}'})

# Blog routes
@app.route('/blog')
def blog_list():
    return render_template('blog_list.html', blogs=BLOG_POSTS)

@app.route('/blog/<slug>')
def blog_post(slug):
    blog = next((post for post in BLOG_POSTS if post['slug'] == slug), None)
    if not blog:
        return "Blog post not found", 404
    return render_template('blog.html', blog=blog)


# Robots.txt for SEO (updated)
@app.route('/robots.txt')
def robots():
    robots_content = '''User-agent: *
Allow: /

Sitemap: https://ringtonewala.com/sitemap.xml'''
    return robots_content, 200, {'Content-Type': 'text/plain'}

@app.route('/preview_ringtone', methods=['POST'])
def preview_ringtone():
    """Preview ringtone from YouTube video"""
    try:
        print("Preview ringtone request received")
        data = request.get_json()
        print(f"Request data: {data}")
        
        youtube_url = data.get('youtube_url')
        start_time = float(data.get('start_time', 0))
        duration = float(data.get('duration', 30))
        quality = data.get('quality', 'high')
        format_type = data.get('format', 'mp3')
        
        print(f"Processing: URL={youtube_url}, start={start_time}, duration={duration}, quality={quality}, format={format_type}")
        
        if not youtube_url:
            return jsonify({'error': 'YouTube URL is required'}), 400
        
        # Generate unique filename for preview
        timestamp = int(time.time())
        preview_filename = f"preview_ringtone_{timestamp}.{format_type}"
        preview_path = os.path.join(DOWNLOAD_FOLDER, preview_filename)
        
        # Download audio using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': preview_path.replace(f'.{format_type}', '.%(ext)s'),
            'extractaudio': True,
            'audioformat': format_type,
            'noplaylist': True,
            'extract_flat': False,
        }
        
        # Set quality based on selection (optimized for speed)
        if quality == 'high':
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format_type,
                'preferredquality': '128',  # Reduced from 192 for speed
            }]
        elif quality == 'medium':
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format_type,
                'preferredquality': '96',  # Reduced from 128 for speed
            }]
        else:  # low
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format_type,
                'preferredquality': '64',  # Reduced from 96 for speed
            }]
        
        # Add speed optimizations
        ydl_opts.update({
            'sleep_interval': 0,  # Reduced sleep for faster downloads
            'max_sleep_interval': 1,  # Reduced max sleep
            'socket_timeout': 30,  # Faster timeout
            'retries': 3,  # Fewer retries for speed
            'fragment_retries': 3,  # Fewer fragment retries
            'http_chunk_size': 10485760,  # Larger chunk size for faster downloads
        })
        
        print(f"Starting yt-dlp download with options: {ydl_opts}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        print("yt-dlp download completed")
        
        # Find the actual downloaded file
        actual_file = None
        print(f"Looking for files in: {DOWNLOAD_FOLDER}")
        for file in os.listdir(DOWNLOAD_FOLDER):
            print(f"Found file: {file}")
            if file.startswith(f"preview_ringtone_{timestamp}"):
                actual_file = os.path.join(DOWNLOAD_FOLDER, file)
                print(f"Matched file: {actual_file}")
                break
        
        if not actual_file or not os.path.exists(actual_file):
            print(f"No matching file found for preview_ringtone_{timestamp}")
            return jsonify({'error': 'Failed to download audio'}), 500
        
        # Create ringtone using FFmpeg (use different filename to avoid in-place editing)
        final_ringtone_filename = f"final_preview_{timestamp}.{format_type}"
        ringtone_path = os.path.join(DOWNLOAD_FOLDER, final_ringtone_filename)
        
        # FFmpeg command for ringtone creation (optimized for speed)
        if format_type == 'mp3':
            ffmpeg_cmd = get_ffmpeg_cmd([ '-y', '-threads', '0', '-i', actual_file,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:a', 'libmp3lame',
                '-b:a', '96k',  # Lower bitrate for faster processing
                '-ss', '0',  # Force start time to 0
                '-fflags', '+bitexact',  # Ensure consistent output
                '-write_xing', '1',  # Write Xing header for better compatibility
                '-id3v2_version', '0',  # Use ID3v2.3
                '-map_metadata', '-1',  # Remove all metadata
                '-f', 'mp3',  # Force MP3 format
                '-preset', 'ultrafast',  # Fastest preset
                '-ac', '2',
                '-ar', '22050',  # Lower sample rate for speed
                ringtone_path
            ])
        else:  # m4a
            ffmpeg_cmd = get_ffmpeg_cmd([ '-y', '-threads', '0', '-i', actual_file,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:a', 'aac',
                '-b:a', '96k',  # Lower bitrate for faster processing
                '-preset', 'ultrafast',  # Fastest preset
                '-ac', '2',
                '-ar', '22050',  # Lower sample rate for speed
                ringtone_path
            ])
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            # Clean up downloaded file
            if os.path.exists(actual_file):
                os.remove(actual_file)
            return jsonify({'error': f'FFmpeg error: {result.stderr}'}), 500
        
        # Validate the created ringtone
        validate_cmd = get_ffmpeg_cmd(['-v', 'error', '-i', ringtone_path, '-f', 'null', '-'])
        validate_result = subprocess.run(validate_cmd, capture_output=True, text=True)
        
        if validate_result.returncode != 0:
            # Clean up files
            if os.path.exists(actual_file):
                os.remove(actual_file)
            if os.path.exists(ringtone_path):
                os.remove(ringtone_path)
            return jsonify({'error': 'Invalid ringtone created'}), 500
        
        # Clean up the original downloaded file
        if os.path.exists(actual_file):
            os.remove(actual_file)
        
        # Return the ringtone file for browser playback
        mimetype = 'audio/mpeg' if format_type == 'mp3' else 'audio/mp4'
        
        # Send the file and clean up afterwards
        response = send_file(ringtone_path, 
                        as_attachment=False,  # Don't download, just preview
                        mimetype=mimetype)
        
        # Clean up the final ringtone file after sending
        try:
            if os.path.exists(ringtone_path):
                os.remove(ringtone_path)
        except Exception as e:
            print(f"Warning: Could not clean up final preview file: {e}")
        
        return response
        
    except yt_dlp.DownloadError as e:
        error_msg = str(e)
        if 'HTTP Error 400' in error_msg:
            return jsonify({'error': 'Invalid YouTube URL or video is not available'}), 400
        elif 'HTTP Error 403' in error_msg:
            return jsonify({'error': 'Video is restricted by YouTube'}), 403
        elif 'Precondition check failed' in error_msg:
            return jsonify({'error': 'Video is not available for download'}), 403
        else:
            return jsonify({'error': f'YouTube download error: {error_msg}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/preview_ringtone_from_file', methods=['POST'])
def preview_ringtone_from_file():
    """Preview ringtone from uploaded MP3 file"""
    try:
        if 'mp3_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['mp3_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.mp3'):
            return jsonify({'error': 'Please upload an MP3 file'}), 400
        
        start_time = float(request.form.get('start_time', 0))
        duration = float(request.form.get('duration', 30))
        quality = request.form.get('quality', 'high')
        format_type = request.form.get('format', 'mp3')
        
        # Save uploaded file temporarily
        timestamp = int(time.time())
        temp_filename = f"temp_upload_{timestamp}.mp3"
        temp_path = os.path.join(DOWNLOAD_FOLDER, temp_filename)
        file.save(temp_path)
        
        # Create ringtone filename
        ringtone_filename = f"preview_ringtone_{timestamp}.{format_type}"
        ringtone_path = os.path.join(DOWNLOAD_FOLDER, ringtone_filename)
        
        # FFmpeg command for ringtone creation (optimized for speed)
        if format_type == 'mp3':
            ffmpeg_cmd = get_ffmpeg_cmd([ '-y', '-threads', '0', '-i', temp_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:a', 'libmp3lame',
                '-b:a', '96k',  # Lower bitrate for faster processing
                '-ss', '0',  # Force start time to 0
                '-fflags', '+bitexact',  # Ensure consistent output
                '-write_xing', '1',  # Write Xing header for better compatibility
                '-id3v2_version', '0',  # Use ID3v2.3
                '-map_metadata', '-1',  # Remove all metadata
                '-f', 'mp3',  # Force MP3 format
                '-preset', 'ultrafast',  # Fastest preset
                '-ac', '2',
                '-ar', '22050',  # Lower sample rate for speed
                ringtone_path
            ])
        else:  # m4a
            ffmpeg_cmd = get_ffmpeg_cmd([ '-y', '-threads', '0', '-i', temp_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:a', 'aac',
                '-b:a', '96k',  # Lower bitrate for faster processing
                '-preset', 'ultrafast',  # Fastest preset
                '-ac', '2',
                '-ar', '22050',  # Lower sample rate for speed
                ringtone_path
            ])
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        if result.returncode != 0:
            if os.path.exists(ringtone_path):
                os.remove(ringtone_path)
            return jsonify({'error': f'FFmpeg error: {result.stderr}'}), 500
        
        # Validate the created ringtone
        validate_cmd = get_ffmpeg_cmd(['-v', 'error', '-i', ringtone_path, '-f', 'null', '-'])
        validate_result = subprocess.run(validate_cmd, capture_output=True, text=True)
        
        if validate_result.returncode != 0:
            if os.path.exists(ringtone_path):
                os.remove(ringtone_path)
            return jsonify({'error': 'Invalid ringtone created'}), 500
        
        # Return the ringtone file for browser playback
        mimetype = 'audio/mpeg' if format_type == 'mp3' else 'audio/mp4'
        return send_file(ringtone_path, 
                        as_attachment=False,  # Don't download, just preview
                        mimetype=mimetype)
        
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    # Create download folder if it doesn't exist
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    
    # Production settings for Railway
    port = int(os.environ.get('PORT', 8003))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    app.run(debug=debug, host='0.0.0.0', port=port)
