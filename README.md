### Allica Bank Technical Test - Luke Barrett

Question:
* Create a REST API project in Python
* Expose a HTTP method to post Customer details—First Name, Last Name and Date Of Birth 
* Save the details
* Create another HTTP method to retrieve the customer details.

**Design Decisions**

Due to the time available to complete this project, I have made several design decisions I wouldn't
normally make when building a production-ready application.

- Database Choice: SQLite was chosen as the local database solution due to its simplicity and 
ease of integration for local 'PoC' development. If this application was to be used in a production
environment, I'd typically use a most robust database like PostgresSQL, and set this up using Terraform,
and manage schema changes using something like Alembic.

- Application Choice: I have used FastAPI for the application layer, due to its simplicity and speed of development.

**Running the Application**

Install Dependencies: `poetry install`

Run the Handler: `poetry run python app.py`

This will execute the FastAPI application, allowing users to POST to the RPC-style application.

POST - /users/
```json 
{
  "first_name": "Luke",
  "last_name": "Barrett",
  "date_of_birth": "1998-06-12"
}
```
The above request will insert a user into the local SQLite database.

The GET endpoint allows a user to filter the application results based off the provided filter. The user can provide 
generic first name filtering like so:
GET - `/users?first_name="Luke Barrett`

Additionally, the user can specify additional parameters for better response filtering
GET - `/users?first_name="Luke Barrett&last_name="Barrett"&date_of_birth="1998-06-12"`

**Testing Strategy**

- **Unit Test:** The unit-tests have been kept super simple for this application, since we are using SQLite, we can 
spin up a temporary database for the scope of the testing suite. Normally, if this was a production level 
application, I would spin up a docker container with a PostgresSQL database, and
use that for the scope of the unit-testing and tear it down afterwards.

- **Integration Test:** If this was a production application, I would implement some integration tests, 
ensuring the database is providing the correct response once it has been deployed.

- **E2E Tests** I would also normally include additional end-to-end tests, to ensure the full flow of the application
is working as expected once it has been deployed, but that isn't necesary for a PoC application of this size.

# Production Considerations

If this application was to be deployed to a production environment, I'd consider the following improvements:

- **Database:** Replace SQLite with PostgresSQL, or another cloud-based database designed to handler higher loads.

- **User Authentication/RBAC** Ensure the Application is ensure, and has good Role-Based Access Control, 
non-administrator users should **not** be able to view sensitive data, or append new Users to the database 
without permission.

- **IaC:** Use Terraform to manage infrastructure, including the DB setup, env configuration and deployment pipelines.

- **CI/CD:** Set up a CI/CD pipeline to automate linting, testing, building, and deployment.


# Future Work

- The Database implementation for this application is super simple if this application was going to production, I would
add some integrated transaction management and ensure all database transactions are ATOMIC to avoid deadlocks. My normal
 preferred architecture for an application like this would be Domain-Driven design, with the User being the Domain 
Aggregate for this application. I'd also manage Database transactions via a unit-of-work, and ensure the database 
is locked whilst a transaction is taking place.

- Improved Testing: Add some load testing and additional edge-case handling to ensure the application is capable of
handling various scenarios in production.

- Environment Management: Implement environment level configurations and secret management for secure deployment.

- Authentication: Any non-PoC application should **always** include user authentication, my preferred choice for
authentication, and RBAC is OAuth.
