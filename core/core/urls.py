from django.contrib import admin
from django.urls import path
from messenger import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path("api/register/", views.register),
    path("api/login/", views.login_view),
    path("api/me/", views.me),

    # ECC keys
    path("api/keys/upload/", views.upload_public_key),
    path("api/keys/<int:user_id>/", views.get_public_key),

    # Contacts
    path("api/search/", views.search_user),
    path("api/contacts/", views.list_contacts),
    path("api/contacts/add/", views.add_contact),

    # Messages
    path("api/messages/<int:user_id>/", views.message_history),
]