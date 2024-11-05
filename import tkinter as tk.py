import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import mysql.connector

# Establish MySQL connection
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Chennaichennai$',
            database='ticket_booking'
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None

class OnlineTicketBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Ticket Booking System")

        # Initialize variables
        self.events = [
            {"name": "Concert", "date": "2024-07-01", "venue": " venkateswara party Hall", "price": 50, "tickets_available": 100},
            {"name": "Theater Play", "date": "2024-07-10", "venue": "Inox Theater", "price": 30, "tickets_available": 50},
            {"name": "Sports Event", "date": "2024-08-05", "venue": " nehru Stadium", "price": 40, "tickets_available": 200},
            # Add more events as needed
        ]
        self.bookings = []


        
        # Main frame
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack()

        # Display available events
        self.display_available_events()

    def display_available_events(self):
        for event in self.events:
            tk.Label(self.main_frame, text=f"{event['name']} ({event['date']} @ {event['venue']}) - ${event['price']} per ticket").pack()
            tk.Button(self.main_frame, text="Book Tickets", command=lambda e=event: self.book_tickets(e)).pack()
        tk.Button(self.main_frame, text="View Bookings", command=self.view_bookings).pack()

    def book_tickets(self, event):
        self.main_frame.pack_forget()

        self.booking_frame = tk.Frame(self.root, padx=20, pady=20)
        self.booking_frame.pack()

        tk.Label(self.booking_frame, text=f"Booking Tickets for {event['name']} ({event['date']} @ {event['venue']}) - ${event['price']} per ticket").grid(row=0, columnspan=2, pady=10)
        tk.Label(self.booking_frame, text="Number of Tickets:").grid(row=1, column=0)
        self.tickets_entry = tk.Entry(self.booking_frame)
        self.tickets_entry.grid(row=1, column=1)
        tk.Label(self.booking_frame, text="Name:").grid(row=2, column=0)
        self.name_entry = tk.Entry(self.booking_frame)
        self.name_entry.grid(row=2, column=1)
        tk.Label(self.booking_frame, text="Email:").grid(row=3, column=0)
        self.email_entry = tk.Entry(self.booking_frame)
        self.email_entry.grid(row=3, column=1)
        tk.Label(self.booking_frame, text="Contact Number:").grid(row=4, column=0)
        self.contact_entry = tk.Entry(self.booking_frame)
        self.contact_entry.grid(row=4, column=1)
        tk.Button(self.booking_frame, text="Confirm Booking", command=lambda: self.confirm_booking(event)).grid(row=5, columnspan=2, pady=10)

    def confirm_booking(self, event):
        try:
            num_tickets = int(self.tickets_entry.get())
            name = self.name_entry.get()
            email = self.email_entry.get()
            contact = self.contact_entry.get()

            if num_tickets <= 0:
                messagebox.showerror("Booking Error", "Please enter a valid number of tickets.")
                return

            if event['tickets_available'] < num_tickets:
                messagebox.showerror("Booking Error", "Not enough tickets available.")
                return

            total_price = event['price'] * num_tickets
            booking_details = {
                "event_name": event['name'],
                "date": event['date'],
                "venue": event['venue'],
                "price_per_ticket": event['price'],
                "num_tickets": num_tickets,
                "total_price": total_price,
                "name": name,
                "email": email,
                "contact": contact,
                "booking_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            self.bookings.append(booking_details)
            event['tickets_available'] -= num_tickets

            messagebox.showinfo("Booking Confirmation", "Booking confirmed successfully!")
            self.booking_frame.pack_forget()
            self.main_frame.pack()
            self.display_available_events()

        except ValueError:
            messagebox.showerror("Booking Error", "Please enter a valid number of tickets.")

    def view_bookings(self):
        self.main_frame.pack_forget()

        bookings_window = tk.Toplevel(self.root)
        bookings_window.title("Current Bookings")

        if self.bookings:
            for idx, booking in enumerate(self.bookings, start=1):
                tk.Label(bookings_window, text=f"Booking {idx}: {booking['event_name']} ({booking['date']} @ {booking['venue']}) - {booking['num_tickets']} tickets - Total: ${booking['total_price']}").pack()
        else:
            tk.Label(bookings_window, text="No bookings yet.").pack()

        tk.Button(bookings_window, text="Close", command=bookings_window.destroy).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = OnlineTicketBookingSystem(root)
    root.mainloop()
