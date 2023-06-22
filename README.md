# Πληροφοριακά Συστήματα - Υποχρεωτική Εργασία
Η εργασία υλοποιήθηκε από: ΑΡΜΑΝΤΟ ΚΟΣΤΑΣ, e20073


## Τρόπος Εκτέλεσης 
Το πρόγραμμα εκτελείται στην πόρτα 5000 με flask και η Mongodb στην πόρτα 27017. 

Έχουμε ένα database DigitalAirlines με collections users, flights, reservations.
Δημιουργούμε το container ως εξής: 
```bash
docker-compose up -d
```
Με την χρήση του postman μπορούμε να στέλνουμε μεθόδους.

#
## /register_user
Στην υπηρεσία υπάρχουν δύο κατηγορίες χρηστών:

• Οι απλοί χρήστες.

• Οι διαχειριστές.

Ο διαχειριστής, θα είναι ένας χρήστης ο οποίος θα υπάρχει ήδη στο σύστημα.

Για να δημιουργήσουμε έναν νέο απλό χρήστη θα στείλουμε: POST http://localhost:5000/register_user

Η μορφή με την οποία πρέπει να δοθεί είναι η εξής:
```json
{
    "username":"user7",
    "surname":"sur7",
    "email":"user7@gmail.com",
    "password":"123",
    "date_of_birth":"12-12-1998",
    "country":"Greece",
    "passport_number":"AK99"
}
```
Σε περίπτωση επιτυχής εκτέλεσης εμφανίζεται το μήνυμα: Registration successful, user was added to the MongoDB

Σε περίπτωση που δοθεί email η username ίδιο με κάποιον άλλο χρήστη στο σύστημα εμφανίζεται το μήνυμα: User already exists
#
## /login_user
Για να γίνει είσοδος στην υπηρεσία από τον χρήστη θα στείλουμε: POST http://localhost:5000/login_user

Η μορφή με την οποία πρέπει να δοθεί είναι η εξής:
```json
{
    "email":"user7@gmail.com",
    "password":"123"
}
```
Σε περίπτωση επιτυχής εκτέλεσης εμφανίζονται τα στοιχεία του χρήστη που έκανε login.

Αν τα στοιχεία του login είναι λάθος εμφανίζεται το μήνυμα: Wrong email or password.Please Enter Again.

Αν κάποιος χρήστης προσπαθεί να κάνει login ενώ είναι κάποιος άλλος χρήστης μέσα στην υπηρεσία  τότε εμφανίζει το μήνυμα: A user is already logged in.

Αν κάποιος admin προσπαθεί να κάνει login εμφανίζει το μήνυμα: Admin is Unauthorized to Login. 

## /logout_user
Για να γίνει έξοδος απο την υπηρεσία από τον χρήστη θα στείλουμε: GET http://localhost:5000/logout_user

Σε περίπτωση επιτυχής εκτέλεσης εμφανίζεται το μήνυμα: Logged out

Σε περίπτωση που ο χρήστης δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: User has not logged in 
#
## /flight_search_user
Για να κάνει αναζήτηση πτήσεων ένας χρήστης θα στείλουμε: POST http://localhost:5000/flight_search_user

Η μορφή με την οποία πρέπει να δοθεί είναι η εξής:
```json
{
    "origin_airport": "Athens",
    "destination_airport": "Thess",
    "date_of_flight": "13-05-2023"
}
```
```json
{
    "origin_airport": "Athens",
    "destination_airport": "Thess"
}
```
```json
{
    "date_of_flight": "13-05-2023"
}
```
Σε περίπτωση που δοθεί κενό το δεχόμαστε ώστε να εμφανίσουμε όλες τις διαθέσιμες πτήσεις

Σε περίπτωση που ο χρήστης δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: User has not logged in.

Σε περίπτωση που δεν βρεθεί κάποια πτήση που να αντιστοιχεί στην αναζήτηση εμφανίζει ανάλογο μήνυμα: No flights found 

Σε περίπτωση επιτυχής εκτέλεσης εμφανίζεται το αποτέλεσμα της αναζήτησης.
#
## /display_flight_details_user
Για να κάνει εμφάνιση των στοιχείων πτήσης βάσει μοναδικού κωδικού θα στείλουμε: POST http://localhost:5000/display_flight_details_user

Η μορφή με την οποία πρέπει να δοθεί είναι η εξής:
```json
{
    "flight_id": "647d07741503b448d055b73c"
}
```
Σε περίπτωση που ο χρήστης δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: User has not logged in 

Σε περίπτωση που δοθεί λάθος το flight_id εμφανίζει το μήνυμα: Invalid flight ID

Σε περίπτωση που δεν βρεθεί η πτήση εμφανίζει: No flights found

Σε περίπτωση επιτυχής εκτέλεσης εμφανίζει τα στοιχεία της πτήσης
#
## /book_ticket
Για να κάνει κράτηση ένας χρήστης χρησιμοποιώντας το μοναδικό κωδικό της πτήσης θα στείλουμε: POST http://localhost:5000/book_ticket

