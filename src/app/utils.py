import logging

from django.shortcuts import get_object_or_404

from app.models import Movie, Image


logger = logging.getLogger(__name__)


def get_movie_by_params(**kwargs):
    return get_object_or_404(Movie, **kwargs)


def get_image_by_id(id):
    return get_object_or_404(Image, id=id)
