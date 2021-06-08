from django import forms
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from app.models import Movie, News, Stock, SeoParameters, Image, MainPageBanner, NewsAndStockBanner


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
