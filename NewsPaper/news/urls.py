from django.urls import path
from .views import PostList, PostDetail, PostListFiltered, PostCreateView, PostUpdateView, PostDeleteView, \
    BaseRegisterView, LoginViewPage, PersonalPage, make_author, PostCategoryView, subscribe_to_category, \
    unsubscribe_from_category

urlpatterns = [
    # news
    path('news/', PostList.as_view(), name='post_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/add/', PostCreateView.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('news/search/', PostListFiltered.as_view()),

    # login
    path('login/', LoginViewPage.as_view(), name='login'),
    path('signup/', BaseRegisterView.as_view(), name='signup'),
    path('upgrade/', make_author, name = 'upgrade'),
    path('personal/', PersonalPage.as_view(), name='personal'),

    path('category/<int:pk>', PostCategoryView.as_view(), name='category'),
    path('subscribe/<int:pk>', subscribe_to_category, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe_from_category, name='unsubscribe'),
    
]