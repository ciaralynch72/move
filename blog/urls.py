from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('add_post', views.AddPostView.as_view(), name='add_post'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('category/<category>', views.CatListView.as_view(), name='cats'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('<slug:slug>/edit/', views.EditPostView.as_view(), name='edit_post'),
]
