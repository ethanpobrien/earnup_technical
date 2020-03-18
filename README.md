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
before accessing any of the django management commands. See the poetry docs if
needed as well: https://python-poetry.org/docs/#installation

You will next have to create the database as this cannot be checked into the
repository. I have provided a slightly altered CSV. The alterations from the
original CSV were performed by the `csv_cleaner.py` script if you want to see
what was done there.

First you must run `python manage.py migrate` to run the initial schema
migrations for the sqlite3 database. Then you can run `python manage.py
create_database --filename=cleaned_file.csv` to create the rental agreements in the database. Once this has
been done you next run `python manage.py runserver` and visit
`localhost:8000/api/rentals/` to see a listview of the rentals database table.
This is the endpoint that you can run pass parameters to in order to search the
rentals database.

There is no authentication for this endpoint as I figured it would be simpler
to expose it publicly instead of having you set up a user account just for an
API request locally. However I would definitely set up the authentication class
necessary to restrict this endpoint to authenticated users only, if this were a
true app and not a more PoC type app.

Examples are such links as:

http://localhost:8000/api/rentals/?latitude=40.73494&longitude=-73.9503&distance=40

http://localhost:8000/api/rentals/?query=near+the+empire+state+building


# How this works
There are a few main components for how this works. The first is in the data
ingestion. When creating the rental rows in the database, a new column is
created which contains the bedroom count for the rentals. This is done by
guessing based on a set of keywords that are translated into a numeral from the
rental description. The same extraction logic is applied to the query string in
the query parameters. If a bedroom count is found in the query string then the
search results are filtered on this requirement.

Similar logic is applied to finding landmarks in the query string. I think
there are a number of other ways this type of data cleaning at the data
ingestion step combined with query cleaning at the request step can help refine
the search results.

I think for the search string matching, there are two main types of
descriptions - those pertaining to the rental location and those pertaining to
the rental interior, which is why I chose landmarks and room counts as the two
parts of search string matching that I would tackle.

Then for location information, a basic bounding box is drawn based upon the
original search parameters. However if this bounding box does not result in any
query results, the bounding box is expanded past the request distance in the
interest of surfacing at least some results.

If no query parameters are entered then all the rentals are returned and if
there are both location and search query parameters present the combination of
both sets are returned (not the intersection of the sets).

These trade-offs always err on the side of returning more results rather than
fewer results. I think there are many more in depth search optimizations that I
could be doing as well, as there are a high number of columns that I do not
search at the moment. I think the burroughs and neighborhoods of New York could
be cached in a similar manner to the landmarks, so that if they were detected
in a string the search space could be restricted to the burrough mentioned.

Another note on the way this functions. I am doing a slightly odd search, as I
search through the CSV and pull the ID from the CSV when matches are found, and
then return database objects when finalizing the response. I took this liberty
as I figured for this size of an app this is a feasible way to search, and
allowed me to reuse some starter code from a test script I drafted earlier in
the solving of this problem. I want to acknowledge the lack of scalability of
this solution, as efficient SQL queries would far outpace this system at scale.
