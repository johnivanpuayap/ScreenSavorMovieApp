from django.forms import ModelForm
from django.forms import ModelForm
from django import forms
from .models import Movie, Genre, Director, Cast


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'year_released', 'duration', 'description', 'genre', 'director']

    title = forms.CharField(label='Enter Movie Title: ')
    year_released = forms.IntegerField(widget=forms.TextInput, label='Enter Year Released: ')
    duration = forms.IntegerField(widget=forms.TextInput, label='Enter Duration (in seconds):')
    description = forms.CharField(label='Enter Description: ')
    director = forms.ModelChoiceField(queryset=Director.objects.all(), label='Choose Director: ')
    genre = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Genre.objects.all(), label='Choose Genre/s: ')
    cast = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Cast.objects.all(), label='Choose Cast/s: ')