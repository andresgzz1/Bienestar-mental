from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from profesional.views import valid_extension
from relaxation_space.models import gif_space, image_space, sound_space, space as sp
from django.contrib import messages
from rest_framework.response import Response


def valid_extensionGif(value):
    if (not value.name.endswith('.gif')) and value.name is not None:
        return Response({'Msj': 'Error, formato no permitido'})


# Create your views here.


@login_required()
def adminView_rp(request):

    user = request.user
    if user.is_admin:
        spaces = []
        images_list = []
        images_list_format = []
        spaces_disponibles = []
        if sp.objects.all().exists():
            spaces = sp.objects.all()
            for space in spaces:
                if image_space.objects.filter(space=space).exists():
                    images = image_space.objects.filter(space=space)
                    images_list.extend(images)

                else:
                    """ Se asigna el space a una lista de espacios disponibles """
                    spaces_disponibles.append(space)
            for image in images_list:
                """ print url de imagen """

                img = {
                    'id': image.id,
                    'name_image': image.name_image,
                    'img_space': image.space_img,
                    'space': image.space,
                }
                images_list_format.append(img)

        else:

            spaces_name_list = ['Lluvia', 'Cafetería',
                                'Playa', 'Noche', 'Viento']

            for space_name in spaces_name_list:
                spaces_get = sp.objects.create(
                    space_name=space_name,
                )
                images = image_space.objects.filter(space=spaces_get)

                images_list.extend(images)

                for image in images_list:
                    img = {
                        'id': image.id,
                        'name_image': image.name_image,
                        'img_space': image.space_img,
                        'space': image.space,
                    }
                    images_list_format.append(img)

                spaces.extend(spaces_get)

        return render(request, 'admin/admin_relax_space.html', {'spaces': spaces, 'images_list': images_list_format, 'spaces_disponibles': spaces_disponibles})
    else:
        return redirect('login2')


@login_required()
def adminView_rp_add(request):
    user = request.user
    if user.is_admin:
        if request.method == 'POST':
            space = request.POST.get('txtSpace')
            name_image = request.POST.get('txtNameImage')
            img_space = request.FILES.get('txtImage')

            space_object = sp.objects.get(id=space)

            """ Validar existencia de imagenes en space """
            if valid_extension(img_space):
                messages.add_message(request=request, level=messages.ERROR,
                                     message="Error, formato no permitido. Formatos permitidos: png, jpg, jpeg, gif, bmp")
            elif image_space.objects.filter(space=space_object).exists():
                """ mandar mensaje error """
                messages.add_message(request=request, level=messages.SUCCESS, message="Ya se encuentra asignada una imagen, sólo puedes agregar una imagen al espacio de relajación " +
                                     space_object.space_name + ".", extra_tags='alert alert-danger alert-dismissible fade show')
            else:
                messages.add_message(request=request, level=messages.SUCCESS, message="Imagen agregada correctamente al espacio de relajación " +
                                     space_object.space_name + ".", extra_tags='alert alert-success alert-dismissible fade show')
                image_space.objects.create(
                    name_image=name_image,
                    space_img=img_space,
                    space=space_object,
                )
            return redirect('adminView_rp')
        else:
            return render(request, 'admin/admin_relax_space_add.html')
    else:
        return redirect('login2')


@login_required()
def adminView_rp_delete(request, idImage):
    user = request.user
    if user.is_admin:
        if request.method == 'POST':
            if image_space.objects.filter(id=idImage).exists():
                image_space.objects.get(id=idImage).delete()
                messages.add_message(request=request, level=messages.SUCCESS, message="Imagen eliminada correctamente.",
                                     extra_tags='alert alert-success alert-dismissible fade show')
            else:
                messages.add_message(request=request, level=messages.SUCCESS, message="No se encuentra la imagen.",
                                     extra_tags='alert alert-danger alert-dismissible fade show')
            return redirect('adminView_rp')
        else:
            return render(request, 'admin/admin_relax_space_add.html')
    else:
        return redirect('login2')


