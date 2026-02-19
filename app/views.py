# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from.models import Favourite
from django.contrib.auth import logout


def index_page(request):
    return render(request, 'index.html')

def home(request):
    """
    Vista principal que muestra la galería de personajes de Los Simpsons.
    
    Esta función debe obtener el listado de imágenes desde la capa de servicios
    y también el listado de favoritos del usuario, para luego enviarlo al template 'home.html'.
    Recordar que los listados deben pasarse en el contexto con las claves 'images' y 'favourite_list'.
    """ 
    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)

    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})

    
def search(request):
   from .services import filterByCharacter

def search(request):
    images = []
    query = request.POST.get("query", "").lower()
    if query != "":
        images = services.filterByCharacter(query)
    return render(request, "home.html", {"images": images})
    """
    Busca personajes por nombre.
    
    Se debe implementar la búsqueda de personajes según el nombre ingresado.
    Se debe obtener el parámetro 'query' desde el POST, filtrar las imágenes según el nombre
    y renderizar 'home.html' con los resultados. Si no se ingresa nada, redirigir a 'home'.
    """
    pass
    

def filter_by_status(request):
    """
    Filtra personajes por su estado (Alive/Deceased).
    """
    if request.method != "POST":
        return redirect("home")

    status = request.POST.get("status", "").strip()

    if status == "":
        return redirect("home")

    images = services.filterByStatus(status)
    favourite_list = services.getAllFavourites(request)

    return render(request, "home.html", {
        "images": images,
        "favourite_list": favourite_list
    })


    """
    Filtra personajes por su estado (Alive/Deceased).
    
    Se debe implementar el filtrado de personajes según su estado.
    Se debe obtener el parámetro 'status' desde el POST, filtrar las imágenes según ese estado
    y renderizar 'home.html' con los resultados. Si no hay estado, redirigir a 'home'.
    """
    

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)

    return render(request, 'favourites.html', {
        'favourite_list': favourite_list
    })




    """
    Obtiene todos los favoritos del usuario autenticado.
    """
    

@login_required
def saveFavourite(request):
    if request.method == "POST":
        services.saveFavourite(request)
    return redirect("home")
    """
    Guarda un personaje como favorito.
    """
       

@login_required
def deleteFavourite(request):
    if request.method != "POST":
        return redirect("home")
    
    fav_id = request.POST.get("id")
    if not fav_id:
        return redirect("home")
    
    #seguridad: que solo pueda borrar un favorito que le pertenece al usuario
    if not Favourite.objects.filter(id=fav_id, user=request.user).exists():
        return redirect("home")
    
    services.deleteFavourite(request) # esto usa repositorio.deleteFavourite(fav_id) para eliminarlo de la base de datos.
    return redirect("home")



    """
    Elimina un favorito del usuario.
    """
    

@login_required
def exit(request):
    logout(request)
    return redirect('home')