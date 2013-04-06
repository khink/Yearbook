Information
-----------
This is an application aimed at collecting data for the Yearbook created for
the passing out batch of the institute. The application allows the user to add
details about him by answering questions (such as : 'Favourite quotation',
'Where do you see yourself in 5 years?') and let's users post some remark
(called 'testimonial' here) about another user. These details are then
reflected in the printed yearbook.



Installation instructions
-------------------------

1. This is a Web2Py application, so you need a Web2Py installation.

2. All the content of this repository should reside in in a folder in the
"applications" folder of Web2Py.

   For instance, let your Web2Py folder be `~/web2py`, then you would need to
   clone this repository in `~/web2py/applications` yielding a folder as
   `~/web2py/applications/Yearbook2013`. To access the site, you would then
   need to visit `http://<host_address>:<port>/Yearbook2013/`


Database related information
-----------------------------

* Currently, this application makes use of SQLite.
* To modify that look into `models/db.py`.


HHC Branch
----------

A branch for customer modifications.

This branch targets the following:
* Modify departments structure
* Modify personal data on profile, notably:
  - Display 2 photos (students need not be able to change these)
    Photos should not be on a publicly accessible URL.
* Allow adding testimonials for teachers/professors
* Disable or modify workflow (approval mechanism)
* Add an overview page for the book layouters

Then there's some small stuff, like
* Dutch translation
* Modify templates

We should also prevent login by brute force, but that should probably happen in
web2py.
