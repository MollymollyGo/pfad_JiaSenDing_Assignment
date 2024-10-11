from flask import Flask, render_template, request
import webbrowser
from threading import Timer

app = Flask(__name__)

# 启动应用时自动打开浏览器
def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        h = request.form.get('h', '')
        s = request.form.get('s', '')
        v = request.form.get('v', '')

        # 检查输入是否为空
        if not h or not s or not v:
            return "All fields are required!"

        # 转换为整数
        h = int(h)
        s = int(s)
        v = int(v)

        # HSV 转换为 CSS RGB 格式 (0-255)
        rgb = hsv_to_rgb(h, s, v)
        rgb_css = f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"

        # 渲染动态页面，传递颜色值
        return render_template('dynamic.html', color=rgb_css)

    except ValueError:
        return "Please enter a valid value!"

# HSV 转换为 RGB
def hsv_to_rgb(h, s, v):
    s /= 100
    v /= 100
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    r, g, b = (r + m) * 255, (g + m) * 255, (b + m) * 255
    return int(r), int(g), int(b)

if __name__ == '__main__':
    # 在Flask应用启动前打开浏览器
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)
