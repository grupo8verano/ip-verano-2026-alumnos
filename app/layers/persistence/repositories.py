# capa DAO de acceso/persistencia de datos.
from app.models import Favourite

def saveFavourite(fav):
    favourite, created = Favourite.objects.get_or_create(
        name=fav.name,
        user=fav.user,
        defaults={
            "gender": fav.gender,
            "status": fav.status,
            "occupation": fav.occupation,
            "phrases": fav.phrases,
            "age": fav.age,
            "image": fav.image,
        }
    )
    return favourite
    
    
def getAllFavourites(user):
     return Favourite.objects.filter(user=user).values(
        "id", "name", "gender", "status", "occupation", "phrases", "age", "image", "user_id"
    )

    
"""
    Obtiene todos los favoritos de un usuario desde la base de datos.
    """

def deleteFavourite(favId):
    favourite = Favourite.objects.get(id=favId)
    favourite.delete()
    return True