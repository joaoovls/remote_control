from flask import Flask, render_template, request, jsonify
import pyautogui
import base64
import io
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comando', methods=['POST'])
def controls():
    dados = request.get_json(force=True, silent=True)
    if not dados:
        return {"status": "error", "msg": "sem dados"}, 400

    acao = dados.get('acao')

    try:
        if acao == 'mouse_move':
            dx = dados.get('dx', 0)
            dy = dados.get('dy', 0)
            pyautogui.moveRel(dx, dy, duration=0)

        elif acao == 'mouse_click':
            btn = dados.get('button', 'left')
            pyautogui.click(button=btn)

        elif acao == 'mouse_double_click':
            pyautogui.doubleClick()

        elif acao == 'mouse_right_click':
            pyautogui.rightClick()

        elif acao == 'mouse_scroll':
            dy = dados.get('dy', 0)
            pyautogui.scroll(int(dy*20))

        elif acao == 'mouse_press':
            btn = dados.get('button', 'left')
            pyautogui.mouseDown(button=btn)

        elif acao == 'mouse_release':
            btn = dados.get('button', 'left')
            pyautogui.mouseUp(button=btn)

        elif acao == 'key_press':
            key = dados.get('key', '')
            if key:
                pyautogui.press(key)

        elif acao == 'hotkey':
            keys = dados.get('keys', [])
            if keys:
                pyautogui.hotkey(*keys)

        elif acao == 'type_text':
            text = dados.get('text', '')
            if text:
                try:
                    import pyperclip
                    pyperclip.copy(text)
                    pyautogui.hotkey('ctrl', 'v')
                except ImportError:
                    pyautogui.write(text, interval=0.03)

        elif acao == 'play_pause':
            pyautogui.press('playpause')

        elif acao == 'next_track':
            pyautogui.press('nexttrack')

        elif acao == 'prev_track':
            pyautogui.press('prevtrack')

        elif acao == 'volume_up':
            pyautogui.press('volumeup')

        elif acao == 'volume_down':
            pyautogui.press('volumedown')

        elif acao == 'mute':
            pyautogui.press('volumemute')

        elif acao == 'minimize':
            pyautogui.hotkey('super', 'down')   # Windows
            # pyautogui.hotkey('super', 'h')   # Linux

        elif acao == 'maximize':
            pyautogui.hotkey('super', 'up')

        elif acao == 'close_window':
            pyautogui.hotkey('alt', 'f4')

        elif acao == 'show_desktop':
            pyautogui.hotkey('super', 'd')

        elif acao == 'task_switch':
            pyautogui.hotkey('alt', 'tab')

        elif acao == 'task_manager':
            pyautogui.hotkey('ctrl', 'shift', 'esc')

        elif acao == 'screenshot':
            img = pyautogui.screenshot()
            # Reduz resolução para envio rápido
            w, h = img.size
            img = img.resize((w // 3, h // 3))
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=60)
            b64 = base64.b64encode(buf.getvalue()).decode()
            return {"status": "OK", "image": b64}, 200

        elif acao == 'get_screen_size':
            size = pyautogui.size()
            return {"status": "OK", "width": size.width, "height": size.height}, 200

        else:
            return {"status": "error", "msg": f"ação desconhecida: {acao}"}, 400

    except Exception as e:
        return {"status": "error", "msg": str(e)}, 500

    return {"status": "OK"}, 200


if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"  Acesse no celular: http://{local_ip}:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)