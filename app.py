from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PASSWORD'] = os.getenv('UPLOAD_PASSWORD')

SECTIONS = ['notes', 'dpps', 'books', 'lectures']

@app.route('/')
def home():
    return render_template('index.html', sections=SECTIONS)

@app.route('/files/<section>')
def files(section):
    if section not in SECTIONS:
        return "❌ Section not found"

    section_path = os.path.join(app.config['UPLOAD_FOLDER'], section)
    files = os.listdir(section_path) if os.path.exists(section_path) else []
    return render_template('files.html', section=section, files=files)
    @app.route('/admin/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        password = request.form.get('password')
        if password != app.config['PASSWORD']:
            return "❌ Incorrect password"

        uploaded_file = request.files['file']
        section = request.form.get('section')
        if uploaded_file and section in SECTIONS:
            section_path = os.path.join(app.config['UPLOAD_FOLDER'], section)
            os.makedirs(section_path, exist_ok=True)
            uploaded_file.save(os.path.join(section_path, uploaded_file.filename))
            return redirect(url_for('files', section=section))

    return render_template('upload.html', sections=SECTIONS)

# Serve files directly
@app.route('/uploads/<section>/<filename>')
def uploaded_file(section, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], section), filename)

if __name__ == '__main__':
    app.run(debug=True)
