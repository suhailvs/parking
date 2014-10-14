from django.shortcuts import render

def my_custom_404_view(request):
	return render(request,'errorpages/error_404.html')

from django.http import HttpResponse
from homepage.models import Parking
from django.conf import settings
import os
def delete_unused_media_files(request):
    parks=[p.pic.name.lower().lstrip('images/') for p in Parking.objects.all()]
    
    folder=os.path.join(settings.MEDIA_ROOT,'images')
    files = [f.lower() for f in os.listdir(folder)] # if os.path.isfile(f)]

    todel=[f for f in files if f not in parks]
    deleted_items=[]
    for f in todel:
        fname=os.path.join(folder,f)
        try:
            os.remove(fname)
            deleted_items.append(fname)
        except:pass
    """
    msg='parking_database:{0} <br> media_folder:{1} <br> files to delete: {2}'.format(
    	','.join(parks),
    	','.join(files),   
    	','.join(todel) 	
    )
    """
    msg="<strong>Deleted:</strong><br>{0}".format('<br> + '.join(deleted_items))
    return HttpResponse(msg)
