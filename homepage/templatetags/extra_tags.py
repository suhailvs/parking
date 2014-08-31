from django import template
from homepage.models import Orders
register = template.Library()

@register.simple_tag
def get_my_orders(user):
	od= Orders.objects.filter(user__id=user)
	if not od:
		return ''
	str_html=template.Template("""
<div class="well">
	<h3> Orders done by <code>{{request.user}}</code></h3>	
	<table class="table">
		<tr>
			<th>Sl</th><th>Parking Address</th>
			<th>Order Date</th><td>Parking Date</th>
			<th>Duration</th><th>Payment</th>
		</tr>
		{% for order in ods %}
		<tr>
			<td>{{forloop.counter}}</td><td>{{order.parking.streetaddress}}</td>
			<td>{{order.order_date}}</td><td>{{order.park_date}}</td>
			<td>{{order.duration}} Hours</td><td>{{order.paid}}</td>
		</tr>
		{% endfor %}
	</table>
</div>""")
	return str_html.render(template.Context({'ods':od}))