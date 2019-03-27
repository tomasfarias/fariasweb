# Fariasweb

My personal webpage/blog in Flask. Check it out tomasfarias.com

## Getting started

Clone the repo:

```
git clone https://github.com/tomasfarias/fariasweb.git
```
 
Install the requirements:

```
pip install -r requirements.txt
``` 

Like all Flask apps, set the `FLASK_APP` and `FLASK_ENV` environment variables.

In Windows:
```
set FLASK_APP=fariasweb.py
set FLASK_ENV=development
```

In bash:
```
export FLASK_APP=fariasweb.py
export FLAS_ENV=development
```

Only the first time, you will need to run the database migrations:

```
flask db upgrade
```

Finally, run your own Flask development server!

```
flask run
```


### Prerequisites

The project is written in Python 3.7.2 although the code should work with any >= 3.6 version (I really like f-strings!).

## Running the tests

All testing is done with pytest and currently contained in a single file. Run them with:

```
pytest app/tests/
```

While the tests pass, currently there's a lot of deprecation warnings being raised by some of the Flask extensions used.

## Authors

* **Tomás Farías** - *Hey! My name is in the title!* [tomasfarias](https://github.com/tomasfarias)

## Acknowledgments

This project started thanks to the amazing [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by [Miguel Grinberg](https://github.com/miguelgrinberg). If you're interested in getting into Flask I strongly recommend going over at least the first ten parts.
