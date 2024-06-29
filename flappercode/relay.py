# Relay code

import RPi.GPIO as GPIO
import time
import psycopg2

# Database connection details (replace with your actual values)
HOST = "200.10.10.230"
USER = "postgres"
PASSWORD = "Lahore*999"  # Replace with your password
DATABASE = "postgres"

# GPIO pin for relay (replace with your actual pin)
RELAY_PIN = 18

def connect_to_database():
    """Connects to the database and returns a connection object or None on error."""
    try:
        conn = psycopg2.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        return conn
    except (Exception, psycopg2.Error) as err:
        print(f"Error connecting to database: {err}")
        return None

def verify_and_blacklist_number(number):
    """Verifies the number in the database and blacklists it (if not already blacklisted)."""
    conn = connect_to_database()

    if conn:
        try:
            cursor = conn.cursor()

            # Check if number exists and is not blacklisted
            cursor.execute("SELECT * FROM codes WHERE code = %s AND used = 'false'", (number,))
            row = cursor.fetchone()

            if row:  # Number found and not blacklisted
                # Open relay (replace with your relay activation logic)
                GPIO.setup(RELAY_PIN, GPIO.OUT)  # One-time setup for relay pin as output
                #GPIO.output(RELAY_PIN, GPIO.HIGH)  # Activate relay
                print(f"Number {number} verified. Access granted. Blacklisting...")

                # Blacklist logic (update flag in database)
                cursor.execute("UPDATE codes SET used = 'true' WHERE code = %s", (number,))
                conn.commit()
                print(f"Number {number} blacklisted in database.")

                # Delay for 1 second before closing relay
                time.sleep(1)  # Delay for 1 second

                # Close relay
                GPIO.setup(RELAY_PIN, GPIO.IN)  # Deactivate relay
                print(f"Relay closed after access.")

            else:  # Number not found or blacklisted
                print(f"Number {number} not found or already blacklisted. Access denied.")

        except (Exception, psycopg2.Error) as err:
            print(f"Database error: {err}")

        finally:
            if conn:
                cursor.close()
                conn.close()

    else:
        print("Failed to connect to database.")

def delete_number(number):
    """Deletes a number from the database (if it exists)."""
    conn = connect_to_database()

    if conn:
        try:
            cursor = conn.cursor()

            # Delete the number (assuming unique 'code' column)
            cursor.execute("DELETE FROM codes WHERE code = %s", (number,))
            conn.commit()
            print(f"Number {number} deleted from database.")

        except (Exception, psycopg2.Error) as err:
            print(f"Database error: {err}")

        finally:
            if conn:
                cursor.close()
                conn.close()

    else:
        print("Failed to connect to database.")

def main():
    # Set up GPIO (one-time setup outside the loop)
    GPIO.setmode(GPIO.BCM)
    #GPIO.setup(RELAY_PIN, GPIO.OUT)  # Configure relay pin as output

    while True:  # Continuous loop for code input
        try:
            # Get number input (replace with your actual input method)
            number = input("Enter code (or 'd' to delete): ")

            if number.lower() == 'd':  # Handle deletion request
                delete_number(input("Enter number to delete: "))
            else:
                # Verify and blacklist the number (if not already blacklisted)
                verify_and_blacklist_number(number)

        except KeyboardInterrupt:
            # Handle keyboard interrupt (optional)
            print("Exiting...")
            break  # Exit the loop on Ctrl+C

    # Clean up GPIO (optional)
    GPIO.cleanup()

if __name__ == "__main__":
    main()





