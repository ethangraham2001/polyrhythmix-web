from django.contrib import admin
from django.urls import path, include

from .views import GenerateMidiView, DownloadMidiView

urlpatterns = [
    path('generate', GenerateMidiView.as_view(), name='generate-midi'),
    path('download/<slug:midi_name>', DownloadMidiView.as_view()),
]