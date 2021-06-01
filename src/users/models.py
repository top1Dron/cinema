from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
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
    phone_number = models.CharField(_("Номер телефона"), max_length=13, unique=True,
        # valid=[+38(093)1350239,+38(093)135-02-39,+38(093)135 02 39,+380931350239,0931350239,+380445371428, +38(044)5371428,+38(044)537 14 28,+38(044)537-14-28,+38(044) 537.14.28,044.537.14.28,0445371428,044-537-1428,(044)537-1428,044 537-1428]
        # invalid = [+83(044)537 14 28,088 537-1428]
        validators=[
            validators.RegexValidator(
                regex=r'^(?:\+38)?(?:\(0[0-9][0-9]\)[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|044[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|0[0-9][0-9][0-9]{7})$')
        ])
    address = models.CharField(_("Адрес"), max_length=150, null=True, blank=True)
    payment_card_number = models.CharField(_("Номер карты"), max_length=16, null=True, blank=True)
    birth_date = models.DateField(_("Дата рождения"), null=True, blank=True)
    language = models.CharField(_("Язык"), max_length=2, choices=(('ru', _('')), ('ua', _(''))), null=True, blank=True)
    gender = models.CharField(_("Пол"), max_length=1, choices=(('M', _('')), ('W', _(''))), null=True, blank=True)
    city = models.IntegerField(_("Город"), choices=CITIES, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']


    def __str__(self) -> str:
        return self.email
    
    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
