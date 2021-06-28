from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms.widgets import RadioSelect
from django.utils.translation import ugettext_lazy as _

from admin.models import Mail
from app.models import (AboutCinemaPage, AdvertisePage, CafeBarPage, 
    ChildrenRoomPage, Movie, News, Stock, SeoParameters, Image, 
    MainPageBanner, NewsAndStockBanner, MainPage, VipHallPage, 
    MobileAppPage, Cinema, Hall, CinemaContactsPage, Session)
from users.models import User


class AdminCinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = ('name_ru', 'name_uk', 'description_ru', 'description_uk', 'condition_ru', 'condition_uk', 'logo', 'banner')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_uk'].label = 'Назва кінотеатру (українською)'
        self.fields['name_ru'].label = 'Название кинотеатра (на русском)'
        self.fields['description_uk'].label = 'Опис (українською)'
        self.fields['description_ru'].label = 'Описание (на русском)'
        self.fields['condition_uk'].label = 'Умови (українською)'
        self.fields['condition_ru'].label = 'Условия (на русском)'


class AdminHallForm(forms.ModelForm):
    supported_types = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=Movie.MOVIE_TYPES
    )

    class Meta:
        model = Hall
        fields = ('number', 'description_ru', 'description_uk', 'banner', 'supported_types')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description_uk'].label = 'Опис (українською)'
        self.fields['description_ru'].label = 'Описание (на русском)'
        self.fields['supported_types'].label = _('Поддерживаемые форматы')

class AdminMovieForm(forms.ModelForm):
    type = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=Movie.MOVIE_TYPES
    )
    genre = forms.MultipleChoiceField(
        required=False,
        choices=Movie.GENRE,
    )

    class Meta:
        model = Movie
        fields = ('name_ru', 'name_uk', 'description_ru', 'description_uk', 'poster', 
            'trailer', 'type', 'duration', 'is_active', 'release_date', 'country_ru', 
            'director_ru', 'scriptwriter_ru', 'language_ru', 'age_limit',
            'budget_ru', 'country_uk', 'director_uk', 'scriptwriter_uk', 'language_uk', 
            'budget_uk', 'genre')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_uk'].label = 'Назва фільму (українською)'
        self.fields['name_ru'].label = 'Название фильма (на русском)'
        self.fields['description_uk'].label = 'Опис (українською)'
        self.fields['description_ru'].label = 'Описание (на русском)'
        self.fields['type'].label = _('Тип')
        self.fields['genre'].label = _('Жанр')


