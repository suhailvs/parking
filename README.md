parking
=======

list parking


There will be a map, which will show some [markers](https://developers.google.com/maps/documentation/javascript/examples/marker-simple) where parking space is available. when user clicks a marker it will redirect to another page where user can view the details of parking space, such as:

+ real photos,
+ its availability(what time it is available in [calendar view](http://arshaw.com/fullcalendar/))
+ do checkout at there if he is logged in(paypal).

also logged in users can:

+ add details about them.
+ view their payments and parking space they purchase.
+ List their parking space

Requirements
------------

	django
	django-user-accounts==1.0b18
	django-bootstrap-form
	Pillow


Email
-----

+ EMAIL_HOST = 'smtpout.secureserver.net'
+ EMAIL_HOST_USER = 'info@flexspot.co'
+ EMAIL_HOST_PASSWORD = 'Password123' 
+ EMAIL_PORT = 80
+ EMAIL_USE_TLS = False