@login_required()
def adminView_rp_update(request, idImage):
    user = request.user
    if user.is_admin:
        if request.method == 'POST':
            space = request.POST.get('txtSpace')
            name_image = request.POST.get('txtNameImage')
            img_space = request.FILES.get('txtImage')

            image_object = image_space.objects.get(id=idImage)

            space_object = sp.objects.get(id=space)

            if (name_image == '' or image_object.name_image == name_image) and (img_space == None) and (space_object == image_object.space or space_object == ''):
                messages.add_message(
                    request=request, level=messages.ERROR, message="No se han realizado cambios")
            else:
                if img_space is not None and valid_extension(img_space):
                    messages.add_message(request=request, level=messages.ERROR,
                                         message="Error, formato no permitido. Formatos permitidos: png, jpg, jpeg, gif, bmp")
                elif image_space.objects.filter(space=space_object).exists() and space_object != image_object.space:
                    """ mandar mensaje error """
                    messages.add_message(request=request, level=messages.SUCCESS, message="Ya se encuentra asignada una imagen, sólo puedes agregar una imagen al espacio de relajación " +
                                         space_object.space_name + ".", extra_tags='alert alert-danger alert-dismissible fade show')
                elif name_image == '':
                    messages.add_message(request=request, level=messages.ERROR,
                                         message="Error, el nombre de la imagen no puede estar vacío")
                else:
                    messages.add_message(request=request, level=messages.SUCCESS, message="Imagen actualizada correctamente.",
                                         extra_tags='alert alert-success alert-dismissible fade show')
                    image_object.name_image = name_image
                    if img_space is not None:
                        image_object.space_img = img_space
                    image_object.space = space_object
                    image_object.save()

            return redirect('adminView_rp')
        else:
            return render(request, 'admin/admin_relax_space.html')
    else:
        return redirect('login2')


""" Renderizar vista de admin spacio de relajación GIFS """


@login_required()
def adminView_rp_gif(request, idSpace):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:

            gifsList = []

            if sp.objects.filter(id=idSpace).exists():
                space = sp.objects.get(id=idSpace)
                if gif_space.objects.filter(space=space).exists():
                    gifs = gif_space.objects.filter(space=space)
                    gifsList.extend(gifs)
                else:
                    gifsList = []

                return render(request, 'admin/gifs_relax_space.html', {'gifs': gifsList, 'space': space})
            else:
                messages.add_message(request=request, level=messages.ERROR,
                                     message="No se ha encontrado espacios de relajación")
                return redirect('login2')
        else:
            messages.add_message(request=request, level=messages.ERROR,
                                 message="No tienes permisos para acceder a esta sección")
            return redirect('login2')

    else:
        return redirect('login2')


@login_required()
def rp_gif_add(request, idSpace):
    user = request.user
    if user.is_admin:
        if request.method == 'POST':

            if sp.objects.filter(id=idSpace).exists():
                space_object = sp.objects.get(id=idSpace)
                name_image = request.POST.get('txtNameGif')
                img_space = request.FILES.get('txtImage')

                """ Validar existencia de imagenes en space """
                if valid_extensionGif(img_space):
                    messages.add_message(request=request, level=messages.ERROR,
                                         message="Error, formato no permitido, ingrese un archivo GIF.")
                else:
                    gif_space.objects.create(
                        name_gif=name_image,
                        gif_space=img_space,
                        space=space_object,
                    )
                    messages.add_message(request=request, level=messages.SUCCESS, message="GIF agregada correctamente al espacio de relajación " +
                                         space_object.space_name + ".", extra_tags='alert alert-success alert-dismissible fade show')

                return redirect('adminView_rp_gif', idSpace)
            else:
                messages.add_message(request=request, level=messages.ERROR,
                                     message="No se ha encontrado espacios de relajación")
                return redirect('login2')
        else:
            return render(request, 'admin/admin_relax_space_add.html')
    else:
        return redirect('login2')