class AdminSessionForm(forms.ModelForm):
    format = forms.ChoiceField(label=_('Формат показа'), choices=Movie.MOVIE_TYPES, widget=forms.Select(attrs={'class': 'form-select'}))
    last_session_date = forms.DateTimeField(required=False, label=_('Дата последнего сеанса (опционально)'))
    
    class Meta:
        model = Session
        fields = ('movie', 'time', 'hall', 'format', 'price', 'vip_price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['movie'].label = _('Фильм')
        self.fields['hall'].label = _('Зал кинотеатра')

    def clean(self):
        data = self.cleaned_data
        if data.get('last_session_date') is not None and data['last_session_date'] < data['time']:
            raise forms.ValidationError(_('Дата последнего показа не может быть ранее даты первого показа'))
        return super().clean()


class AdminNewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ('title_ru', 'title_uk', 'description_ru', 'description_uk',
            'main_image', 'youtube_link', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title_uk'].label = 'Назва новини (українською)'
        self.fields['title_ru'].label = 'Название новости (на русском)'
        self.fields['description_uk'].label = 'Опис (українською)'
        self.fields['description_ru'].label = 'Описание (на русском)'
        


class AdminStockForm(forms.ModelForm):

    class Meta:
        model = Stock
        fields = ('title_ru', 'title_uk', 'description_ru', 'description_uk',
            'main_image', 'youtube_link', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title_uk'].label = 'Назва акції (українською)'
        self.fields['title_ru'].label = 'Название акции (на русском)'
        self.fields['description_uk'].label = 'Опис (українською)'
        self.fields['description_ru'].label = 'Описание (на русском)'


class SeoParametersForm(forms.ModelForm):

    class Meta:
        model = SeoParameters
        fields = ('seo_url', 'seo_title', 'seo_keywords', 'seo_description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['seo_url'].widget.attrs['class'] = 'form-control bg-light'
        self.fields['seo_title'].widget.attrs['class'] = 'form-control bg-light'
        self.fields['seo_keywords'].widget.attrs['class'] = 'form-control bg-light'
        self.fields['seo_url'].label = 'URL'
        self.fields['seo_title'].label = 'Title'
        self.fields['seo_keywords'].label = 'Keywords'
        self.fields['seo_description'].label = 'Description'


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('image',)


Gallery = generic_inlineformset_factory(Image, ImageForm, extra=4)


class MainBannerForm(forms.ModelForm):
    rotational_speed = list(MainPageBanner.SECONDS)
    rotational_speed = forms.ChoiceField(choices=tuple(rotational_speed), label=_('Скорость вращения'))
    
    class Meta:
        model = MainPageBanner
        fields = ('rotational_speed', 'backgroung_image')


class NewsAndStockBannerForm(forms.ModelForm):
    rotational_speed = list(NewsAndStockBanner.SECONDS)
    rotational_speed = forms.ChoiceField(choices=tuple(rotational_speed), label=_('Скорость вращения'))

    class Meta:
        model = NewsAndStockBanner
        fields = ('rotational_speed',)

    
class MainPageForm(forms.ModelForm):

    class Meta:
        model = MainPage
        fields = ('number1', 'number2', 'seo_text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['seo_text'].label = 'SEO текст'


class CafeBarForm(forms.ModelForm):

    class Meta:
        model = CafeBarPage
        fields = ('title_ru', 'title_uk', 'description_ru', 'description_uk', 'main_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title_uk'].label = 'Назва (українською)'
        self.fields['title_ru'].label = 'Название (на русском)'
        self.fields['description_uk'].label = 'Опис (українською)'
        self.fields['description_ru'].label = 'Описание (на русском)'


class VipHallForm(forms.ModelForm):

    class Meta:
        model = VipHallPage
        fields = ('title_ru', 'title_uk', 'description_ru', 'description_uk', 'main_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title_uk'].label = 'Назва (українською)'
        self.fields['title_ru'].label = 'Название (на русском)'
        self.fields['description_uk'].label = 'Опис (українською)'
        self.fields['description_ru'].label = 'Описание (на русском)'


class AboutCinemaForm(forms.ModelForm):

    class Meta:
        model = AboutCinemaPage
        fields = ('title_ru', 'title_uk', 'description_ru', 'description_uk', 'main_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title_uk'].label = 'Назва (українською)'
        self.fields['title_ru'].label = 'Название (на русском)'
        self.fields['description_uk'].label = 'Опис (українською)'
        self.fields['description_ru'].label = 'Описание (на русском)'


class AdvertiseForm(forms.ModelForm):

    class Meta:
        model = AdvertisePage
        fields = ('title_ru', 'title_uk', 'description_ru', 'description_uk', 'main_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title_uk'].label = 'Назва (українською)'
        self.fields['title_ru'].label = 'Название (на русском)'
        self.fields['description_uk'].label = 'Опис (українською)'
        self.fields['description_ru'].label = 'Описание (на русском)'


class ChildrenRoomForm(forms.ModelForm):

    class Meta:
        model = ChildrenRoomPage
        fields = ('title_ru', 'title_uk', 'description_ru', 'description_uk', 'main_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title_uk'].label = 'Назва (українською)'
        self.fields['title_ru'].label = 'Название (на русском)'
        self.fields['description_uk'].label = 'Опис (українською)'
        self.fields['description_ru'].label = 'Описание (на русском)'


class CinemaContactsPageForm(forms.ModelForm):

    class Meta:
        model = CinemaContactsPage
        fields = ('address', 'coordinates', 'logo')


class MobileAppForm(forms.ModelForm):

    class Meta:
        model = MobileAppPage
        fields = ('title_ru', 'title_uk', 'description_ru', 'description_uk', 'main_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title_uk'].label = 'Назва (українською)'
        self.fields['title_ru'].label = 'Название (на русском)'
        self.fields['description_uk'].label = 'Опис (українською)'
        self.fields['description_ru'].label = 'Описание (на русском)'


class UserUpdateForm(forms.ModelForm):
    language = forms.ChoiceField(label=_("Язык"), choices=(('ru', 'Русский'), ('ua', 'Українська')), 
        widget=RadioSelect(attrs={'class': 'form-check-input'}))
    gender = forms.ChoiceField(label=_("Пол"), choices=(('M', _('Мужской')), ('W', _('Женский'))), 
        widget=RadioSelect(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 
            'email', 'address', 'payment_card_number', 
            'language', 'gender', 'phone_number',
            'birth_date', 'city', 'is_active', 'is_staff',
            'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(label=_("Имя"), widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=32, required=False)
    last_name=forms.CharField(label=_("Фамилия"), widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=32, required=False)
    password1=forms.CharField(label=_("Пароль"), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2=forms.CharField(label=_("Повторите пароль"), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    language = forms.ChoiceField(label=_("Язык"), choices=(('ru', 'Русский'), ('ua', 'Українська')), 
        widget=RadioSelect(attrs={'class': 'form-check-input'}), required=False)
    gender = forms.ChoiceField(label=_("Пол"), choices=(('M', _('Мужской')), ('W', _('Женский'))), 
        widget=RadioSelect(attrs={'class': 'form-check-input'}), required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',
            'address', 'payment_card_number', 'is_superuser',
            'language', 'gender', 'phone_number',
            'birth_date', 'city', 'is_active', 'is_staff')


class MailingForm(forms.ModelForm):
    recipients = forms.ChoiceField(label=_('Выбрать email кому слать'), choices=(
        ('0', _('Все пользователи')), ('1', _('Выбранные пользователи'))),
        widget=RadioSelect(attrs={'class': 'form-check-input'}))
    file_id = forms.CharField(max_length=200)
    
    class Meta:
        model = Mail
        fields = ('email',)