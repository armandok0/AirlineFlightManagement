from pymongo import MongoClient
from flask import Flask, request, jsonify, Response, session
import json
from bson import ObjectId

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017')

# Choose DigitalAirlines database
db = client['DigitalAirlines']

# Choose collections
users = db['users']
flights = db['flights']
reservations = db['reservations']

# Initiate Flask App
app = Flask(__name__)
# For session
app.secret_key = '12345'


# / route
@app.route('/')
def index():
    return "Welcome to Digital Airlines"


#################### Register user ####################
@app.route('/register_user', methods=['POST'])
def register_user():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON content", status=500, mimetype='application/json')
    if not all(key in data for key in ['username', 'surname', 'email', 'password', 'date_of_birth', 'country', 'passport_number']):
        return Response("Incomplete information", status=500, mimetype='application/json')

    # User's Register Information
    username = data['username']
    surname = data['surname']
    email = data['email']
    password = data['password']
    date_of_birth = data['date_of_birth']
    country = data['country']
    passport_number = data['passport_number']

    # Check if user already exists
    already_user = users.find_one(
        {'$or': [{'email': email}, {'username': username}]})
    if already_user:
        return Response('User already exists', status=403, mimetype='application/json')

    # User's information to add
    user = {
        'username': username,
        'surname': surname,
        'email': email,
        'password': password,
        'date_of_birth': date_of_birth,
        'country': country,
        'passport_number': passport_number,
        'category': 'Simple User'
    }

    # Add user to the users collection
    users.insert_one(user)
    return Response('Registration successful, user was added to the MongoDB', status=200, mimetype='application/json')
########################################################


################# Login user ###########################
@app.route('/login_user', methods=['POST'])
def login_user():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON content", status=500, mimetype='application/json')
    if data is None:
        return Response("Bad request", status=500, mimetype='application/json')
    if not all(key in data for key in ['email', 'password']):
        return Response("Incomplete information", status=500, mimetype='application/json')

   # User's Login Information
    email = data['email']
    password = data['password']

    # Check if a user is already logged in
    if 'user' in session:
        return Response("A user is already logged in.", status=403, mimetype='application/json')

    # Search if email and password exists
    user = users.find_one({"email": email, "password": password})

    if user:
        # Convert ObjectId to string
        user['_id'] = str(user['_id'])

        # Check if admin is tring to log in
        if user.get('category') == 'admin':
            return Response("Admin is Unauthorized to Login.", status=403, mimetype='application/json')

        # Save user data in session
        session['user'] = user
        return Response(json.dumps(user), status=200, mimetype='application/json')
    else:
        return Response("Wrong email or password.Please Enter Again.", status=401, mimetype='application/json')
########################################################


################# Logout user ###########################
@app.route('/logout_user')
def logout_user():
    # Check if user is logged in
    if 'user' in session:
        # End the  session
        session.pop('user')
        return Response('Logged out', status=200, mimetype='application/json')
    else:
        return Response("User has not logged in", status=401, mimetype='application/json')
########################################################


################# Search flights ###########################
@app.route('/flight_search_user', methods=['POST'])
def flight_search_user():
    # Check if the user has logged in
    if 'user' not in session:
        return Response("User has not logged in", status=401, mimetype='application/json')

    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON content", status=500, mimetype='application/json')
    if data is None:
        return Response("Bad request", status=500, mimetype='application/json')

    # Search based on
    origin_airport = data.get('origin_airport')
    destination_airport = data.get('destination_airport')
    date_of_flight = data.get('date_of_flight')

    # Checks all the search criteria
    search_ = {}
    if origin_airport and destination_airport and date_of_flight:
        search_['origin_airport'] = origin_airport
        search_['destination_airport'] = destination_airport
        search_['date_of_flight'] = date_of_flight
    elif origin_airport and destination_airport:
        search_['origin_airport'] = origin_airport
        search_['destination_airport'] = destination_airport
    elif date_of_flight:
        search_['date_of_flight'] = date_of_flight

    flights_search = flights.find(search_)

    # Case to search all
    search = []
    for flight in flights_search:
        flight_data = {
            'Flight id': str(flight.get('_id')),
            'Origin Airport': str(flight.get('origin_airport')),
            'Destination Airport': str(flight.get('destination_airport')),
            'Date of flight': str(flight.get('date_of_flight'))
        }
        search.append(flight_data)

    # No flights found
    if not search:
        return Response("No flights found", status=404, mimetype='application/json')

    return jsonify(search)
#################################################################


