from flask import Flask, render_template, request, redirect, url_for
from PIL import Image

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(url_for('home'))
    
    image = request.files['image']
    if image.filename == '':
        return redirect(url_for('home'))

    # Simpan gambar yang diupload
    image.save('static/alam.jpg')

    return render_template('form.html')

@app.route('/crop', methods=['POST'])
def crop():
    size = request.form['size']
    position = request.form['position']

    # Parsing nilai size menjadi lebar dan tinggi crop
    width, height = map(int, size.split('x'))

    # Baca gambar yang diupload
    image = Image.open('static/alam.jpg')

    # Tentukan posisi crop berdasarkan nilai yang dipilih
    left, top = 0, 0  # Default: Top Left
    if position == 'top center':
        left = (image.width - width) // 2
    elif position == 'top right':
        left = image.width - width
    elif position == 'center left':
        top = (image.height - height) // 2
    elif position == 'center':
        left = (image.width - width) // 2
        top = (image.height - height) // 2
    elif position == 'center right':
        left = image.width - width
        top = (image.height - height) // 2
    elif position == 'bottom left':
        top = image.height - height
    elif position == 'bottom center':
        left = (image.width - width) // 2
        top = image.height - height
    elif position == 'bottom right':
        left = image.width - width
        top = image.height - height

    # Lakukan operasi crop sesuai dengan settingan
    # Menggunakan nilai width, height, left, dan top dari form
    cropped_image = image.crop((left, top, left + width, top + height))

    # Simpan gambar hasil crop
    cropped_image.save('static/cropped_image.jpg')

    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
