from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    user_agent: str = request.headers.get("User-Agent")
    icon_per_line:int = 6 if "Mobile" in user_agent else 9
    return render_template('index.html', icon_per_line = icon_per_line)

if __name__ == '__main__':
    app.run(debug=True)