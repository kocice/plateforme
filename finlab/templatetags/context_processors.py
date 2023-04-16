# context_processors.py

from django.contrib.auth.decorators import login_required
from credit.models import Notification


# @login_required(login_url='finlab:login')
def notifications(request):
    if request.user.is_authenticated:
        user = request.user
        notifications = Notification.objects.filter(destinataire=user, lue=False).order_by('-date_envoie')[:5]
        notifications = None if len(notifications) == 0 else notifications
    else:
        notifications = None
    return {'notifications': notifications}
