# Simple Flask Website

A simple website with SQLite database powered by Python and Flask framework.

## Development

### Environment

Create virtual environment for the project with Python 3.

Example using virtualenvwrapper:

```
mkvirtualenv -p python3 myenv
workon myenv
```

Install project requirements inside your virtual environment:

```
pip install -r requirements.txt
```

### Create instance config

Create `instance` folder in project root and `config.py` file in it for your instance config.

For example:

```
SITE_NAME="Simple Flask Website"
SECRET_KEY="MyVerySecretKey"
```

Note: Public environment variables are stored in `.flaskenv` file.


### Run the app

Run the application with:

```
flask run
```

Access the application by visiting `http://localhost:5000` in your browser.
