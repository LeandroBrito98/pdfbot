from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from fpdf import FPDF
import os
from PIL import Image
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'files' not in request.files:
        return "Nenhum arquivo enviado", 400

    files = request.files.getlist('files')
    if not files:
        return "Nenhum arquivo selecionado", 400

    pdf = FPDF()
    pdf.set_auto_page_break(0)

    for file in files:
        filename = secure_filename(file.filename)
        image = Image.open(file.stream)
        image_rgb = image.convert('RGB')
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_rgb.save(temp_path)
        pdf.add_page()
        pdf.image(temp_path, x=10, y=10, w=190)
        os.remove(temp_path)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return send_file(pdf_output, mimetype='application/pdf', as_attachment=True, download_name='arquivo.pdf')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='127.0.0.1', port=5000, debug=True)
