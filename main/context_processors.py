
#Возвращает контекст для всех страниц для тем Django
def main_dark_theme(request):
    context = {
        'current_theme': request.session.get('theme', 'light'),
    }
    return context
