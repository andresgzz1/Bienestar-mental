from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from relaxation_space.models import space

# Create your views here.
@login_required()
def adminView_rp(request):
    user = request.user
    if user.is_admin:
        spaces = []
        if space.objects.all().exists():
            spaces = space.objects.all()
        else:
            
            spaces_name_list = ['Lluvia', 'Cafetería', 'Playa', 'Noche', 'Viento']

            for space_name in spaces_name_list:
                spaces_get = space.objects.create(
                space_name = space_name,
                )
                spaces.append(spaces_get)


        return render(request, 'admin/admin_relax_space.html', {'spaces': spaces})
    else:
        return redirect(request, 'admin/admin_relax_space.html')