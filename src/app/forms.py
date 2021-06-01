import logging

from django import forms
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from app.models import Movie, SeoParameters, Image



class MovieForm(forms.ModelForm):
    type = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=Movie.MOVIE_TYPES
    )

    class Meta:
        model = Movie
        fields = ('name', 'name_uk', 'description', 'description_uk', 'poster', 
            'trailer', 'type', 'duration', 'is_active', 'release_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name_uk'].label = 'Назва фільму (українською)'
        self.fields['description_uk'].label = 'Опис (українською)'
        # self.fields['trailer'].widget.attrs['class'] = 'form-control'
        # self.fields['type'].widget.attrs['class'] = 'form-group'


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