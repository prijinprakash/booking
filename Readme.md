## Summary:

1. This is a simple booking application for **Hotels (multiple units)** and **Apartments (single unit)**
    - **Listing** table allows to add hotels and apartments
    - **BookingInfo** table carries information about pricing of apartments and different types of hotel rooms (single room, double room etc...)
    - **HotelRoom** table keeps track of different hotel rooms in each hotel room type (booking info of hotels). Minimum one room must be
    present in each hotel room type for reservation
    - **Reservation** table carries information about reservations in different date ranges.

2. There is a pre-build structure for Hotels/Apartments. Database is prefilled with information - **db.sqlite3**.
    - superuser
        - username: **admin**
        - password: **admin**

3. **endpoint** where we will get available Apartments and Hotels based on:
    - **available days** (date range ex.: "from 2021-12-09 to 2021-12-12")
        - Apartment should not have any blocked day inside the range
        - Hotel should have at least 1 Hotel Room available from any of the HotelRoomTypes (booking info of hotels)
    - **max_price** (100):
        - Apartment price must be lower than max_price.
        - Hotel should have at least 1 Hotel Room without any blocked days in the range with price lower than max_price.

    - returned objects are **sorted** from lowest to highest price.

## Initial Project setup
    git clone https://github.com/prijinprakash/booking.git
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd booking
    python manage.py runserver


## Test Case example:

For covering more test cases we are going to need at least one hotel with 3 Hotel Room Types:

- First with price=50 (below max_price) with blocked day inside the search criteria for all rooms(could be 1 room)

- Second with price=60 (below max_price) with blocked day insde the search criteria for one out of few rooms

- Third with price 200 (above max_price) 


## Request example:

http://localhost:8000/api/v1/units/?max_price=100&check_in=2021-11-28&check_out=2021-12-01


## Response example:

    {
        "items": [
            {
                "listing_type": "Apartment",
                "title": "Luxurious Studio",
                "country": "UK",
                "city": "London",
                "price": "40.00"
            },
            {
                "listing_type": "Hotel",
                "title": "Hotel Lux 5***",
                "country": "UK",
                "city": "London",
                "price": "60.00"
            },
            {
                "listing_type": "Apartment",
                "title": "Excellent 2 Bed Apartment Near Tower Bridge",
                "country": "UK",
                "city": "London",
                "price": "90.00"
            }
        ]
    }