Η μορφή με την οποία πρέπει να δοθεί είναι η εξής:
```json
{
  "flight_id": "647d07741503b448d055b73c",
  "name": "Manos",
  "surname": "Giannidis",
  "passport_number": "AR4322",
  "date_of_birth": "12-06-1999",
  "email": "giorgos@gmail.com",
  "ticket_class": "business"
}
```
Σε περίπτωση που ο χρήστης δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: User has not logged in

Σε περίπτωση που δοθεί λάθος το flight_id εμφανίζει το μήνυμα: Invalid flight ID

Σε περίπτωση που δεν βρεθεί η πτήση εμφανίζει: No flights found

Σε περίπτωση που to ticket_class είναι λανθασμένο εμφανίζει το μήνυμα : Invalid ticket class

Σε περίπτωση που έχουν τελειώσει τα διαθέσιμα economy εισιτήρια εμφανίζει το μήνυμα: No available economy tickets

Σε περίπτωση που έχουν τελειώσει τα διαθέσιμα business εισιτήρια εμφανίζει το μήνυμα: No available business tickets

Σε περίπτωση επιτυχής εκτέλεσης εμφανίζει: Ticket booked successfully

## /display_reservations_user
Για να εμφανίζονται οι κρατήσεις που έχει κάνει ο συγκεκριμένος χρήστης θα στείλουμε: GET http://localhost:5000/display_reservations_user

Σε περίπτωση που ο χρήστης δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: User has not logged in

Σε περίπτωση που ο χρήστης δεν έχει κρατήσεις εμφανίζεται το μήνυμα: User has no reservations

Σε περίπτωση επιτυχής εκτέλεσης εμφανίζει τις κρατήσης.
#
## /display_reservation_details
Για να κάνει ο χρήστης εμφάνιση στοιχείων κράτησης βάσει μοναδικού κωδικού κράτησης θα στείλουμε:
POST http://localhost:5000/display_reservation_details

Η μορφή με την οποία πρέπει να δοθεί είναι η εξής:
```json
{
  "reservation_id": "647d75dd7eac7541b23da4fc"
}
```
Σε περίπτωση που ο χρήστης δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: User has not logged in

Σε περίπτωση που δοθεί λάθος το reservation_id εμφανίζει το μήνυμα: Invalid Reservation id

Σε περίπτωση που ο χρήστης δεν έχει κρατήσεις η προσπαθεί να δει τα στοιχεία κάποιας άλλης κράτησης που δεν είναι δικιά του θα εμφανίζει: Reservation not found or this is not users reservation to view

Σε περίπτωση που δεν βρεθεί η πτήση εμφανίζει: No flights found

Σε περίπτωση επιτυχής εκτέλεσης εμφανίζει τα στοιχεία της κράτησης.
#
## /cancel_reservation
Για ακύρωση κράτησης βάσει μοναδικού κωδικού κράτησης θα στείλουμε: POST http://localhost:5000/cancel_reservation

Η μορφή με την οποία πρέπει να δοθεί είναι η εξής:
```json
{
  "reservation_id": "647d75dd7eac7541b23da4fc"
}
```
Σε περίπτωση που ο χρήστης δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: User has not logged in

Σε περίπτωση που δοθεί λάθος το reservation_id εμφανίζει το μήνυμα: Invalid Reservation id

Σε περίπτωση που ο χρήστης δεν έχει κρατήσεις η προσπαθεί να δει τα στοιχεία κάποιας άλλης κράτησης που δεν είναι δικιά του θα εμφανίζει: Reservation not found or this is not users reservation to cancel

Σε περίπτωση που δεν βρεθεί η πτήση εμφανίζει: No flights found

Σε περίπτωση επιτυχής εκτέλεσης εμφανίζει τo μήνυμα: Reservation canceled successfully
#

## /delete_account
Για διαγραφή του λογαριασμού του από την υπηρεσία θα στείλουμε: DELETE http://localhost:5000/delete_account

Σε περίπτωση που ο χρήστης δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: User has not logged in

Βρίσκει τον χρήστη που είναι συνδεδεμένος και τον διαγραφεί εμφανίζοντας το μήνυμα: Account deleted
#
## /login_admin
Για να κάνει είσοδο στο σύστημα ένας διαχειριστής θα στείλουμε: POST http://localhost:5000/login_admin

Η μορφή με την οποία πρέπει να δοθεί είναι η εξής:
```json
{
    "email":"user1@gmail.com",
    "password":"123"
}
```
Σε περίπτωση επιτυχής εκτέλεσης εμφανίζονται τα στοιχεία του διαχειριστή που έκανε login.

Αν τα στοιχεία του login είναι λάθος εμφανίζεται το μήνυμα: Wrong email or password.Please Enter Again.

Αν κάποιος διαχειριστής προσπαθεί να κάνει login ενώ είναι κάποιος άλλος διαχειριστής μέσα στην υπηρεσία  τότε εμφανίζει το μήνυμα: An admin is already logged in.

