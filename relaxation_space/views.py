from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def adminView_rp(request):
    user = request.user
    if user.is_admin:
        return render(request, 'admin/admin_relax_space.html')
    else:
        return redirect(request, 'admin/admin_relax_space.html')