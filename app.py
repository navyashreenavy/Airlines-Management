from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Passenger, Flight, Ticket
import os

app = Flask(__name__)
app.secret_key = 'super_secret_beautiful_airlines'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///airlines.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def create_tables():
    # Attempt to create tables and dummy data only if tables don't exist
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()
    if not Flight.query.first():
        f1 = Flight(flight_number="AI101", source="New York", destination="London", date="2026-05-01", capacity=150, seats_available=150, price=500.0)
        f2 = Flight(flight_number="BA202", source="London", destination="Paris", date="2026-05-02", capacity=100, seats_available=100, price=150.0)
        f3 = Flight(flight_number="DL303", source="New York", destination="Los Angeles", date="2026-05-03", capacity=200, seats_available=200, price=300.0)
        db.session.add_all([f1, f2, f3])
        db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/flights')
def flights():
    query = Flight.query
    search_q = request.args.get('q', '')
    if search_q:
        query = query.filter((Flight.source.ilike(f'%{search_q}%')) | (Flight.destination.ilike(f'%{search_q}%')))
    
    flights_list = query.all()
    return render_template('flights.html', flights=flights_list, search_q=search_q)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        flight_number = request.form.get('flight_number')
        source = request.form.get('source')
        destination = request.form.get('destination')
        date = request.form.get('date')
        capacity = int(request.form.get('capacity', 0))
        price = float(request.form.get('price', 0.0))
        
        new_flight = Flight(flight_number=flight_number, source=source, destination=destination, date=date, capacity=capacity, seats_available=capacity, price=price)
        db.session.add(new_flight)
        try:
            db.session.commit()
            flash('Flight added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Failed to add flight. Ensure flight number is unique.', 'error')
            
        return redirect(url_for('admin'))
        
    return render_template('admin.html')

@app.route('/book/<flight_number>', methods=['GET', 'POST'])
def book(flight_number):
    flight = Flight.query.get_or_404(flight_number)
    if request.method == 'POST':
        name = request.form.get('name')
        passport = request.form.get('passport')
        contact = request.form.get('contact')
        
        # Check passenger exists by passport to be smart, otherwise create new
        passenger = Passenger.query.filter_by(passport_number=passport).first()
        if not passenger:
            passenger = Passenger(name=name, passport_number=passport, contact_number=contact)
            db.session.add(passenger)
            db.session.commit()
            
        if flight.book_seat():
            ticket = Ticket(passenger_id=passenger.id, flight_number=flight.flight_number)
            db.session.add(ticket)
            db.session.commit()
            flash(f'Ticket booked successfully! Your PNR is {ticket.pnr}', 'success')
            return redirect(url_for('my_tickets', pnr=ticket.pnr))
        else:
            flash('Sorry, no seats available on this flight.', 'error')
            return redirect(url_for('flights'))
            
    return render_template('book.html', flight=flight)

@app.route('/my_tickets', methods=['GET', 'POST'])
def my_tickets():
    ticket = None
    if request.method == 'POST':
        pnr = request.form.get('pnr')
        ticket = Ticket.query.get(pnr)
        if not ticket:
            flash('Ticket not found. Check your PNR.', 'error')
            
    # Allow GET with PNR query parameter
    pnr_query = request.args.get('pnr')
    if pnr_query:
        ticket = Ticket.query.get(pnr_query)
        
    return render_template('ticket.html', ticket=ticket)

@app.route('/cancel/<pnr>', methods=['POST'])
def cancel(pnr):
    ticket = Ticket.query.get_or_404(pnr)
    if not ticket.is_cancelled:
        ticket.is_cancelled = True
        ticket.flight.cancel_seat()
        db.session.commit()
        flash(f'Ticket {pnr} has been successfully cancelled.', 'success')
    else:
        flash('Ticket is already cancelled.', 'warning')
    return redirect(url_for('my_tickets', pnr=pnr))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
