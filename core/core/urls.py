from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from messenger import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/register/", views.register),
    path("api/login/", views.login_view),
    path("api/me/", views.me),
    path("api/account/", views.delete_account),
    path("api/account/avatar/", views.change_avatar),
    path("api/avatars/", views.list_avatars),
    path("api/keys/upload/", views.upload_public_key),
    path("api/keys/<int:user_id>/", views.get_public_key),
    path("api/search/", views.search_user),
    path("api/contacts/", views.list_contacts),
    path("api/contacts/add/", views.add_contact),
    path("api/messages/<int:user_id>/", views.message_history),
] + static("/avatars/", document_root=str(settings.BASE_DIR.parent / "avatars"))
