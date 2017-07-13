# MycroBlog
An end-to-end blog web application using Python and Flask.

## Functional Use Cases

- User can register into the database.
No repetitions are allowed in both user name and email address.
- User can log into the index page.
Only upon logging into the system, the user will be able to access index.
- User can see other user's posts.
- User can see their own posts in the user page.
- User can display an "about me" section and edit it.
- User can log out from any page when logged in.

## Test cases

As the application grows in size it gets more and more difficult to ensure code changes don't break functionality.

Each test described in tests.py runs a focused part of the project and verifies that the result obtained is the expected one.
When the test coverage is large, modifications and additions are assumed not to affect the application by running the tests.

- Test user is added into the database correctly
- Test user is not duplicated in database
- Test user can follow and unfollow a user.
- Test user can see followed users' posts.