########## Display flight details ############
# By flight id
@app.route('/display_flight_details_user', methods=['POST'])
def display_flight_details_user():
    # Check if user has logged in
    if 'user' not in session:
        return Response("User not logged in", status=401, mimetype='application/json')

    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON content", status=500, mimetype='application/json')
    if not all(key in data for key in ['flight_id']):
        return Response("Incomplete information", status=500, mimetype='application/json')

    # Flight id
    flight_id = data['flight_id']

    # Flight id to ObjectId
    try:
        flight_id = ObjectId(data['flight_id'])
    except Exception as e:
        return Response('Invalid flight ID', status=400, mimetype='application/json')

    # Find flight
    flight = flights.find_one({'_id': flight_id})
    if not flight:
        return Response('Flight not found', status=404, mimetype='application/json')

    # Output
    flight_details = {
        'Date of flight': flight['date_of_flight'],
        'Origin Airport': flight['origin_airport'],
        'Destination Airport': flight['destination_airport'],
        'Available Tickets': {
            'Economy': flight['economy_ticket'],
            'Business': flight['business_ticket']
        },
        'Ticket Prices': {
            'Economy': flight['economy_cost'],
            'Business': flight['business_cost']
        }
    }

    return jsonify(flight_details)
########################################################################


######################## Book a ticket #################################
# By flight id
@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    # Check if user has logged in
    if 'user' not in session:
        return Response("User not logged in", status=401, mimetype='application/json')

    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON content", status=500, mimetype='application/json')
    if not all(key in data for key in ['flight_id', 'name', 'surname', 'passport_number', 'date_of_birth', 'email', 'ticket_class']):
        return Response("Incomplete information", status=500, mimetype='application/json')

    # User's information
    user = session['user']
    user_id = user['_id']
    name = data['name']
    surname = data['surname']
    passport_number = data['passport_number']
    date_of_birth = data['date_of_birth']
    email = data['email']
    ticket_class = data['ticket_class']

    # Fliight id to ObjectId
    try:
        flight_id = ObjectId(data['flight_id'])
    except Exception as e:
        return Response('Invalid flight ID', status=400, mimetype='application/json')

    # Check if  flight exists
    flight = flights.find_one({'_id': flight_id})
    if not flight:
        return Response('Flight _id not found', status=404, mimetype='application/json')

    # Check if Ticket class is valid
    if ticket_class not in ['business', 'economy']:
        return Response('Invalid ticket class', status=400, mimetype='application/json')

    # Output
    reservation = {
        'user_id': user_id,
        'flight_id': str(flight_id),
        'name': name,
        'surname': surname,
        'passport_number': passport_number,
        'date_of_birth': date_of_birth,
        'email': email,
        'ticket_class': ticket_class
    }

    # Check if there are available tickets
    if ticket_class == 'business' and flight['business_ticket'] <= 0:
        return Response('No available business tickets', status=400, mimetype='application/json')
    elif ticket_class == 'economy' and flight['economy_ticket'] <= 0:
        return Response('No available economy tickets', status=400, mimetype='application/json')

    # Insert into collection
    reservations.insert_one(reservation)

    if ticket_class == 'business':
        # Update the number of business tickets
        flights.update_one({'_id': flight_id}, {
                           '$inc': {'business_ticket': -1}})
    else:
        # Update the number of economy tickets
        flights.update_one({'_id': flight_id}, {
                           '$inc': {'economy_ticket': -1}})

    return Response('Ticket booked successfully', status=200, mimetype='application/json')
########################################################


################# Display reservations ###########################
@app.route('/display_reservations_user')
def display_reservations_user():
    # Check if the user has logged in
    if 'user' not in session:
        return Response("User has not logged in", status=401, mimetype='application/json')

    user = session['user']
    user_id = user['_id']

    # Check if user has booking
    user_bookings = reservations.find({"user_id": user_id})
    if reservations.count_documents({"user_id": user_id}) == 0:
        return Response('User has no reservations', status=404, mimetype='application/json')

    # Output
    reservations_list = []
    for i in user_bookings:
        booking = {
            "Reservation Id": str(i.get('_id')),
            "Flight Id": str(i.get('flight_id')),
            "User Id": str(i.get('user_id')),
            "Name": i.get('name'),
            "Surname": i.get('surname'),
            "Passport Number": i.get('passport_number'),
            "Date of Birth": i.get('date_of_birth'),
            "Email": i.get('email'),
            "Ticket Class": i.get('ticket_class')
        }
        reservations_list.append(booking)

    # Return the bookings as JSON response
    return jsonify(reservations_list)
############################################################


