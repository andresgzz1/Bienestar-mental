from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from relaxation_space.models import image_space, space as sp

# Create your views here.
@login_required()
def adminView_rp(request):
    user = request.user
    if user.is_admin:
        spaces = []
        images_list = []
        if sp.objects.all().exists():
            spaces = sp.objects.all()
            for space in spaces:
                if image_space.objects.filter(space = space).exists():
                    images = image_space.objects.filter(space=space)
                    images_list.extend(images)
            
        else:
            
            spaces_name_list = ['Lluvia', 'Cafetería', 'Playa', 'Noche', 'Viento']

            for space_name in spaces_name_list:
                spaces_get = sp.objects.create(
                space_name = space_name,
                )
                images = image_space.objects.filter(space=spaces_get)
                
                images_list.extend(images)
                spaces.extend(spaces_get)


        return render(request, 'admin/admin_relax_space.html',{'spaces': spaces,'images_list': images_list})
    else:
        return redirect(request, 'admin/admin_relax_space.html')