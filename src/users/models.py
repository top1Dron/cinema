from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

class User(AbstractUser):
    CITIES = (
        (1, _('Одесса')),
        (2, _('Николаев')),
        (3, _('Херсон')),
        (4, _('Винница')),
        (5, _('Киев')),
        (6, _('Львов')),
        (7, _('Харьков')),
        (8, _('Тернополь')),
        (9, _('Кропивницкий')),
        (10, _('Ивано-Франковск')),
        (11, _('Днепр')),
        (12, _('Запорожье')),
        (13, _('Ужгород')),
        (14, _('Луцк')),
        (15, _('Мариуполь')),
        (16, _('Черкассы')),
        (17, _('Чернигов')),
        (18, _('Черновцы')),
    )

    email = models.EmailField(_('E-mail'), unique=True)
    phone_number = models.CharField(_("Номер телефона"), max_length=13, unique=True)
    address = models.CharField(_("Адрес"), max_length=150, null=True, blank=True)
    payment_card_number = models.CharField(_("Номер карты"), max_length=16, null=True, blank=True)
    birth_date = models.DateField(_("Дата рождения"), null=True, blank=True)
    language = models.CharField(_("Язык"), max_length=2, choices=(('ru', _('')), ('ua', _(''))), null=True, blank=True)
    gender = models.CharField(_("Пол"), max_length=1, choices=(('M', _('')), ('W', _(''))), null=True, blank=True)
    city = models.IntegerField(_("Город"), choices=CITIES, null=True, blank=True)


    def __str__(self) -> str:
        return self.email
    
    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
