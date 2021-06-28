from app import utils
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import RadioSelect
from django.utils.translation import ugettext_lazy as _

from app.models import Movie, Session
from users.models import User


class UserCreateForm(UserCreationForm):
    password1=forms.CharField(label=_("Пароль"), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2=forms.CharField(label=_("Повторите пароль"), widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserUpdateForm(forms.ModelForm):
    language = forms.ChoiceField(label=_("Язык"), choices=(('ru', 'Русский'), ('ua', 'Українська')), 
        widget=RadioSelect(attrs={'class': 'form-check-input'}))
    gender = forms.ChoiceField(label=_("Пол"), choices=(('M', _('Мужской')), ('W', _('Женский'))), 
        widget=RadioSelect(attrs={'class': 'form-check-input'}))
    password1 = forms.CharField(label=_('Пароль'), max_length=250, required=False)
    password2 = forms.CharField(label=_('Подтвердите пароль'), max_length=250, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 
            'email', 'address', 'payment_card_number', 
            'language', 'gender', 'phone_number',
            'birth_date', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1:
            if password1 != password2:
                raise forms.ValidationError(_('Пароли не совпадают!'))
            if len(password1) < 8:
                raise forms.ValidationError(_('Пароль должен быть не менее 8 символов!'))
            if not any(c.isupper() for c in password1):
                raise forms.ValidationError(_('Пароль должен содержать хотя бы 1 символ в верхнем регистре!'))
            if not any(c.islower() for c in password1):
                raise forms.ValidationError(_('Пароль должен содержать хотя бы 1 символ в нижнем регистре!'))
            if not any(c.isdigit() for c in password1):
                raise forms.ValidationError(_('Пароль должен содержать хотя бы 1 цифру!'))
        return super().clean()


class SessionFilterForm(forms.ModelForm):
    movie_choices = [(movie.pk, movie.name) for movie in utils.get_active_movies()]
    movie_choices.insert(0, ('', _('Все')))
    movie = forms.ChoiceField(choices=tuple(movie_choices), label=_('Фильмы'))
    
    cinema_choices = [(cinema.pk, cinema.name) for cinema in utils.get_cinemas()]
    cinema_choices.insert(0, ('', _('Все')))
    cinema = forms.ChoiceField(choices=tuple(cinema_choices), label=_('Кинотеатры'))
    
    format_choices = list(Movie.MOVIE_TYPES)
    format_choices.insert(0, ('', _('Все')))
    format = forms.ChoiceField(
        label=_('Формат'),
        # widget=forms.CheckboxSelectMultiple,
        choices=tuple(format_choices)
    )

    class Meta:
        model = Session
        fields = ['movie', 'cinema']