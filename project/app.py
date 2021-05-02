from random import randint
from datetime import date
import string
import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/info')
def info():
  return render_template('info.html')

@app.route('/')
def main():
  return render_template('main.html', names_array = [f for f in os.listdir('./static') if allowed_file(f)])

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'],
                             filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('uploaded_file', filename=filename))
  return render_template('upload.html')

@app.route('/notes')
def notes_base():
  return render_template('notes.html')

@app.route('/notes', methods=['GET', 'POST'])
def make_note():
  inputter = request.form['text_box']
  name = date.today().strftime("%-d-%m-%Y-") 
  random_number = randint(0, 100)
  name = 'note' + name + '-' + str(random_number) + '.txt'
  if request.method == 'POST':
    with open('./static/' + name, 'w+') as f:
      f.write(str(inputter))
  return render_template('notes.html')

if __name__ == '__main__':
  app.run()
