from django.urls import  path
from . import views

urlpatterns=[
    path("notes/",views.NoteListCreate.as_view(),name="note-list"),
    path("notes/<int:pk>/summary/",views.NoteSummaryView.as_view(),name="note-summary"),
    path("notes/delete/<int:pk>/",views.NoteDelete.as_view(),name="delete-note")

]