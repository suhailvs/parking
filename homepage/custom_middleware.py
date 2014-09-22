from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class RestrictAdminMiddleware(object):
	"""Restricts Super user access only to /admin/."""
	def process_request(self, request):
		if request.user.is_active and request.user.is_superuser:
			#print request.path[:3]
			if request.path[:7] != '/admin/' and request.path[:3] != '/p/':
				return HttpResponseRedirect(reverse('admin:index'))