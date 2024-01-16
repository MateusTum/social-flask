# SECRET_KEY: A secret key used for securing the Flask application. 
# It is crucial for session security, form protection, and other cryptographic purposes.
# Please ensure this key is kept confidential and is unique for each Flask application.
SECRET_KEY = 'bacon'

# DATABASE_URI: The Uniform Resource Identifier (URI) for the SQLite database used by the Flask application.
# In this case, it points to a local SQLite database file named 'site.db'.
DATABASE_URI = 'sqlite:///site.db'

# DEBUG: A boolean flag indicating whether the Flask application is in debug mode.
# Debug mode provides additional information about errors and enables auto-reloading of the server on code changes.
DEBUG = True

# HOST: The network interface on which the Flask development server will listen.
# '0.0.0.0' means the server will be accessible from any IP address, making it suitable for development environments.
HOST = "127.0.0.1"

# ROWS_PER_PAGE: Number of posts loaded on feed
ROWS_PER_PAGE = 10
