from models import Flight, Passenger, Ticket

class FlightService:
    def __init__(self):
        self.flights = []
        # Add dummy data
        self.add_flight(Flight("AI101", "New York", "London", "2026-05-01", 150, 500.0))
        self.add_flight(Flight("BA202", "London", "Paris", "2026-05-02", 100, 150.0))
        self.add_flight(Flight("DL303", "New York", "Los Angeles", "2026-05-03", 200, 300.0))

    def add_flight(self, flight: Flight):
        self.flights.append(flight)

    def display_all_flights(self):
        if not self.flights:
            print("No flights available.")
            return
        for f in self.flights:
            print(f)

    def search_flights(self, source: str, destination: str):
        return [f for f in self.flights if f.source.lower() == source.lower() and f.destination.lower() == destination.lower()]

    def get_flight_by_number(self, flight_number: str):
        for f in self.flights:
            if f.flight_number.lower() == flight_number.lower():
                return f
        return None


class BookingService:
    def __init__(self):
        self.ticket_database = {}

    def book_ticket(self, passenger: Passenger, flight: Flight) -> Ticket | None:
        if flight.book_seat():
            ticket = Ticket(passenger, flight)
            self.ticket_database[ticket.pnr] = ticket
            print(f"Ticket booked successfully! PNR: {ticket.pnr}")
            return ticket
        else:
            print("Sorry, no seats available on this flight.")
            return None

    def cancel_ticket(self, pnr: str) -> bool:
        ticket = self.ticket_database.get(pnr)
        if ticket and not ticket.is_cancelled:
            ticket.cancel()
            ticket.flight.cancel_seat()
            print(f"Ticket {pnr} has been cancelled.")
            return True
        print("Invalid PNR or ticket is already cancelled.")
        return False

    def view_ticket(self, pnr: str):
        ticket = self.ticket_database.get(pnr)
        if ticket:
            print(ticket)
        else:
            print("Ticket not found.")
