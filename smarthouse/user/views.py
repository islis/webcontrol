from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
import logging

log = logging.getLogger(__name__)

class UserLoginView(LoginView):
    template_name = 'user/login_form.html'

    def get_success_url(self):
        log.info(f'{self.request.user} вошёл в систему')
        return reverse('main')

def user_logout(request):
    log.info(f'{request.user} вышёл из системы')
    return redirect('/', logout(request))
