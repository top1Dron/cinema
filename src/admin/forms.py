from django import forms
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms.widgets import RadioSelect
from django.utils.translation import ugettext_lazy as _

from app.models import (AboutCinemaPage, AdvertisePage, CafeBarPage, 
    ChildrenRoomPage, Movie, News, Stock, SeoParameters, Image, 
    MainPageBanner, NewsAndStockBanner, MainPage, VipHallPage, 
    MobileAppPage)
from users.models import User


class AdminMovieForm(forms.ModelForm):
    type = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=Movie.MOVIE_TYPES
    )

    class Meta:
        model = Movie
        fields = ('name_ru', 'name_uk', 'description_ru', 'description_uk', 'poster', 
            'trailer', 'type', 'duration', 'is_active', 'release_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_uk'].label = 'Назва фільму (українською)'
        self.fields['name_ru'].label = 'Название фильма (на русском)'
        self.fields['description_uk'].label = 'Опис (українською)'
        self.fields['description_ru'].label = 'Описание (на русском)'
        self.fields['type'].label = _('Тип')


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
            'is_superuser', 'date_joined')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)