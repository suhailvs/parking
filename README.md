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




paypal sandbox url
------------------

+ [accounts](https://developer.paypal.com/webapps/developer/applications/accounts)
+ [ipn url](https://developer.paypal.com/webapps/developer/applications/ipn_simulator)

for paypal testing use:

+ email: parkingbuyer@testing.com
+ password: suhail412

captcha
-------

https://www.google.com/recaptcha/admin

