## Local Library Web Application
Hi! The project is under the [master branch](https://github.com/deusbalatro/locallibrary/tree/master)

This project is created for learning purposes and serves as a simple dynamic web application for an imaginary local library. Built using Django, it focuses on back-end and database logic, with minimal emphasis on front-end styling.

### Features:
- Authentication system based on Django's framework.
- Staff members can perform CRUD operations on books, authors, and copies, as well as modify return dates of books.
- Users and staff members have different access levels and corresponding pages.
- Users can view the availability status of books in the library, helping them decide whether to borrow a book.
- Users have the ability to view a list of books they have borrowed.
- Staff members have access to a comprehensive list of borrowed books, including those borrowed by other members, in addition to being able to view the books they have borrowed themselves.
- And the other features such as detailed author information, providing users with comprehensive details about each author, as well as book details.

### Technology Stack:
- Django
- PostgreSQL (Development database)
- SQLite (Included in the repository)

### Screenshots:
Check out screenshots of the web application [here](https://github.com/deusbalatro/locallibrary/tree/master/screenshots).

### If you would like to run it on your computer:
1. [Install Python and Django on your system](https://docs.djangoproject.com/en/5.0/topics/install/).
2. [Download the Local Library project from the master branch](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives).
3. Open your terminal.
4. Navigate to the project directory.
5. Run the following commands in order:

   - `
   py manage.py migrate
   `
   - `
   py manage.py runserver
   `

   These commands will create a database and start the development server, and you can access the web application in your browser at `http://127.0.0.1:8000/`.


Bye!
