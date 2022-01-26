# Implement User Notifications In Flask

This is continuation of improving a user's experience within a flask chat application. Previously, in the [flask popover project](https://github.com/GitauHarrison/flask-popovers), we implemented the popover component when a mouse hovers over a user's name. Here, we go further and add private messaging features. Every time a user receives a message, we want the application to notify the recipient that indeed there is a new message in the inbox. The recipient does not have to do anything to see the notifications since the application can automatically display them when they come.

![Notifications](/app/static/images/notifications.gif)

## Features

- User notifications
- Private messaging

## Tools Used

- Flask
- Python
- JQuery
- Ajax

## Testing the Deployed Application

- [Application on heroku](https://user-notifications.herokuapp.com/)

You can test notifications on the deployed application by logging in to an already existing account.

User 1:
 - Username: harry
 - Password: 12345678

User 2:
 - Username: gitau
 - Password: 12345678

 Alternatively, you can create your own user. Link on the [registration link](https://user-notifications.herokuapp.com/register). You will be redirected to the [login page](https://user-notifications.herokuapp.com/login) after a successful registration.

## Testing The Application On Your Local Machine

1. Clone this repository:
    ```python
    $ git clone git@github.com:GitauHarrison/user-notifications-in-flask.git
    ```
<br>

2. Navigate to the `user-notifications-in-flask` directory:
    ```python
    $ cd user-notifications-in-flask
    ```
<br>

3. Create and activate a virtual environment:
    ```python
    $ virtualenv venv
    $ source venv/bin/activate

    # Alternatively, you can use virtualenvwrapper
    $ mkvirtualenv venv
    ```
    - Virtualenvwrapper is a wrapper around virtualenv that makes it easier to use virtualenvs. mkvirtualenv not only creates but also activates a virtual enviroment for you. Learn more about virtualenvwrapper [here](https://github.com/GitauHarrison/notes/blob/master/virtualenvwrapper_setup.md).
<br>

4. Install dependencies:
    ```python
    (venv)$ pip3 install -r requirements.txt
    ```
<br>

5. Add environment variables needed to run the application:
    ```python
    (venv)$ cp .env.example .env
    ```
    - You can get a random value for your `SECRET_KEY` by running `python -c "import os; print os.urandom(24)"` in your terminal.
<br>

6. Run the application:
    ```python
    (venv)$ flask run
    ```
    * Ensure that you are in the root directory of the project before running this command.
<br>

7. Open the application on two windows in your favorite browser by copying and pasting the link below in the URL bar:
    
    - http://localhost:5000
    - You should see the application running.
<br>

8. Feel to create two users of your own. Simply [register](http://localhost:5000/register) them and then [login](http://localhost:5000/login).
<br>

9. On one browser window, hover your mouse over a user's name. If the target user is not the current user, then you will see a _send private message_ link. Click on the link to send a private message to the target user.
<br>

10. On the other browser window, you should see a notification that the target user has received a new message. You can click on the notification to view the message.
<br>

11. Repeat the same process for the other user.

## HowTo