#################### Display reservations details ####################
# By reservation id
@app.route('/display_reservation_details', methods=['POST'])
def display_reservation_details():
    # Check if the user has logged in
    if 'user' not in session:
        return Response("User has not logged in", status=401, mimetype='application/json')

    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON content", status=500, mimetype='application/json')
    if not all(key in data for key in ['reservation_id']):
        return Response("Incomplete information", status=500, mimetype='application/json')

    # User's information
    user = session['user']
    user_id = user['_id']

    reservation_id = data['reservation_id']

    # reservation_id to ObjectId
    try:
        reservation_id = ObjectId(reservation_id)
    except Exception as e:
        return Response('Invalid Reservation id', status=400, mimetype='application/json')

     # Reservations on this flight
    flight_reservations = reservations.find_one({'_id': reservation_id})
    if reservations.count_documents({'_id': reservation_id, 'user_id': user_id}) == 0:
        return Response('Reservation not found or this is not users reservation to view', status=400, mimetype='application/json')

    # Check if flight exists
    flight = flights.find_one(
        {'_id': ObjectId(flight_reservations['flight_id'])})
    if not flight:
        return Response('Flight not found', status=404, mimetype='application/json')

    # Prepare the reservation details response
    reservation_details = {
        'Origin': flight['origin_airport'],
        'Destination': flight['destination_airport'],
        'Date of flight': flight['date_of_flight'],
        'First name': flight_reservations['name'],
        'Last name': flight_reservations['surname'],
        'Passport number': flight_reservations['passport_number'],
        'Date of birth': flight_reservations['date_of_birth'],
        'Email': flight_reservations['email'],
        'Ticket class': flight_reservations['ticket_class'] if flight_reservations.get('ticket_class') is not None else ''
    }

    return jsonify(reservation_details)
######################################################################


############ Cancel reservation #######################################
# By reservation id
@app.route('/cancel_reservation', methods=['POST'])
def cancel_reservation():
    # Check if user is logged in
    if 'user' not in session:
        return Response("User has not logged in", status=401, mimetype='application/json')

    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON content", status=500, mimetype='application/json')
    if not all(key in data for key in ['reservation_id']):
        return Response("Incomplete information", status=500, mimetype='application/json')

    # User's information
    user = session['user']
    user_id = user['_id']
    reservation_id = data['reservation_id']

    # to ObjectId
    try:
        reservation_id = ObjectId(reservation_id)
    except Exception as e:
        return Response('Invalid reservation id', status=400, mimetype='application/json')

    # Check if  reservation exists
    reservation = reservations.find_one(
        {'_id': reservation_id, 'user_id': user_id})
    if not reservation:
        return Response('Reservation not found or this is not users reservation to cancel', status=404, mimetype='application/json')

    # Delete reservation
    reservations.delete_one({'_id': reservation_id})

    # to ObjectId
    try:
        flight_id = ObjectId(reservation['flight_id'])
    except Exception as e:
        return Response('Invalid flight id', status=400, mimetype='application/json')

    # Update
    if reservation['ticket_class'] == 'business':
        # Update the number of business tickets
        flights.update_one({'_id': flight_id}, {
                           '$inc': {'business_ticket': +1}})

    if reservation['ticket_class'] == 'economy':
        # Update the number of economy tickets
        flights.update_one({'_id': flight_id}, {
                           '$inc': {'economy_ticket': +1}})

    return Response('Reservation canceled successfully', status=200, mimetype='application/json')
######################################################################


################# Delete user account ###########################
@app.route('/delete_account', methods=['DELETE'])
def delete_account():
    # Check if user is logged in
    if 'user' in session:
        # Find user in session and get his email
        user = session['user']
        email = user['email']

        # Delete user account
        users.delete_one({'email': email})

        # End  session
        session.pop('user')

        return Response('Account deleted', status=200, mimetype='application/json')
    else:
        return Response("User has not logged in", status=401, mimetype='application/json')
####################################################################


################################################################################################################################################################
################################################################################################################################################################


################# Login Admin ###########################
@app.route('/login_admin', methods=['POST'])
def login_admin():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON content", status=500, mimetype='application/json')
    if data is None:
        return Response("Bad request", status=500, mimetype='application/json')
    if not all(key in data for key in ['email', 'password']):
        return Response("Incomplete information", status=500, mimetype='application/json')

    # Admin's login information
    email = data['email']
    password = data['password']

    # Check if an admin is already logged in
    if 'admin' in session:
        return Response("An admin is already logged in.", status=403, mimetype='application/json')

    # Search if email and password exist for an admin
    admin = users.find_one({"email": email, "password": password})

    if admin:
        # Convert ObjectId to string
        admin['_id'] = str(admin['_id'])

        # Check if user is tring to log in
        if admin.get('category') == 'Simple User':
            return Response("User is Unauthorized to Login.", status=401, mimetype='application/json')

        # Save admin data in session
        session['admin'] = admin
        return Response(json.dumps(admin), status=200, mimetype='application/json')
    else:
        return Response("Wrong email or password.Please Enter Again.", status=401, mimetype='application/json')
