from re import T
from modeltranslation.translator import register, TranslationOptions
from app.models import (Movie, Cinema, Hall, News, Stock, 
    CafeBarPage, VipHallPage, AboutCinemaPage, AdvertisePage, 
    ChildrenRoomPage, MobileAppPage)


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


@register(CafeBarPage)
class CafeBarPageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(VipHallPage)
class VipHallPageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(AboutCinemaPage)
class AboutCinemaPageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(AdvertisePage)
class AdvertisePageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(ChildrenRoomPage)
class ChildrenRoomPageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(MobileAppPage)
class MobileAppPageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')