# Voting-Management

It's an assignment for some company. They wanted to me to make elasticsearch work with python django with this assignment.

There are two types of user 'admin' and 'registered user'

Registered users can take the poll or voting while admin can also take poll, but in addition can see the results of all the voting till now as well as new questions to the poll.

No user can vote more than once on the same poll.

All the user can registered themselves from web app.

While for creating the admin, one has to create it using the following command

'python manage.py createsuperuser' from the root directory of the project.

It will ask Username, email and password.

Once superuser is created, superuser can also login from the webapp and extra options will be visible to the superuser / admin.