@login_required()
def rp_gif_delete(request, idGif):
    user = request.user
    if user.is_admin:
        if gif_space.objects.filter(id=idGif).exists():
            gif = gif_space.objects.get(id=idGif)
            space_id = gif.space.id
            gif.delete()
            messages.add_message(request=request, level=messages.SUCCESS, message="GIF eliminado correctamente.",
                                 extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('adminView_rp_gif', space_id)
        else:
            messages.add_message(
                request=request, level=messages.ERROR, message="No se ha encontrado GIF")
            return redirect('adminView_rp')
    else:
        return redirect('login2')


@login_required()
def rp_gif_edit(request, idGif):
    user = request.user
    if user.is_admin:
        name_image = request.POST.get('txtNameImage')
        img_space = request.FILES.get('txtImage')

        image_object = gif_space.objects.get(id=idGif)

        if (name_image == '' or image_object.name_gif == name_image) and (img_space == None):
            messages.add_message(
                request=request, level=messages.ERROR, message="No se han realizado cambios")
        else:
            if img_space is not None and valid_extensionGif(img_space):
                messages.add_message(request=request, level=messages.ERROR,
                                     message="Error, formato no permitido, ingrese un archivo GIF")
            elif name_image == '':
                messages.add_message(request=request, level=messages.ERROR,
                                     message="Error, el nombre de la imagen no puede estar vacío")
            else:
                image_object.name_gif = name_image
                if img_space is not None:
                    image_object.gif_space = img_space
                image_object.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Imagen actualizada correctamente.",
                                     extra_tags='alert alert-success alert-dismissible fade show')

        return redirect('adminView_rp_gif', image_object.space.id)


""" Renderizar vista principal de spacio de relajación """


@login_required()
def relax_space_view(request, type):
    user = request.user
    if user.is_authenticated:
        spaces_format = []
        gifs_space_format = []
        sonido_list = []
        if sp.objects.filter().exists():
            spaces = sp.objects.all()
            for space in spaces:
                if image_space.objects.filter(space=space).exists():
                    image = image_space.objects.get(space=space)
                    img = {
                        'id': space.id,
                        'space_name': space.space_name,
                        'img_space': image.space_img,
                    }
                    spaces_format.append(img)
            if spaces_format == [] and user.is_client:
                messages.add_message(request=request, level=messages.ERROR,
                                     message="No se han encontrado espacios de relajación, vuelva a intentar mas tarde...")
                return redirect('login2')

            if type == 'default':
                pass
            else:
                if gif_space.objects.filter(space_id=type).exists():
                    gifs_space_list = gif_space.objects.filter(space_id=type)
                    gifs_space_format.extend(gifs_space_list)
                    sonido = sound_space.objects.filter(space_id=type)
                    sonido_list.extend(sonido)
                else:
                    pass

            return render(request, 'user/space_relax.html', {'spaces': spaces_format, 'gifs': gifs_space_format, 'sonido_list': sonido_list, 'type': type})
        else:
            messages.add_message(request=request, level=messages.ERROR,
                                 message="No se ha encontrado espacios de relajación, vuelva a intentar mas tarde...")
            if user.is_admin:
                spaces_name_list = ['Lluvia', 'Cafetería',
                                    'Playa', 'Noche', 'Viento']
                for space_name in spaces_name_list:
                    space_get = sp.objects.create(space_name=space_name)
            return redirect('login2')

    else:
        return redirect('login2')


@login_required()
def adminView_rp_sounds(request, idSpace):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            soundlist = []
            if sp.objects.filter(id=idSpace).exists():
                space = sp.objects.get(id=idSpace)
                if sound_space.objects.filter(space=space).exists():
                    sounds = sound_space.objects.filter(space=space)
                    soundlist.extend(sounds)
                else:
                    soundlist = []
                return render(request, 'admin/sound_relax_space.html', {'sound': soundlist, 'space': space})
            else:
                messages.add_message(request=request, level=messages.ERROR,
                                     message="No se ha encontrado espacios de relajación")
                return redirect('login2')
        else:
            messages.add_message(request=request, level=messages.ERROR,
                                 message="No tienes permisos para acceder a esta sección")
            return redirect('login2')


