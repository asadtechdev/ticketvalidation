from datetime import date
from flask import Flask, render_template, request

app = Flask(__name__)

def validate_ticket(ticket_number):
  """
  This function validates the ticket number and updates the used tickets list.

  Args:
      ticket_number: The ticket number entered by the user.

  Returns:
      A string indicating if the ticket is valid or not.
  """
  global valid_range, used_tickets

  if ticket_number in valid_range:
    valid_range.remove(ticket_number)
    used_tickets.append(ticket_number)
    return "Valid Ticket"
  else:
    return "Invalid Ticket"

# Initialize valid ticket range (1 to 100)
#valid_range = list(range(040400000, 040420000))


# DDMM Policy function
def get_valid_ticket_range(today=date.today()):
  """
  This function generates a valid ticket range based on the given date (default is today).

  Args:
      today (date, optional): The date to use for generating the range. Defaults to date.today().

  Returns:
      list: A list of integers representing the valid ticket range (DDMM00000 to DDMM20000).
  """

  # Extract day and month from the date
  day = today.day
  month = today.month

  # Construct the lower and upper bounds of the range (as strings)
  lower_bound = f"{day:02d}{month:02d}20000000"
  upper_bound = f"{day:02d}{month:02d}21000000"

  # Convert strings to integers for the valid range
  return list(range(int(lower_bound), int(upper_bound) + 1))

# Example usage (assuming you've fixed the leading zero issue in your `app.py`)
valid_range = get_valid_ticket_range()





# Initialize used tickets list (empty)
used_tickets = []

while True:
  # Get ticket number input
  ticket_number = input("Enter ticket number (or 'q' to quit): ")

  # Check for quit option
  #if ticket_number.lower() == 'q':
    #break

  # Try converting input to integer (handle non-numeric input)
  try:
    ticket_number = int(ticket_number)
  except ValueError:
    print("Invalid input. Please enter a number.")
    continue

  # Validate ticket and print result
  result = validate_ticket(ticket_number)
  print(result)

print("Ticket validation program terminated.")


@app.route("/", methods=["GET", "POST"])
def validate():
    # Get ticket number from form if submitted (POST)
    if request.method == "POST":
        ticket_number = int(request.form["ticket_number"])
        result = validate_ticket(ticket_number)
        #return {"result": result}

    else:
        result = None  # No previous validation

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  # Run the app on port 5000