########################################################


################# Logout Admin ###########################
@app.route('/logout_admin')
def logout_admin():
    # Check if admin is logged in
    if 'admin' in session:
        # End the  session
        session.pop('admin')
        return Response('Logged out', status=200, mimetype='application/json')
    else:
        return Response("Admin has not logged in", status=401, mimetype='application/json')
########################################################


################# Create flight ########################
@app.route('/create_flight', methods=['POST'])
def create_flight():
    # Check if admin is logged in to procced
    if 'admin' not in session:
        return Response("Admin has not logged in", status=401, mimetype='application/json')

    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON content", status=500, mimetype='application/json')
    if data is None:
        return Response("Bad request", status=500, mimetype='application/json')
    if not all(key in data for key in ['origin_airport', 'destination_airport', 'date_of_flight', 'business_ticket', 'business_cost', 'economy_ticket', 'economy_cost']):
        return Response("Incomplete information", status=500, mimetype='application/json')

    # Flight information
    origin_airport = data['origin_airport']
    destination_airport = data['destination_airport']
    date_of_flight = data['date_of_flight']
    business_ticket = int(data['business_ticket'])
    business_cost = int(data['business_cost'])
    economy_ticket = int(data['economy_ticket'])
    economy_cost = int(data['economy_cost'])

    # Create a new flight
    flight = {
        'origin_airport': origin_airport,
        'destination_airport': destination_airport,
        'date_of_flight': date_of_flight,
        'business_ticket': business_ticket,
        'business_cost': business_cost,
        'economy_ticket': economy_ticket,
        'economy_cost': economy_cost
    }

    # Insert the flight into the flights collection
    flights.insert_one(flight)
    return Response('Flight created', status=200, mimetype='application/json')
########################################################


################# Update Ticket Prices ###########################
@app.route('/update_ticket_prices', methods=['PUT'])
def update_ticket_prices():
    # Check if admin has logged in
    if 'admin' not in session:
        return Response("Admin not logged in", status=401, mimetype='application/json')

    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON content", status=500, mimetype='application/json')
    if not all(key in data for key in ['flight_id', 'business_cost', 'economy_cost']):
        return Response("Incomplete information", status=500, mimetype='application/json')

    # New Ticket Price for flight information
    flight_id = data['flight_id']
    business_cost = int(data['business_cost'])
    economy_cost = int(data['economy_cost'])

    # flight ID to ObjectId
    try:
        flight_id = ObjectId(flight_id)
    except Exception as e:
        return Response('Invalid flight ID', status=400, mimetype='application/json')

    # Check if flight exists
    find_ticket_to_update = flights.find_one({'_id': flight_id})
    if not find_ticket_to_update:
        return Response('Flight _id not found', status=404, mimetype='application/json')

    # Update the flight with the new ticket prices
    flights.update_one({'_id': flight_id}, {
                       '$set': {'business_cost': business_cost, 'economy_cost': economy_cost}})
    return Response('Ticket prices updated', status=200, mimetype='application/json')
##############################################################


################# Delete flight ###########################
# By flight id
@app.route('/delete_flight', methods=['DELETE'])
def delete_flight():
    # Check if admin has logged in
    if 'admin' not in session:
        return Response("Admin not logged in", status=401, mimetype='application/json')

    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON content", status=500, mimetype='application/json')
    if not all(key in data for key in ['flight_id']):
        return Response("Incomplete information", status=500, mimetype='application/json')

    # Flight information
    flight_id = data['flight_id']

    # Flight ID to ObjectId
    try:
        flight_id = ObjectId(flight_id)
    except Exception as e:
        return Response('Invalid flight ID', status=400, mimetype='application/json')

    # Check if flight exists
    flight = flights.find_one({'_id': flight_id})
    if not flight:
        return Response('Flight not found', status=404, mimetype='application/json')

    # Check if there are reservations for the flight
    reservations_count = reservations.count_documents(
        {'flight_id': str(flight['_id'])})
    if reservations_count > 0:
        return Response('Cannot delete flight. Reservations exist.', status=400, mimetype='application/json')

    # Delete the flight
    flights.delete_one({'_id': flight['_id']})

    return Response('Flight deleted', status=200, mimetype='application/json')
