from django.db import models
from homepage.models import User,Order
# Create your models here.

class Log_errors(models.Model):
	time_occured = models.DateTimeField(auto_now_add=True)
	errors=models.TextField(blank=True)
	def __unicode__(self):
		return unicode(self.errors)


from paypal.standard.ipn.signals import payment_was_successful
def show_me_the_money(sender, **kwargs):
	ipn_obj = sender
	# You need to check 'payment_status' of the IPN
	import time
	log='called show me money:{0}\n'.format(time.time())#print ('called show me money')

	if ipn_obj.payment_status == "Completed":
		# Undertake some action depending upon `ipn_obj`.
		#if ipn_obj.custom == "Upgrade all users!":
		#    Users.objects.update(paid=True)
		try:
			orderid= int(ipn_obj.invoice)
			log+='passed orderid:{0}'.format(orderid)
			cur_order=Order.objects.get(id=orderid)			
			cur_order.paid=True
			cur_order.save()
			# increment the credit balance
			#cur_order.user.UserDetails.increment_credit_balance(cur_order.pack.credits)
			log+='order paid:{0}\n'.format(orderid)
		except ValueError:
			log+='Unable to conver ipn_obj.invoice to integer.\n'
		except NameError:
			log+='ipn_obj.invoice doesnt exist\n'
			log+='ERROR: Doesnt saved Order paid\n'
		except:
			log+='ERROR: Doesnt saved Order paid\n'
			#raise
		log+='suuccess\n'
	else:
		log+='error:ipn_obj.payment_status = {0}\n'.format(ipn_obj.payment_status)
	Log_errors(errors=log).save()

payment_was_successful.connect(show_me_the_money)