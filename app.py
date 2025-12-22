from flask import Flask, request, make_response, render_template_string, redirect, url_for
from models import EventManager
from datetime import datetime

app = Flask(__name__)
event_manager = EventManager()

MAIN_TEMPLATE = """
<!doctype html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Event Manager</title>
<style>
body { font-family: Arial, sans-serif; padding: 2rem; transition: background .3s, color .3s; }
body.light{ background:#fff; color:#111; }
body:not(.light){ background:#0b1220; color:#eef; }
.toggle { padding: .5rem 1rem; border-radius:8px; cursor:pointer; display:inline-block; background:rgba(255,255,255,.08); color:inherit; text-decoration:none; margin-bottom:1rem; }
.event { border:1px solid #333; padding:1rem; margin:1rem 0; border-radius:8px; }
.light .event { border-color:#ddd; }
form { margin:1rem 0; }
input, textarea { padding:.5rem; margin:.25rem; border-radius:4px; border:1px solid #333; background:rgba(255,255,255,.1); color:inherit; }
.light input, .light textarea { background:#fff; border-color:#ddd; color:#111; }
button { padding:.5rem 1rem; border-radius:4px; border:none; background:#007acc; color:#fff; cursor:pointer; }
</style>
</head>
<body class="{{ 'light' if theme == 'light' else '' }}">
  <a class="toggle" href="{{ url_for('toggle') }}">Toggle theme</a>
  <h1>Event Manager</h1>
  {{ content }}
</body>
</html>
"""

@app.route("/")
def index():
    theme = request.cookies.get("site-theme", "dark")
    events = event_manager.get_all_events()
    content = f"""
    <h2>All Events</h2>
    <a href="{url_for('create_event')}">Create New Event</a>
    {''.join([f'<div class="event"><h3>{e.title}</h3><p>{e.description}</p><p>Date: {e.date}</p><p>Location: {e.location}</p><p>Organizer: {e.organizer}</p><p>Attendees: {len(e.attendees)}</p><a href="{url_for("view_event", event_id=e.id)}">View Details</a></div>' for e in events]) if events else '<p>No events yet. <a href="' + url_for('create_event') + '">Create one!</a></p>'}
    """
    return render_template_string(MAIN_TEMPLATE, theme=theme, content=content)

@app.route("/toggle")
def toggle():
    theme = request.cookies.get("site-theme", "dark")
    new = "light" if theme == "dark" else "dark"
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie("site-theme", new, max_age=60*60*24*365)
    return resp

@app.route("/create", methods=["GET", "POST"])
def create_event():
    theme = request.cookies.get("site-theme", "dark")
    if request.method == "POST":
        event_manager.create_event(
            request.form["title"],
            request.form["description"],
            request.form["date"],
            request.form["location"],
            request.form["organizer"]
        )
        return redirect(url_for('index'))
    
    content = f"""
    <h2>Create Event</h2>
    <form method="post">
        <input name="title" placeholder="Event Title" required><br>
        <textarea name="description" placeholder="Description" required></textarea><br>
        <input name="date" type="datetime-local" required><br>
        <input name="location" placeholder="Location" required><br>
        <input name="organizer" placeholder="Organizer Name" required><br>
        <button type="submit">Create Event</button>
    </form>
    <a href="{url_for('index')}">Back to Events</a>
    """
    return render_template_string(MAIN_TEMPLATE, theme=theme, content=content)

@app.route("/event/<int:event_id>")
def view_event(event_id):
    theme = request.cookies.get("site-theme", "dark")
    event = event_manager.get_event(event_id)
    if not event:
        return redirect(url_for('index'))
    
    content = f"""
    <h2>{event.title}</h2>
    <p><strong>Description:</strong> {event.description}</p>
    <p><strong>Date:</strong> {event.date}</p>
    <p><strong>Location:</strong> {event.location}</p>
    <p><strong>Organizer:</strong> {event.organizer}</p>
    <h3>Attendees ({len(event.attendees)})</h3>
    {'<ul>' + ''.join([f'<li>{name}</li>' for name in event.attendees]) + '</ul>' if event.attendees else '<p>No attendees yet.</p>'}
    <form method="post" action="{url_for('register', event_id=event_id)}">
        <input name="name" placeholder="Your Name" required>
        <button type="submit">Register</button>
    </form>
    <a href="{url_for('index')}">Back to Events</a>
    """
    return render_template_string(MAIN_TEMPLATE, theme=theme, content=content)

@app.route("/register/<int:event_id>", methods=["POST"])
def register(event_id):
    event_manager.register_attendee(event_id, request.form["name"])
    return redirect(url_for('view_event', event_id=event_id))

if __name__ == "__main__":
    app.run(debug=True)
    