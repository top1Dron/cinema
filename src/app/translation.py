from modeltranslation.translator import register, TranslationOptions
from app.models import Movie, Cinema, Hall, News, Stock


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Cinema)
class CinemaTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'condition')


@register(Hall)
class HallTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Stock)
class StockTranslationOptions(TranslationOptions):
    fields = ('title', 'description')