""" Crud sound in relaxation_space """


def validar_musica(value):
    if (not value.name.endswith('.mp3') and
        not value.name.endswith('.wav') and
            not value.name.endswith('.mp3')) and value.name is not None:
        return Response({'Msj': 'Error, formato no permitido'})


@login_required()
def add_sound_rp(request, idSpace):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if sp.objects.filter(id=idSpace).exists():
                space_object = sp.objects.get(id=idSpace)
                name_music = request.POST.get('txtNameSound')
                soundspace = request.FILES.get('sound')
                if soundspace is not None and validar_musica(soundspace):
                    messages.add_message(request=request, level=messages.ERROR, message="Error, Formato no permitido" +
                                         "Porfavor suba el archivo en el formato permitido: .mp3 .WAV")
                    return redirect('adminView_rp_sound', idSpace)
                else:
                    sound_space.objects.create(
                        name_music=name_music,
                        music_space=soundspace,
                        space=space_object,
                    )
                    messages.add_message(request=request, level=messages.SUCCESS, message="Sonido agregada correctamente al espacio de relajación " +
                                         space_object.space_name + ".", extra_tags='alert alert-success alert-dismissible fade show')
                return redirect('adminView_rp_sound', idSpace)
            else:
                messages.add_message(request=request, level=messages.ERROR,
                                     message="No se ha encontrado espacios de relajación")
                return redirect('login2')
        else:
            return render(request, 'admin_relax_space_add.html')
    else:
        return redirect('login2')


@login_required()
def sound_space_view(request):
    user = request.user
    if user.is_authenticated:
        spaces_format = []
        if sp.objects.filter().exists():
            spaces = sp.objects.all()
            for space in spaces:
                if sound_space.objects.filter(space=space).exists():
                    sound = sound_space.objects.get(space=space)
                    snd = {
                        'id': space.id,
                        'space_name': space.space_name,
                        'img_space': sound.music_space.url,
                    }
                    spaces_format.append(snd)
                else:
                    snd = {
                        'id': space.id,
                        'space_name': space.space_name,
                        'img_space': '',
                    }
                    spaces_format.append(snd)
        else:
            spaces_format = None

        return render(request, 'user/sound_relax_space.html', {'spaces': spaces_format})

    else:
        return redirect('login2')


@login_required()
def delete_sound_rp(request, idsound):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:

            if sound_space.objects.filter(id=idsound).exists:
                sound_del = sound_space.objects.get(id=idsound)
                id_sp = sound_del.space.id
                sound_del.delete()
            messages.add_message(
                request=request, level=messages.SUCCESS, message="Sound deleted successfully")
            return redirect('adminView_rp_sound', id_sp)
        else:
            return render(request, 'admin/admin_relax_space_add.html')
    else:
        return redirect('login2')


@login_required()
def update_sound_rp(request, idsound):
    user = request.user
    if user.is_admin:
        name_sound = request.POST.get('txtnamesound')
        soun_space = request.FILES.get('music_space')

        sound_object = sound_space.objects.get(id=idsound)

        if (name_sound == '' or sound_object.name_music == name_sound) and (soun_space == None):
            messages.add_message(
                request=request, level=messages.ERROR, message="No se han realizado cambios")
        else:
            if soun_space is not None and validar_musica(soun_space):
                messages.add_message(request=request, level=messages.ERROR, message="Error, Formato no permitido" +
                                     "Porfavor suba el archivo en el formato permitido: .mp3 .WAV")
            elif name_sound == '':
                messages.add_message(request=request, level=messages.ERROR,
                                     message="Error, el nombre del sonido no puede estar vacío")
            else:
                sound_object.name_music = name_sound
                if soun_space is not None:
                    sound_object.music_space = soun_space
                sound_object.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Sonido actualizada correctamente.",
                                     extra_tags='alert alert-success alert-dismissible fade show')

    return redirect('adminView_rp_sound', sound_object.space.id)
