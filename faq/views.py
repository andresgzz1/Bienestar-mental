from django.shortcuts import render, redirect

from faq.models import faq
from django.contrib import messages

# Create your views here.



# listar usuarios creados vista admin
def view_adminfaq(request, type):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:

            if type == "depresion":
                faqs = faq.objects.filter(type=type)

            return render(request, 'admin/admin_faq.html', {'user': user,'faqs': faqs})
    else:
        return redirect('login2')



# listar usuarios creados vista admin
def add_faq(request, type):
    user = request.user
    if user.is_authenticated:

        if user.is_admin:
            
            txtQuestion = request.POST.get('txtQuestion')
            txtResp = request.POST.get('txtResp')

            if txtResp == None or txtQuestion == None:
                messages.error(request, 'Debe llenar todos los campos')
            else:
                faq.objects.create(question=txtQuestion, resp=txtResp, type=type, state=True)
                messages.success(request, 'Pregunta agregada con exito')

            return redirect('faqAdmin', type=type)
    else:
        return redirect('login2')


# listar usuarios creados vista admin
def edit_faq(request, type, id):
    user = request.user
    if user.is_authenticated:

        if user.is_admin:
            
            faqUpdate = faq.objects.get(id=id)

            txtQuestion = request.POST.get('txteditQuestion')
            txtResp = request.POST.get('txteditResp')

            if txtResp == None or txtQuestion == None:
                messages.error(request, 'Debe llenar todos los campos')
            else:
                faqUpdate.question = txtQuestion
                faqUpdate.resp = txtResp
                faqUpdate.save()

                messages.success(request, 'Pregunta editada con exito')

            return redirect('faqAdmin', type=type)
    else:
        return redirect('login2')


# users
def delfaq(request, id):
    user = request.user
    if user.is_authenticated:
            if faq.objects.filter(id=id).exists():
                faqUpdate = faq.objects.get(id=id)
                faqUpdate.delete()
                messages.add_message(request=request, level=messages.SUCCESS, message="FAQ eliminada correctamente")
            else:
                messages.add_message(request=request, level=messages.SUCCESS, message="Ya no existe el registro a eliminar")

            return redirect('faqAdmin', faqUpdate.type )
    else:
        return redirect('login2')