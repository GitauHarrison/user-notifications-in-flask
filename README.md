# Implement User Notifications In Flask

This is continuation of improving a user's experience within a flask chat application. Previously, in the [flask popover project](https://github.com/GitauHarrison/flask-popovers), you can see how to implement the popover component when a mouse hovers over a user's name. This project builds on that feature and adds private messaging. Every time a user receives a message, we want the application to notify the recipient that indeed there is a new message in the inbox. The recipient does not have to do anything to see the notifications since the application can automatically display them (notification, not message) when they come.

![Notifications](/app/static/images/notifications.gif)

## Features

- User notifications
- Private messaging

## Tools Used

- Flask
- Python
- JQuery
- Ajax

## Contributors

[![GitHub Contributors](https://img.shields.io/github/contributors/GitauHarrison/flask-popovers)](https://github.com/GitauHarrison/user-notifications-in-flask/graphs/contributors)


## Testing the Deployed Application

- [Application on heroku](https://user-notifications.herokuapp.com/)

You can test notifications on the deployed application by logging in to an already existing account.

User 1:
 - Username: harry
 - Password: 12345678

User 2:
 - Username: gitau
 - Password: 12345678

 Alternatively, you can create your own user. Click on the [registration link](https://user-notifications.herokuapp.com/register). You will be redirected to the [login page](https://user-notifications.herokuapp.com/login) after a successful registration.

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

8. Feel free to create two users of your own. Simply [register](http://localhost:5000/register) them and then [login](http://localhost:5000/login).
<br>

9. On one browser window, hover your mouse over a user's name. If the target user is not the current user, then you will see a _send private message_ link. Click on the link to send a private message to the target user.
<br>

10. On the other browser window, you should see a notification that the target user has received a new message. You can click on the notification to view the message.
<br>

11. Repeat the same process for the other user.

## HowTo

### Create Messages Model

Create a `Message` table in the database to store a user's messages.

```python
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'Message: {self.body}'

# Remember to define the relationship between the `Message` and `User` models.
```
The interesting thing with this table is that we define two foreign keys, one for the sender and another for the recipient, both of whom are users. This relationship is defined in the `User` table.


### Count Number of Unread Messages

Count the number of messages a user has received since he read his messages last:

```python
class User(UserMixin, db.Model):
    # ...
    last_message_read_time = db.Column(db.DateTime)

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()
```
This helper method uses the last time a user visited the messages page to determine which messages are new. It returns the number of messages that have been recieved by a user.


### Update Messages Model
Store the messages in the database:

```python
@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(
            author=current_user,
            recipient=user,
            body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('user', username=recipient))
    return render_template(
        'send_message.html',
        title='Send Message',
        form=form,
        recipient=recipient)
```
In the `User` model, we defined `author` and `recipient` as foreign keys. We use these keys to update the `Message` model.

### View Messages

To view one's private messages, we need to render a page that shows all the received messages.

```python
@app.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('message', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template(
        'messages.html',
        messages=messages.items,
        next_url=next_url,
        prev_url=prev_url)
```

In the `messages.html` template, we can loop through `messages`:

```python
{% for post in messages %}
    {% include '_post.html' %}
{% endofr %}
```

### Notification Badge

To tell a user that there are new unread messages, we can add a badge in the navigation bar.

```html
<li>
    <a href="{{ url_for('messages') }}">
        Messages
        {% set new_messages = current_user.new_messages() %}
        {% if new_messages %}
            <span class="badge">{{ new_messages }}</span>
        {% endif %}
    </a>
</li>
```
A user will need to click on any link for the badge to update the number of unread messages.

### Message Notification

A notification will be linked to a user. Hence, we need to create a `Notification` model and link it to the user.

```python
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))
```
The data stored in this table will be a JSON list of messages. When a new message comes in, say a user's badge was 1, then the badge will be updated to 2. The name of the previous notification needs to be deleted first, then the new update applied.

```python
class User(UserMixin, db.Model):
    # ...

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n
```

### Update Message Counts

The two places in the application that will need to be updated so the notication is accurate are:
 - when sending messages (URL: `/send_message/<recipient>`)
 
    ```python
    def send_message(recipient):
        # ...

        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
    ```

 - when viewing messages (URL: `/messages`)
     
    ```python
     def messages():
        # ...
        current_user.last_message_read_time = datetime.utcnow()
        current_user.add_notification('unread_message_count', 0)
        db.session.commit()
    ```

### Retrieve Notifcations

```python
@app.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
```

Clients can only request messages since a given time. This is to prevent them from getting duplicate messages.

### Dynamic Notification Badges

To improve a user's experience, the application can poll for new messages and update the badge count dynamically. Using JQuery, we can execute a function when a page loads. Ajaxs allows us to send asynchronous reequest to the server.

```js
{% if current_user.is_authenticated %}
        $(function() {
            var since = 0;
            setInterval(function() {
                $.ajax('{{ url_for('main.notifications') }}?since=' + since).done(
                    function(notifications) {
                        for (var i = 0; i < notifications.length; i++) {
                            if (notifications[i].name == 'unread_message_count')
                                set_message_count(notifications[i].data);
                            since = notifications[i].timestamp;
                        }
                    }
                );
            }, 1000);
        });
{% endif %}
```
`setInterval` works similarly to `setTimeout`, except that it will execute the function repeatedly, with a fixed time delay between each execution.