URL Shortener Service:
    A simple and efficient URL shortener service that allows users to shorten long URLs, customize their short links, and track access analytics.

#Features:
    Shorten long URLs.
    Optional custom slugs for shortened URLs.
    Expiration dates for URLs.
    Access analytics to track how many times a URL has been accessed.
    Rate limiting to prevent abuse.
    Basic security measures including input validation.

#Setup and Execution Steps:
    Create a Virtual Environment:
    python -m venv venv
    source `venv/bin/activate`  # On Windows use `venv\Scripts\activate`

    Install Requirements:
    pip install -r requirements.txt

    Apply Database Migrations:
    python manage.py migrate

    Create a Superuser (Optional):
    python manage.py createsuperuser

    Run the Development Server:
    python manage.py runserver


#Design Decisions and Trade-offs:
    URL Shortening Algorithm:
    I opted for a randomized short ID generation method, ensuring unique short links. This approach is simple but can lead to collisions, hence the uniqueness check before saving to the database.

    Custom Slugs:
    Allowed users to specify custom slugs, adding flexibility to the service. However, this required additional validation to ensure that custom slugs are unique.

    Expiration Feature:
    Implemented an expiration feature for links, which helps in cleaning up the database and reducing clutter. The trade-off is the complexity added to the URL management logic.

    Security Measures:
    Basic input validation is included to prevent SQL injection and XSS attacks. However, more advanced security measures (like OAuth) could be implemented for enhanced protection but would add complexity.

#Deviations from Original Requirements:
    Custom Slug Feature: This feature was not part of the original requirements but was added to enhance user experience by allowing users to create memorable short URLs.

    Rate Limiting: Originally, the plan did not include rate limiting, but it was added to prevent abuse and protect against denial-of-service attacks.

#Additional Features:
    Analytics: Added a feature to track how many times a shortened URL has been accessed, allowing users to see the performance of their links.

    Admin Panel: Integrated the Django admin panel for easy management of shortened URLs, enabling admins to view and delete links.

#Technologies Used:
    Python
    Django
    Django REST Framework
    SQLite 
    Redis (for caching and rate limiting)

#Testing Instructions:
    You can test the API endpoints using tools like Postman.

    Here are the endpoints to test, including the request types, headers, and body formats.

    a. Shorten URL
        Endpoint: POST /url/shorten
        Description: Shorten a long URL with an optional custom slug.

        {
          "original_url": "https://www.example.com",
          "custom_slug": "customslug",   // Optional
          "expires_in_days": 30           // Optional
        }


    b. Redirect URL
        Endpoint: GET /r/<short_id>
        Description: Redirect to the original URL using a short ID or custom slug.
        URL Parameters:
        short_id: The short ID or custom slug you received when creating the URL


    c. URL Analytics
        Endpoint: GET /analytics/<short_id>
        Description: Get analytics for a specific short URL.
        URL Parameters:
        short_id: The short ID or custom slug you received when creating the URL.