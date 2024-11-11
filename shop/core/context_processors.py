from .models import Categories

def categories(request):
    return {
        'categories': Categories(request)
    }