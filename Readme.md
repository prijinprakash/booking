## Initial Project setup
    git clone https://bitbucket.org/staykeepersdev/bookingengine.git
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py runserver


## Test Case example:

For covering more test cases we are going to need at least one hotel with 3 Hotel Room Types:

- First with price=50 (below max_price) with blocked day inside the search criteria for all rooms(could be 1 room)

- Second with price=60 (below max_price) with blocked day insde the search criteria for one out of few rooms

- Third with price 200 (above max_price) 


## Request example:

http://localhost:8000/api/v1/units/?check_in=2021-11-28&check_out=2021-12-01


## Response example:

    {
        "items": [
            {
                "listing_type": "Apartment",
                "title": "Luxurious Studio",
                "country": "UK",
                "city": "London",
                "price": "40"

            },
            {
                "listing_type": "Hotel",
                "title": "Hotel Lux 3***",
                "country": "BG",
                "city": "Sofia",
                "price": "60" # This the price of the first Hotel Room Type with a Room without blocked days in the range

            },
            {
                "listing_type": "Apartment",
                "title": "Excellent 2 Bed Apartment Near Tower Bridge",
                "country": "UK",
                "city": "London",
                "price": "90"
            },
        ]
    }
