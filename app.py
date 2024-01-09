from flask import Flask, request, render_template, send_file
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploaded_videos'
app.config['TRIMMED_FOLDER'] = 'trimmed_videos'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
  os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['TRIMMED_FOLDER']):
  os.makedirs(app.config['TRIMMED_FOLDER'])

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
  if 'file' not in request.files:
    return "No file part"
   
  file = request.files['file']
  start_time = float(request.form['start_time'])
  end_time = float(request.form['end_time'])
   
  if file.filename == '':
    return "No selected file"
   
  video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
  trimmed_video_path = os.path.join(app.config['TRIMMED_FOLDER'], file.filename)

  file.save(video_path)
  original_video_path = video_path


   
  # Provide original_video and trimmed_video variables for template rendering
  original_video = os.path.basename(video_path)
  with VideoFileClip(video_path) as video:
    trimmed_video = video.subclip(start_time, end_time)
    trimmed_video.write_videofile(trimmed_video_path)

  # os.remove(video_path)
   
  return render_template('index.html', original_video=original_video, trimmed_video=os.path.basename(trimmed_video_path), original_video_path=original_video_path)

# ... (rest of your Flask code remains unchanged)


@app.route('/trimmed_videos/<filename>')
def trimmed_video(filename):
  return send_file(os.path.join(app.config['TRIMMED_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
  app.run(debug=True)