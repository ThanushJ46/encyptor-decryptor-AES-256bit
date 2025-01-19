from flask import Flask, request, render_template_string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

app = Flask(__name__)

luxury_html = '''
<!doctype html>
<html>
<head>
  <title>Encrypt/Decryptproject1</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Open+Sans:wght@400;700&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Playfair Display', serif;
      background-color: #1d1f21;
      color: #f4f4f4;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background: linear-gradient(to right, #141E30, #243B55);
    }
    h1 {
      color: #E9B44C;
      text-align: center;
    }
    form {
      background-color: #2C2F33;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      max-width: 400px;
      width: 100%;
      text-align: center;
    }
    label {
      display: block;
      margin-bottom: 8px;
      font-size: 1.2em;
    }
    input[type="text"], input[type="submit"], button, textarea {
      width: calc(100% - 22px);
      padding: 10px;
      margin: 10px 0;
      border: none;
      border-radius: 5px;
      font-size: 1em;
    }
    input[type="submit"], button {
      background-color: #E9B44C;
      color: #1d1f21;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    input[type="submit"]:hover, button:hover {
      background-color: #DDAA00;
    }
    .result {
      margin-top: 20px;
      padding: 10px;
      background-color: #E9B44C;
      color: #1d1f21;
      border-radius: 5px;
    }
    textarea {
      width: calc(100% - 22px);
      height: 100px;
      padding: 10px;
      border-radius: 5px;
      margin: 10px 0;
    }
  </style>
  <script>
    function copyToClipboard(elementId) {
      var copyText = document.getElementById(elementId);
      copyText.select();
      document.execCommand("copy");
    }
    function clearFields() {
      document.querySelector('input[name="text"]').value = '';
      document.querySelector('input[name="key"]').value = '';
      document.getElementById('resultText').value = '';
    }
  </script>
</head>
<body>
  <div>
    <h1>Text Encryption/Decryption</h1>
    <form action="/" method="POST">
      <label>Text:</label>
      <input type="text" name="text" required><br>
      <label>Key:</label>
      <input type="text" name="key" required><br>
      <label>Action:</label>
      <input type="radio" name="action" value="encrypt" checked> Encrypt
      <input type="radio" name="action" value="decrypt"> Decrypt<br>
      <input type="submit" value="Submit">
      <button type="button" onclick="clearFields()">Clear</button>
    </form>
    {% if result %}
      <div class="result">
        <strong>Result:</strong>
        <textarea id="resultText" readonly>{{ result }}</textarea>
        <button onclick="copyToClipboard('resultText')">Copy to Clipboard</button>
      </div>
    {% endif %}
  </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ''
    if request.method == 'POST':
        text = request.form['text']
        key = request.form['key'].rjust(32)[:32]  # Ensure key is 32 bytes
        action = request.form['action']
        
        if action == 'encrypt':
            result = encrypt(text, key)
        else:
            result = decrypt(text, key)

    return render_template_string(luxury_html, result=result)

def encrypt(text, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    padded_text = pad(text.encode('utf-8'), AES.block_size)
    encrypted_text = base64.b64encode(cipher.encrypt(padded_text)).decode('utf-8')
    return encrypted_text

def decrypt(text, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    decrypted_text = unpad(cipher.decrypt(base64.b64decode(text)), AES.block_size).decode('utf-8')
    return decrypted_text

if __name__ == '__main__':
    app.run(debug=True)
