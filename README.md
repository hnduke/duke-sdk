# The One API Python SDK

## Installation

To install the SDK:

1. Create and activate a venv
```
$ mkdir venv
$ python3.10 -m venv venv
$ source venv/bin/activate
```
2. Install the package from PyPi
```
(venv) $ pip install the_one_api_sdk_duke
```

## User Guide

1. If you haven't done so, create an account at [The One API](https://the-one-api.dev/sign-up)
2. Use your access token to authenticate:
```
>>> import the_one_api
>>> the_one_api.api_key = "your-access-token-here"
```

### Endpoints

#### Movie Endpoint

Import the Movie module:
```
>>> from the_one_api import movie
```
Quotes can be listed in full, fetched by ID, or searched using a variety of filters
```
>>> movie.list_all()
>>> movie.get('quote-id')
>>> movie.filter(**filters)
```

#### Quote Endpoint

Import the Quote module:
```
>>> from the_one_api import quote
```
Quotes can be listed in full, fetched by ID, or searched using a variety of filters,
including by movie ID.
```
>>> quote.list_all()
>>> quote.get('quote-id')
>>> quote.filter(movie_id="movie-id", match={"character": "character-id"})  # etc.
```

#### About Sorts and Filters

The `filter` functionality accepts a sort keyword argument and a variety of filters

##### Sort
Supply a field to sort by, and prepend a "-" for a descending sort. Only one field at
a time is supported.
```
>>> movie.filter(sort="name")
>>> quote.filter(sort="-character")
```

##### Match/Negate Match
Supply a dictionary containing a field and value for an exact match (or to not match).
Only one term per match is supported.
```
>>> movie.filter(match={"name": "The Lord of the Rings Series")
>>> movie.filter(negate_match={"name": "The Lord of the Rings Series")
```

##### Filter/Exclude
Supply a dictionary containing a field and a list of values to match (or not match).
```
>>> movie.filter(filter={"name": ["The Return of the King", "The Fellowship of the Ring"]})
>>> movie.filter(exclude={"name": ["The Return of the King", "The Fellowship of the Ring"]})
```

##### Regex/Negate Regex
Supply a MongoDB-style regex pattern to include or not. See the
[MongoDB documentation](https://www.mongodb.com/docs/manual/reference/operator/query/regex/)
for details.
```
>>> quote.filter(regex={"dialog": "/foot/i"})
>>> quote.filter(negate_regex={"dialog": "/foot/i"})
```

##### Less Than, Greater Than, and Greater Than or Equal To
Supply a dictionary containing a field and a number or character.
```
>>> movie.filter(gte={"budgetInMillions": 600}, lt={"budgetInMillions": 400})
>>> quote.filter(lt={"dialog": "B"})
```

## Developer Guide

### Installation

1. Clone the project from GitHub
2. Create a venv and activate it
3. Install the requirements and the project itself in editable mode:
```
(venv) $ pip install -r requirements.txt -r requirements-dev.txt
(venv) $ pip install -e .
```

### Running the test suite

Once the project has been installed following the Developer Guide:

1. Install "requirements-test.txt"
2. Run the tests:
```
(venv) $ python -m pytest
```