Αν κάποιος user προσπαθεί να κάνει login εμφανίζει το μήνυμα: User is Unauthorized to Login.

## /logout_admin
Για να κάνει έξοδο από το σύστημα ένας διαχειριστής θα στείλουμε: GET http://localhost:5000/logout_admin

Σε περίπτωση επιτυχής εκτέλεσης εμφανίζεται το μήνυμα: Logged out

Σε περίπτωση που ο διαχειριστής δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: Admin has not logged in
#
## /create_flight
Για να δημιουργήσει πτήση ένας διαχειριστής θα στείλουμε: POST http://localhost:5000/create_flight

Η μορφή με την οποία πρέπει να δοθεί είναι η εξής:
```json
{
"origin_airport": "Mykonos",
"destination_airport": "HER",
"date_of_flight": "23-06-2023",
"business_ticket": "100",
"business_cost": "300",
"economy_ticket": "200",
"economy_cost": "100"
}
```
Σε περίπτωση που ο διαχειριστής δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: Admin has not logged in

Σε περίπτωση επιτυχής εκτέλεσης εμφανίζεται το μήνυμα: Flight created
#
## /update_ticket_prices
Για να κάνει ανανέωση των τιμών ένας διαχειριστής θα στείλουμε: PUT http://localhost:5000/update_ticket_prices

Η μορφή με την οποία πρέπει να δοθεί είναι η εξής:
```json
{
  "flight_id": "647d07741503b448d055b73c",
  "business_cost": "200",
  "economy_cost": "100"
}
```
Σε περίπτωση που ο διαχειριστής δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: Admin has not logged in

Σε περίπτωση που δοθεί λάθος το flight_id εμφανίζει το μήνυμα: Invalid flight ID

Σε περίπτωση που δεν βρεθεί η πτήση εμφανίζει: Flight _id not found

Σε περίπτωση επιτυχής εκτέλεσης εμφανίζει: Ticket prices updated
#
## /delete_flight
Για να κάνει διαγραφή πτήσης βάση μοναδικοί κωδικού πτήσης ένας διαχειριστής θα στείλουμε: DELETE http://localhost:5000/delete_flight

Η μορφή με την οποία πρέπει να δοθεί είναι η εξής:  
```json
{
  "flight_id": "647d07741503b448d055b73c"
}
```
Σε περίπτωση που ο διαχειριστής δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: Admin has not logged in

Σε περίπτωση που δοθεί λάθος το flight_id εμφανίζει το μήνυμα: Invalid flight ID

Σε περίπτωση που δεν βρεθεί η πτήση εμφανίζει:Flight not found

Σε περίπτωση που θέλει να διαγράψει πτήση στην οποία υπάρχει κράτηση εμφανίζει: Cannot delete flight.Reservations exist.

Σε περίπτωση επιτυχής εκτέλεσης εμφανίζει: Flight deleted
#
## /flight_search_admin
Για να κάνει αναζήτηση πτήσεων ένας διαχειριστής θα στείλουμε: POST http://localhost:5000/flight_search_admin

Η μορφή με την οποία πρέπει να δοθεί είναι η εξής:
```json
{
    "origin_airport": "Athens",
    "destination_airport": "Thess",
    "date_of_flight": "13-05-2023"
}
```
```json
{
    "origin_airport": "Athens",
    "destination_airport": "Thess"
}
```
```json
{
    "date_of_flight": "13-05-2023"
}
```

Σε περίπτωση που δοθεί κενό το δεχόμαστε ώστε να εμφανίσουμε όλες τις διαθέσιμες πτήσεις

Σε περίπτωση που ο διαχειριστής δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: Admin has not logged in

Σε περίπτωση που δεν βρεθεί κάποια πτήση που να αντιστοιχεί στην αναζήτηση εμφανίζει ανάλογο μήνυμα: No flights found 

Σε περίπτωση επιτυχής εκτέλεσης εμφανίζει το αποτέλεσμα της αναζήτησης
#
## /display_flight_details_admin
Για να εμφανίσει τα στοιχεία πτήσης βάσει μοναδικού κωδικού πτήσης ένας διαχειριστής θα στείλουμε: POST http://localhost:5000/display_flight_details_admin

Η μορφή με την οποία πρέπει να δοθεί είναι η εξής:
```json
{
  "flight_id": "647d07741503b448d055b73c"
}
```
Σε περίπτωση που ο διαχειριστής δεν έχει κάνει πρώτα login εμφανίζεται το μήνυμα: Admin has not logged in

Σε περίπτωση που δοθεί λάθος το flight_id εμφανίζει το μήνυμα: Invalid flight ID

Σε περίπτωση που δεν βρεθεί η πτήση εμφανίζει:Flight not found

Σε περίπτωση που δεν βρεθεί η κράτηση εμφανίζει:Reservations not found

Σε περίπτωση επιτυχής εκτέλεσης εμφανίζει τα στοιχεία της πτήσης
