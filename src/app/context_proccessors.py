from app.models import (MainPageBanner, MainPage, AboutCinemaPage, 
    AdvertisePage, CafeBarPage, ChildrenRoomPage,
    CinemaContactsPage, MobileAppPage, VipHallPage, NewsAndStockBanner)


def load_settings(request):
    return {
        'main_page_baner': MainPageBanner.load(),
        'main_page': MainPage.load(),
        'about_cinema': AboutCinemaPage.load(),
        'advertise_page': AdvertisePage.load(),
        'cafe_bar_page': CafeBarPage.load(),
        'children_room_page': ChildrenRoomPage.load(),
        'mobile_app_page': MobileAppPage.load(),
        'vip_hall_page': VipHallPage.load(),
        'news_and_stock_banner': NewsAndStockBanner.load()
    }