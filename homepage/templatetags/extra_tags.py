from django import template
register = template.Library()
"""
@register.simple_tag
def get_my_orders(user):	
	return "some"
"""

@register.filter
def get_imgurl(park, arg='160'):
	# arg can be crop or 160	
    return "{0}_{1}.jpg".format(park.pic.url[:-4],arg) if park.pic else ''