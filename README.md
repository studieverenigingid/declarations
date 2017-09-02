Declarations system Study association i.d
==================

## Backend
To set up the backend:

3. Run `virtualenv venv`
4. Activate the virtualenv: `. venv/bin/activate` (Windows: `venv\scripts\activate`)
5. Run `pip install -r ./requirements.txt` to install all depencencies

To run it: `python run.py`

## Frontend
To set up the frontend (angular + backbone and more, `node` and `npm` are assumed to be installed already)

1. Change to directory frontend: `cd frontend`
2. Install gulp: `npm install -g gulp` (run with `sudo` if there are permission problems)
3. Install all dependencies `npm install` and get yourself some coffee, this’ll take way too long because *npm* :(
4. Run `cp src/js/config.js.sample src/js/config.js` to make a working copy of the config
5. To test only the frontend without backend (why though?) run `gulp` and go to `127.0.0.1:5001`; to just make sure there is a frontend for Flask to show, change the IP address in `src/js/config.js` to the one where Flask will serve and then run `gulp build`
6. ...
7. profit?
8. Pray they don’t change the requirements
