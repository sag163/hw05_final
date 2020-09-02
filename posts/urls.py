from django.urls import path

from . import views

urlpatterns = [
    
    path("", views.index, name="index"),
    path("follow/", views.follow_index, name="follow_index"),
    path('group/<slug:slug>/', views.group_post, name='group'),
    path('new/', views.new_post, name='new_post'),
    path("<username>/<int:post_id>/", views.post_view, name="post"),
    path("<username>/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    path("<username>/<int:post_id>/delete/", views.post_delete, name="post_delete"),

    path("<username>/", views.profile, name="profile"),
    path("<username>/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("<username>/follow/", views.profile_follow, name="profile_follow"), 
    path("<username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
    path('<username>/<int:post_id>/addlike/', views.add_like, name='add_like'),
    path('<username>/<int:post_id>/adddislike/', views.add_dislike, name='add_dislike'),
    
]
