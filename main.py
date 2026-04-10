from models import Flight, Passenger
from services import FlightService, BookingService

def get_int_input(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_float_input(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid decimal number.")


def admin_menu(flight_service: FlightService):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Flight")
        print("2. View All Flights")
        print("0. Back to Main Menu")
        choice = get_int_input("Select an option: ")

        if choice == 1:
            flight_no = input("Enter Flight Number: ")
            source = input("Enter Source: ")
            dest = input("Enter Destination: ")
            date = input("Enter Date (YYYY-MM-DD): ")
            capacity = get_int_input("Enter Capacity: ")
            price = get_float_input("Enter Price: ")
            
            new_flight = Flight(flight_no, source, dest, date, capacity, price)
            flight_service.add_flight(new_flight)
            print("Flight added successfully!")
            
        elif choice == 2:
            flight_service.display_all_flights()
        elif choice == 0:
            break
        else:
            print("Invalid Choice.")

def passenger_menu(flight_service: FlightService, booking_service: BookingService):
    while True:
        print("\n--- Passenger Menu ---")
        print("1. Search Flights")
        print("2. Book a Ticket")
        print("3. Cancel a Ticket")
        print("4. View Ticket Details")
        print("0. Back to Main Menu")
        choice = get_int_input("Select an option: ")

        if choice == 1:
            src = input("Enter Source: ")
            dest = input("Enter Destination: ")
            results = flight_service.search_flights(src, dest)
            if not results:
                print("No flights found for this route.")
            else:
                print("Available Flights:")
                for f in results:
                    print(f)
                    
        elif choice == 2:
            flight_num = input("Enter Flight Number you wish to book: ")
            flight = flight_service.get_flight_by_number(flight_num)
            if flight:
                pid = get_int_input("Enter Passenger ID: ")
                name = input("Enter Name: ")
                passport = input("Enter Passport Number: ")
                contact = input("Enter Contact Number: ")
                
                passenger = Passenger(pid, name, passport, contact)
                booking_service.book_ticket(passenger, flight)
            else:
                print("Flight not found.")
                
        elif choice == 3:
            pnr = input("Enter PNR to Cancel: ")
            booking_service.cancel_ticket(pnr)
            
        elif choice == 4:
            pnr = input("Enter PNR to View: ")
            booking_service.view_ticket(pnr)
            
        elif choice == 0:
            break
        else:
            print("Invalid Choice.")


def main():
    flight_service = FlightService()
    booking_service = BookingService()

    print("Welcome to the Airlines Management System (Python Version)!")
    
    while True:
        print("\n--- Main Menu ---")
        print("1. Admin Menu")
        print("2. Passenger Menu")
        print("0. Exit")
        choice = get_int_input("Select an option: ")

        if choice == 1:
            admin_menu(flight_service)
        elif choice == 2:
            passenger_menu(flight_service, booking_service)
        elif choice == 0:
            print("Thank you for using the Airlines Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
