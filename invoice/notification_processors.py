from .models import Notify


def notifications(request):
    data = Notify.objects.filter(sent=True).order_by('-id')[:3]
    return {'notifications': data}