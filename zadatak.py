from flask import Flask, request, render_template_string
import os
from lxml import etree

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        command = request.form.get('command')
        if command:
            output = os.popen(command).read()
            return f'<pre>{output}</pre>'

        if 'file' in request.files:
            file = request.files['file']
            try:
                xml_content = file.read()
                # tu treba da je zastita od XXE
                tree = etree.fromstring(xml_content, parser=etree.XMLParser(resolve_entities=True))
                return 'XML procesiran (XXE omogućeno).'
            except etree.XMLSyntaxError as e:
                return f'Greška u XML-u: {str(e)}', 400

    return '''
        <form method="post">
            <label for="command">Unesite komandu:</label><br>
            <input type="text" id="command" name="command"><br>
            <input type="submit" value="Izvrši">
        </form>
        <form method="post" enctype="multipart/form-data">
            <label for="file">Pošaljite XML fajl:</label><br>
            <input type="file" id="file" name="file"><br>
            <input type="submit" value="Pošaljite XML">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)