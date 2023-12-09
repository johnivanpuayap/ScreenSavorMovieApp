from django.core.management import setup_environ
from Room8_ScreenSavor import settings

setup_environ(settings)

from movie.models import Genre, Director, Cast, Movie, MovieCast

def populate_data():
    genres = [
        'Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror',
        'Romance', 'Adventure', 'Thriller', 'Animation', 'Fantasy',
        'Biography', 'Crime', 'History', 'Mystery', 'War',
    ]

    for genre_name in genres:
        Genre.objects.create(name=genre_name)
    
    # Add directors
    christopher_nolan = Director.objects.create(first_name='Christopher', last_name='Nolan')
    quentin_tarantino = Director.objects.create(first_name='Quentin', last_name='Tarantino')
    steven_spielberg = Director.objects.create(first_name='Steven', last_name='Spielberg')
    frank_darabont = Director.objects.create(first_name='Frank', last_name='Darabont')
    # Add more directors as needed

    # Add casts
    tom_hanks = Cast.objects.create(first_name='Tom', last_name='Hanks')
    leonardo_dicaprio = Cast.objects.create(first_name='Leonardo', last_name='DiCaprio')
    ellen_page = Cast.objects.create(first_name='Ellen', last_name='Page')
    joseph_gordon_levitt = Cast.objects.create(first_name='Joseph', last_name='Gordon-Levitt')
    jamie_foxx = Cast.objects.create(first_name='Jamie', last_name='Foxx')
    christoph_waltz = Cast.objects.create(first_name='Christoph', last_name='Waltz')
    john_travolta = Cast.objects.create(first_name='John', last_name='Travolta')
    uma_thurman = Cast.objects.create(first_name='Uma', last_name='Thurman')
    samuel_l_jackson = Cast.objects.create(first_name='Samuel L.', last_name='Jackson')
    morgan_freeman = Cast.objects.create(first_name='Morgan', last_name='Freeman')
    tim_robbins = Cast.objects.create(first_name='Tim', last_name='Robbins')
    bob_gunton = Cast.objects.create(first_name='Bob', last_name='Gunton')

    # Add movies
    inception = Movie.objects.create(
        title='Inception',
        year_released=2010,
        duration=148,
        description='A mind-bending thriller.',
        director=christopher_nolan,
    )
    inception.genre.add(Genre.objects.get(name='Action'), Genre.objects.get(name='Drama'))

    MovieCast.objects.create(movie=inception, cast=leonardo_dicaprio, role='Cobb')
    MovieCast.objects.create(movie=inception, cast=ellen_page, role='Ariadne')
    MovieCast.objects.create(movie=inception, cast=joseph_gordon_levitt, role='Arthur')

    django_unchained = Movie.objects.create(
        title='Django Unchained',
        year_released=2012,
        duration=165,
        description='A story of revenge.',
        genre=Genre.objects.get(name='Action'),
        director=quentin_tarantino
    )
    django_unchained.genre.add(Genre.objects.get(name='Drama'))
    
    MovieCast.objects.create(movie=django_unchained, cast=leonardo_dicaprio, role='Calvin Candie')
    MovieCast.objects.create(movie=django_unchained, cast=jamie_foxx, role='Django')
    MovieCast.objects.create(movie=django_unchained, cast=christoph_waltz, role='Dr. King Schultz')

    catch_me_if_you_can = Movie.objects.create(
        title='Catch Me If You Can',
        year_released=2002,
        duration=141,
        description='A true story about Frank Abagnale Jr.',
        director=steven_spielberg
    )
    catch_me_if_you_can.genre.add(Genre.objects.get(name='Drama'), Genre.objects.get(name='Crime'))

    MovieCast.objects.create(movie=catch_me_if_you_can, cast=leonardo_dicaprio, role='Frank Abagnale Jr.')
    MovieCast.objects.create(movie=catch_me_if_you_can, cast=tom_hanks, role='Carl Hanratty')

    pulp_fiction = Movie.objects.create(
        title='Pulp Fiction',
        year_released=1994,
        duration=154,
        description="The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        director=quentin_tarantino
    )
    pulp_fiction.genre.add(Genre.objects.get(name='Crime'), Genre.objects.get(name='Drama'))
    
    MovieCast.objects.create(movie=pulp_fiction, cast=john_travolta, role='Vincent Vega')
    MovieCast.objects.create(movie=pulp_fiction, cast=uma_thurman, role='Mia Wallace')
    MovieCast.objects.create(movie=pulp_fiction, cast=samuel_l_jackson, role='Jules Winnfield')

    shawshank_redemption = Movie.objects.create(
        title='The Shawshank Redemption',
        year_released=1994,
        duration=142,
        description="Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.",
        director=frank_darabont
    )
    shawshank_redemption.genre.add(Genre.objects.get(name='Drama'))

    MovieCast.objects.create(movie=shawshank_redemption, cast=tim_robbins, role='Andy Dufresne')
    MovieCast.objects.create(movie=shawshank_redemption, cast=morgan_freeman, role='Ellis Boyd Redding')
    MovieCast.objects.create(movie=shawshank_redemption, cast=bob_gunton, role='Warden Norton')

    david_fincher = Director.objects.create(first_name='David', last_name='Fincher')
    brad_pitt = Cast.objects.create(first_name='Brad', last_name='Pitt')
    edward_norton = Cast.objects.create(first_name='Edward', last_name='Norton')

    fight_club = Movie.objects.create(
        title='Fight Club',
        year_released=1999,
        duration=139,
        description="An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.",
        director=david_fincher
    )
    fight_club.genre.add(Genre.objects.get(name='Drama'))

    MovieCast.objects.create(movie=fight_club, cast=brad_pitt, role='Tyler Durden')
    MovieCast.objects.create(movie=fight_club, cast=edward_norton, role='The Narrator')

    matthew_mcconaughey = Cast.objects.create(first_name='Matthew', last_name='McConaughey')
    anne_hathaway = Cast.objects.create(first_name='Anne', last_name='Hathaway')

    interstellar = Movie.objects.create(
        title='Interstellar',
        year_released=2014,
        duration=169,
        description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        director=christopher_nolan
    )
    interstellar.genre.add(Genre.objects.get(name='Sci-Fi'), Genre.objects.get(name='Adventure'), Genre.objects.get(name='Drama'))

    MovieCast.objects.create(movie=interstellar, cast=matthew_mcconaughey, role='Cooper')
    MovieCast.objects.create(movie=interstellar, cast=anne_hathaway, role='Brand')

    james_cameron = Director.objects.create(first_name='James', last_name='Cameron')

    kate_winslet = Cast.objects.create(first_name='Kate', last_name='Winslet')

    titanic = Movie.objects.create(
    
        title='Titanic',
        year_released=1997,
        duration=194,
        description="A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
        director=james_cameron
    )
    titanic.genre.add(Genre.objects.get(name='Romance'), Genre.objects.get(name='Drama'))

    MovieCast.objects.create(movie=titanic, cast=kate_winslet, role='Rose DeWitt Bukater')
    MovieCast.objects.create(movie=titanic, cast=leonardo_dicaprio, role='Jack Dawson') 

    cilian_murphy = Cast.objects.create(first_name='Cilian', last_name='Murphy')
    emily_blunt = Cast.objects.create(first_name='Emily', last_name='Blunt')
    matt_damon = Cast.objects.create(first_name='Matt', last_name='Damon')

    oppenheimer = Movie.objects.create(
        title='Oppenheimer',
        year_released=2023,
        duration=180,
        description="The story of American scientist, J. Robert Oppenheimer, and his role in the development of the atomic bomb.",
        director=christopher_nolan
    )
    oppenheimer.genre.add(Genre.objects.get(name='Drama'), Genre.objects.get(name='Biography'), Genre.objects.get(name='History'))
    
    MovieCast.objects.create(movie=oppenheimer, cast=cilian_murphy, role='J. Robert Oppenheimer')
    MovieCast.objects.create(movie=oppenheimer, cast=emily_blunt, role='Kitty Oppenheimer')
    MovieCast.objects.create(movie=oppenheimer, cast=matt_damon, role='Leslie Groves')

    dark_knight_rises = Movie.objects.create(
        title='The Dark Knight Rises',
        year_released=2012,
        duration=164,
        description="Eight years after the Joker's reign of chaos, Batman is coerced out of exile with the assistance of the mysterious Selina Kyle in order to defend Gotham City from the vicious guerrilla terrorist Bane.",
        director=christopher_nolan
    )
    dark_knight_rises.genre.add(Genre.objects.get(name='Action'), Genre.objects.get(name='Drama'), Genre.objects.get(name='Thriller'))

    christian_bale = Cast.objects.create(first_name='Christian', last_name='Bale')
    tom_hardy = Cast.objects.create(first_name='Tom', last_name='Hardy')

    MovieCast.objects.create(movie=dark_knight_rises, cast=christian_bale, role='Bruce Wayne')
    MovieCast.objects.create(movie=dark_knight_rises, cast=tom_hardy, role='Bane')
    MovieCast.objects.create(movie=dark_knight_rises, cast=anne_hathaway, role='Selina')

if __name__ == "__main__":
    populate_data()