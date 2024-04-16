---
date: 2024-04-16T09:40:06.581801
author: AutoGPT <info@agpt.co>
---

# aarushi-geo-location-1

Based on the interview, the user requires an API endpoint designed with FastAPI that handles geolocation data retrieval based on IP addresses. The following key points were highlighted during the discussions:

- The API should be asynchronous (async) to ensure scalability and handle the anticipated volume of up to 1000 requests per second. This aids in maintaining an efficient and responsive service.
- Specific data to be retrieved from the geolocation database includes the country, city, latitude, longitude, and, ideally, the Internet Service Provider (ISP) information. These data points are essential for location-based services, content personalization, technical analytics, and assessing access rights.
- Performance goals are set to achieve response times of less than 200 milliseconds, thereby ensuring a smooth user experience without noticeable delays.
- The need to support bulk IP address queries was also emphasized. This feature will significantly lower the number of requests sent by clients requiring data for multiple IP addresses simultaneously, thus enhancing the overall performance.

To address these requirements, the following technical stack components were identified as suitable choices:
- **Programming Language:** Python, for its simplicity and asynchronous capabilities.
- **API Framework:** FastAPI, noted for its ease of use for creating asynchronous APIs, built-in OpenAPI support for comprehensive documentation, and its dependency injection system which contributes to cleaner, more maintainable code.
- **Database:** PostgreSQL, due to its robustness and the capability to store and efficiently query geolocation data. Specific aspects such as using IP network data types (INET or CIDR) for accurate IP range queries and creating indexes on IP address columns for performance optimization were recommended.
- **ORM:** Prisma, while it doesn't natively support PostgreSQL's geolocation data types such as 'point', can still be utilized by employing raw SQL queries or mapping these specific data types to string or binary fields and manually handling them within the application logic.

In terms of design and development best practices, the project will leverage asynchronous request handling, implement authentication and data validation (utilizing Pydantic models), and consider scalability from the outset to effectively manage the expected load. The database setup will include importing a suitable geolocation database into PostgreSQL, with regular updates to ensure data accuracy.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'aarushi-geo-location-1'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
