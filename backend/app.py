from flask import Flask, render_template, request
import pyautogui

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comands', methods=['POST'])
def controls():
    dados = request.json
    acao = dados.get('acao')

    if acao == 'play_pause':
        pyautogui.press('playpause')
    elif acao == 'volume_up':
        pyautogui.press('volumeup')
    elif acao == 'volume_down':
        pyautogui.press('volumedown')
    elif acao == 'mute':
        pyautogui.press('volumemute')

    return {"status": 'OK'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)