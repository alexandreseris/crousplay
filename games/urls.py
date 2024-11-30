from django.urls import path

import games.views

urlpatterns = [
    path("", games.views.search_page, name=games.views.search_page.__name__),
    path("result/", games.views.search_result, name=games.views.search_result.__name__),
    path("list/", games.views.list_all, name=games.views.list_all.__name__),
    path("about/", games.views.about, name=games.views.about.__name__),
]
