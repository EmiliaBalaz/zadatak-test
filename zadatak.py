from flask import Flask, request, render_template_string
import os
import secrets
from lxml import etree  # Korišćenje lxml biblioteke

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # RCE ranjivost - unos komande
        command = request.form.get('command')
        if command:
            output = os.popen(command).read()
            return f'<pre>{output}</pre>'

        # XXE ranjivost - upload XML fajla
        if 'file' in request.files:
            file = request.files['file']
            try:
                # Parsiranje XML fajla sa lxml (ovde je ranjivo na XXE)
                xml_content = file.read()
                # Dodavanje zaštite protiv XXE
                tree = etree.fromstring(xml_content, parser=etree.XMLParser(resolve_entities=False))
                return 'XML procesiran bez XXE napada.'
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
