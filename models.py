from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    passport_number = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    
    tickets = db.relationship('Ticket', backref='passenger', lazy=True)

class Flight(db.Model):
    flight_number = db.Column(db.String(20), primary_key=True)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    tickets = db.relationship('Ticket', backref='flight', lazy=True)

    def book_seat(self):
        if self.seats_available > 0:
            self.seats_available -= 1
            return True
        return False

    def cancel_seat(self):
        if self.seats_available < self.capacity:
            self.seats_available += 1

class Ticket(db.Model):
    pnr = db.Column(db.String(8), primary_key=True, default=lambda: str(uuid.uuid4())[:8].upper())
    is_cancelled = db.Column(db.Boolean, default=False)
    
    passenger_id = db.Column(db.Integer, db.ForeignKey('passenger.id'), nullable=False)
    flight_number = db.Column(db.String(20), db.ForeignKey('flight.flight_number'), nullable=False)
