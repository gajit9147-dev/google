from datetime import datetime

class Event:
    def __init__(self, id, title, description, date, location, organizer):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.location = location
        self.organizer = organizer
        self.attendees = []

class EventManager:
    def __init__(self):
        self.events = {}
        self.next_id = 1
    
    def create_event(self, title, description, date, location, organizer):
        event = Event(self.next_id, title, description, date, location, organizer)
        self.events[self.next_id] = event
        self.next_id += 1
        return event
    
    def get_event(self, event_id):
        return self.events.get(event_id)
    
    def get_all_events(self):
        return list(self.events.values())
    
    def register_attendee(self, event_id, attendee_name):
        event = self.get_event(event_id)
        if event and attendee_name not in event.attendees:
            event.attendees.append(attendee_name)
            return True
        return False