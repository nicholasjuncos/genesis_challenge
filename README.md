# Genesis Challenge

Code response for Genesis Research.

## Structure

Settings are located in config/settings/ folder. `base.py` contains most generic settings. `local.py` is for development
 and `production.py` is for an actual production website. THIS PROJECT DEFAULTS TO `local.py`! Create a .env file and 
 place in project root directory with settings to configure for production! Make sure you have `ENVIRONMENT=production` 
 if using for production website! See details below. This .env is configured through the use of the library 
[python-decouple](https://pypi.org/project/python-decouple/).

## Installation

Ensure you have installed python 3.8

`git clone https://github.com/nicholasjuncos/genesis_challenge.git`

Then open with project with Pycharm or your selected IDE.

**FOR PRODUCTION ONLY**: Copy and paste your "**.env**" file to this Project's Root Folder. See .env_example for details

### Create Environment

#### Create Environment through Terminal or Pycharm

##### Create in Terminal

First, cd into the project root directory, then run these commands (locations of project and environments vary by your 
preferences):

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

In Pycharm, open **Preferences**>**Project:genesis_challenge**>**Project:Interpreter**. Select the gear, and 
**Add Environment**.

Select **Existing Environment** and direct to the location of the python3 file in the created environment 
(e.g. **~/Documents/genesis_challenge/venv/bin/python3**)


##### Create in Pycharm
1. Open **Preferences**>**Project:genesis_challenge**>**Project:Interpreter**. Select the gear, and **Add Environment**.
2. Set location to destination of your environments folder with the environment name 
(e.g.: **~/Documents/genesis_challenge/venv**)
3. Set "**Base Interpreter**" to your Python3 library in your **/usr/local/bin/** folder.
4. Upgrade Pip and setuptools if necessary.
5. Open Pycharm Terminal (ensure the venv is activated and you are located in project root directory), 
then run `pip install -r requirements.txt`

#### Finalizing Pycharm Setup after environment creation
1. Open **Preferences**>**Languages/Frameworks**>**Django** and set the settings value to "**config/settings/local.py**"
2. At top-right of Pycharm, select "**Add Configuration**". Select the **+** and select "**Django Server**". Create 
with any preferences you have.


### Final Steps
ENSURE THAT YOU ARE IN YOUR ACTIVATED ENVIRONMENT `source ./venv/bin/activate`

Run `python manage.py migrate` in the terminal.

Runserver with the Pycharm run configuration, or `python manage.py runserver`

## Extra Functionality

### Mailhog

Mailhog is used for the sending and receiving of emails in dev environment. Simply install online and input `mailhog` 
in a terminal to activate. You can see the emails sent and received at http://0.0.0.0:8025. For developoment purposes.

### Sentry
[Sentry](https://sentry.io/) logging is recommended for production.

### Django-Storages
[django-storages](https://django-storages.readthedocs.io/en/latest/) is recommended for interacting with AWS, GCP, 
etc.

## Testing and playing with API
### Playing with API
Activate your local environment and run `python manage.py createsuperuser` and input data to access the admin page.

Navigate to [127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) to login with superuser info and interact directly 
with django **MUST CREATE SUPERUSER FIRST**.

For Authentication API purposes, 
[http://127.0.0.1:8000/dj-rest-auth/registration/](http://127.0.0.1:8000/dj-rest-auth/registration/) to register, 
[http://127.0.0.1:8000/dj-rest-auth/login/](http://127.0.0.1:8000/dj-rest-auth/login/) for login, and 
[http://127.0.0.1:8000/dj-rest-auth/login/](http://127.0.0.1:8000/dj-rest-auth/logout/) for logout. 
After retrieving a login token from dj-rest-auth, add it as an **Authorization** Header as such: `Token LOGIN_TOKEN`.
You can also go to [http://127.0.0.1:8000/dj-rest-auth/](http://127.0.0.1:8000/dj-rest-auth/) to see other url options 
in the debug message of the 404 page.

To interact with the custom API features, navigate to [http://127.0.0.1:8000/api](http://127.0.0.1:8000/api/). 
Superusers will have more ability for interacting with the users and articles.

### Testing
Simply navigate to your project root directory, activate your local environment, and run `python manage.py test`
