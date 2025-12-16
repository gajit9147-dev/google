from flask import Flask, request, make_response, render_template_string, redirect, url_for

app = Flask(__name__)

# Minimal template: in a real app serve static index.html; here we inline a tiny page that adds body.light if cookie says 'light'
TEMPLATE = """
<!doctype html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Theme Toggle (Flask)</title>
<style>
body { font-family: Arial, sans-serif; padding: 2rem; transition: background .3s, color .3s; }
body.light{ background:#fff; color:#111; }
body:not(.light){ background:#0b1220; color:#eef; }
.toggle { padding: .5rem 1rem; border-radius:8px; cursor:pointer; display:inline-block; background:rgba(255,255,255,.08); color:inherit; text-decoration:none; }
</style>
</head>
<body class="{{ 'light' if theme == 'light' else '' }}">
  <h1>Server-side Theme Toggle</h1>
  <p>Current theme: <strong>{{ theme }}</strong></p>
  <a class="toggle" href="{{ url_for('toggle') }}">Toggle theme (server)</a>
</body>
</html>
"""

@app.route("/")
def index():
    theme = request.cookies.get("site-theme", "dark")
    return render_template_string(TEMPLATE, theme=theme)

@app.route("/toggle")
def toggle():
    theme = request.cookies.get("site-theme", "dark")
    new = "light" if theme == "dark" else "dark"
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie("site-theme", new, max_age=60*60*24*365)  # 1 year
    return resp

if __name__ == "__main__":
    app.run(debug=True)