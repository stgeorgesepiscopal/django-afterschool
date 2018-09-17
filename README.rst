Django Afterschool
======================

Check-in and check-out for afterschool (as well as some other fun stuff)

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django

.. image:: https://img.shields.io/badge/python-3.7-blue.svg
    :alt:  Python Version 3.7

.. image:: https://img.shields.io/badge/Django-2.1.1-green.svg
    :alt:  Django Version 2.1.1


:License: GPLv3

Description
-----------
St. George's Episcopal School in New Orleans, LA needed a simple way to manage afterschool in-and-out as well as a "Student Finder" that was more intuitive than their current SIS (called PCR).  The CSV imports that are currently built into this package are specific to the PCR Exports.  Anyone interested in making them more generalized is welcome to make a PR!

Installing
----------

Requirements
^^^^^^^^^^^^
* Python 3.7

Setup
^^^^^
* (Recommended) Start a virtualenv with Python 3.7
* Clone the repo ::

    $ git clone https://github.com/sreyemnayr/django-afterschool.git

* Navigate to the new repo ::

    $ cd django-afterschool

* Install required packages ::

    $ pip install -r requirements/local.txt

* Create and edit the .env file ::

    $ cp .env.example .env
    $ nano .env


Basic Commands
--------------

Starting up the server
^^^^^^^^^^^^^^^^^^^^^^

* To run locally, just clone the repo and run ::

    $ python manage.py runserver

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.


Deployment
----------

This application can be deployed with nginx/gunicorn or whatever other WSGI setup you prefer.




