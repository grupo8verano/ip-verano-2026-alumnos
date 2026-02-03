
# capa de servicio/lógica de negocio

import random
from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

def getAllImages(input=None):
    # 1. Obtenemos los datos de la API a través del transporte.
    json_collection = transport.getAllImages()
    
    images = []

    for objeto in json_collection:
        # 2. Convertimos cada objeto en una Card usando el translator.
        # Usamos toCard porque es el método estándar para este proyecto.
        personaje_card = translator.fromRequestIntoCard(objeto)
        images.append(personaje_card)

    return images

def filterByCharacter(name):
    # Traemos los personajes filtrados directamente desde la API
    return getAllImages(name)

def filterByStatus(status_name):
    # Traemos todos los personajes y filtramos por estado (Vivo/Fallecido)
    all_images = getAllImages()
    filtered_images = []

    for card in all_images:
        if card.status == status_name:
            filtered_images.append(card)

    return filtered_images

# Funciones de favoritos (se quedan con pass por ahora para no dar error)
# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    # 1. El translator toma los datos de la pantalla y los prepara como una Card
    fav = translator.fromTemplateIntoCard(request)
    
    # 2. Buscamos qué usuario está logueado para asignarle el favorito
    # (Esto es lo que me preguntabas de fav.user)
    fav.user = get_user(request)
    
    # 3. El repositorio guarda esa Card en la base de datos local (SQLite)
    return repositories.saveFavourite(fav)

def getAllFavourites(request):
    # 1. Identificamos al usuario actual
    user = get_user(request)
    
    # 2. Le pedimos al repositorio todos los favoritos
    favourite_list = repositories.getAllFavourites(user)
    
    # --- ESTO ES LO QUE ARREGLA EL ERROR (Líneas 58-59 aprox) ---
    if favourite_list is None:
        favourite_list = []
    # -----------------------------------------------------------
    
    mapped_favourites = []
    for favourite in favourite_list:
        # 3. Convertimos cada dato en una Card para mostrarla
        card = translator.fromRepositoryIntoCard(favourite)
        mapped_favourites.append(card)

    return mapped_favourites

def deleteFavourite(request):
    # 1. Obtenemos el ID del personaje que el usuario quiere borrar (viene del botón borrar)
    fav_id = request.POST.get('id')
    
    # 2. El repositorio lo elimina definitivamente de la base de datos
    return repositories.deleteFavourite(fav_id)