########################################################


################# Search flights Admin ###########################
@app.route('/flight_search_admin', methods=['POST'])
def flight_search():
    # Check if the admin has logged in
    if 'admin' not in session:
        return Response("Admin has not logged in", status=401, mimetype='application/json')

    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON content", status=500, mimetype='application/json')

    # Search based on
    origin_airport = data.get('origin_airport')
    destination_airport = data.get('destination_airport')
    date_of_flight = data.get('date_of_flight')

    # Checks  the search criteria
    search_ = {}
    if origin_airport and destination_airport and date_of_flight:
        search_['origin_airport'] = origin_airport
        search_['destination_airport'] = destination_airport
        search_['date_of_flight'] = date_of_flight
    elif origin_airport and destination_airport:
        search_['origin_airport'] = origin_airport
        search_['destination_airport'] = destination_airport
    elif date_of_flight:
        search_['date_of_flight'] = date_of_flight

    flights_search = flights.find(search_)

    # OutPut
    search = []
    for flight in flights_search:
        flight_data = {
            'Flight id': str(flight.get('_id')),
            'Origin Airport': str(flight.get('origin_airport')),
            'Destination Airport': str(flight.get('destination_airport')),
            'Date of flight': str(flight.get('date_of_flight'))
        }
        search.append(flight_data)

    # Not Found
    if not search:
        return Response("No flights found", status=404, mimetype='application/json')

    return jsonify(search)
###################################################################


################# Display flights Details ###########################
# By flight id
@app.route('/display_flight_details_admin', methods=['POST'])
def display_flight_details_admin():
    # Check if admin has logged in
    if 'admin' not in session:
        return Response("Admin has not logged in", status=401, mimetype='application/json')

    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON content", status=500, mimetype='application/json')
    if not all(key in data for key in ['flight_id']):
        return Response("Incomplete information", status=500, mimetype='application/json')

    # Flight information
    flight_id = data['flight_id']

    # Flight ID to ObjectId
    try:
        flight_id = ObjectId(flight_id)
    except Exception as e:
        return Response('Invalid flight ID', status=400, mimetype='application/json')

    # Check if flight exists
    flight = flights.find_one({'_id': flight_id})
    if not flight:
        return Response('Flight not found', status=404, mimetype='application/json')

    # Reservations on this flight
    flight_reservations = reservations.find({'flight_id': str(flight['_id'])})
    if reservations.count_documents({'flight_id': str(flight['_id'])}) == 0:
        return Response('Reservations not found', status=404, mimetype='application/json')

    list_of_reservations_details = []
    flight_details = {}
    for reservation in flight_reservations:
        # Get user information based on the user_id in the reservation
        user_id = reservation['user_id']
        user = users.find_one({'_id': ObjectId(user_id)})
        name = user.get('username')
        surname = user.get('surname')

        # Get ticket class
        if 'ticket_class' in reservation:
            ticket_class = reservation['ticket_class']

        # Some of the Output
        reservation_details = {
            'First Name': name,
            'Last Name': surname,
            'Ticket Class': ticket_class
        }
        # Add the reservation details to the list
        list_of_reservations_details.append(reservation_details)

    # Add the list of reservations to the flight details
    flight_details['Reservations'] = list_of_reservations_details

    # Count the number of reservations
    reserved_tickets = reservations.count_documents(
        {'flight_id': str(flight['_id'])})
    # Count the number of reservations per class
    reserved_economy_tickets = reservations.count_documents(
        {'flight_id': str(flight['_id']), 'ticket_class': 'economy'})
    reserved_business_tickets = reservations.count_documents(
        {'flight_id': str(flight['_id']), 'ticket_class': 'business'})

    # Output
    flight_details = {
        'Origin Airport': flight['origin_airport'],
        'Destination Airport': flight['destination_airport'],
        'Total number of tickets': flight["business_ticket"] + flight["economy_ticket"]+reserved_tickets,
        'Total number of tickets per class': {
            'Economy': flight["economy_ticket"]+reserved_economy_tickets,
            'Business': flight["business_ticket"]+reserved_business_tickets
        },
        'Ticket cost per category': {
            'Economy': flight['economy_cost'],
            'Business': flight['business_cost']
        },
        'Available Tickets': flight["business_ticket"] + flight["economy_ticket"],
        'Available tickets per class': {
            'Economy': flight["economy_ticket"],
            'Business': flight["business_ticket"]
        },
        'Reservations': list_of_reservations_details
    }

    return jsonify(flight_details)
########################################################


# Run flask in debug mode in port 5000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
