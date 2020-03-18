# EarnUp Technical Solution

Hi team @ EarnUp - I am thrilled and grateful for the opportunity you have
afforded me with this technical challenge. 

# Runtime Instructions
So there are a few things to keep in mind when running this. First off it is
intended to be run with python 3.6.5+. If you don't have python 3.6.5 (as I
believe mac native is 2.7 still) I recommend pyenv.
1. `brew install pyenv`
1. `pyenv init`
1. `pyenv install 3.6.5`
1. `pyenv local 3.6.5`

This should set your local folders python version to 3.6.5. See these docs if
needed: https://github.com/pyenv/pyenv#homebrew-on-macos

Then you should install poetry with this command:
`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`

and add poetry to your path with `export PATH="$HOME/.poetry/bin:$PATH"`. Then
when you are inside of this github repository you should be able to install the
dependencies with `poetry install`. This will create the environment for you
and handle package dependencies. Run `poetry shell` next, as this is required
before accessing any of the django management commands.

You will next have to create the database as this cannot be checked into the
repository. I have provided a slightly altered CSV. The alterations from the
original CSV were performed by the `csv_cleaner.py` script if you want to see
what was done there.

First you must run `python manage.py migrate` to run the initial schema
migrations for the sqlite3 database. Then you can run `python manage.py
create_database` to create the rental agreements in the database. Once this has
been done you next run `python manage.py runserver` and visit
`localhost:8000/api/rentals/` to see a listview of the rentals database table.
This is the endpoint that you can run pass parameters to in order to search the
rentals database.
