from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    return HttpResponse('<h1>Welcome to About Page</h1>')
def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})
def statistics_view(request):
    matplotlib.use('Agg')

    # Obtener todas las películas
    all_movies = Movie.objects.all()

    # Diccionarios para almacenar la cantidad de películas por año y por género
    movie_counts_by_year = {}
    movie_counts_by_genre = {}

    # Contar las películas por año y género
    for movie in all_movies:
        # Año
        year = movie.year if movie.year is not None else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1
        
        # Género
        genre = movie.genre if movie.genre is not None else "None"
        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1

    # Crear las gráficas
    bar_width = 0.5

    # Gráfica por año
    fig, ax = plt.subplots()
    years = list(movie_counts_by_year.keys())
    year_values = list(movie_counts_by_year.values())
    bar_positions_year = range(len(years))

    ax.bar(bar_positions_year, year_values, width=bar_width, align='center')
    ax.set_title('Movies per Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Movies')
    ax.set_xticks(bar_positions_year)
    ax.set_xticklabels(years, rotation=90)
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica de películas por año en base64
    buffer_year = io.BytesIO()
    plt.savefig(buffer_year, format='png')
    buffer_year.seek(0)
    plt.close()
    image_png_year = buffer_year.getvalue()
    buffer_year.close()
    graphic_year = base64.b64encode(image_png_year).decode('utf-8')

    # Gráfica por género
    fig, ax = plt.subplots()
    genres = list(movie_counts_by_genre.keys())
    genre_values = list(movie_counts_by_genre.values())
    bar_positions_genre = range(len(genres))

    ax.bar(bar_positions_genre, genre_values, width=bar_width, align='center')
    ax.set_title('Movies per Genre')
    ax.set_xlabel('Genre')
    ax.set_ylabel('Number of Movies')
    ax.set_xticks(bar_positions_genre)
    ax.set_xticklabels(genres, rotation=90)
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica de películas por género en base64
    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()
    image_png_genre = buffer_genre.getvalue()
    buffer_genre.close()
    graphic_genre = base64.b64encode(image_png_genre).decode('utf-8')

    # Renderizar la plantilla statistics.html con ambas gráficas
    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre
    })
