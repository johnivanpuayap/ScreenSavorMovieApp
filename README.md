# To do List
- [X] User Login and Registration
- [X] Admin Registration
- [X] Display All Movies
- [ ] Display a Movie
  - [X] Show Movie Information
  - [ ] Show Cast with their Roles
  - [ ] Show the Movie Reviews and Rating
  - [ ] Restructure the models to use id for better url routing
- [ ] View a Cast Member
  - [ ] Show the Cast Member Profile
  - [ ] Show Cast Member's Filmography
- [ ] View a Director
  - [ ] Show the Director's Information
  - [ ] Show the Director's Filmography
- [ ] View a Genre
  - [ ] Make Genres into Tags
  - [ ] Show movies all movies in the Genre
- [ ] Search Button
  - [ ] Add Button to Navigation Bar 
  - [ ] Add filters


# SQL Queries for the Movie Data

INSERT INTO movie_genre (name) VALUES ('Action'), ('Comedy'), ('Drama'), ('Sci-Fi'), ('Horror'), ('Romance'), ('Adventure'), ('Fantasy'), ('Mystery'), ('Thriller');

-- Insert data into the Director table
INSERT INTO movie_director (first_name, last_name) VALUES
    ('Christopher', 'Nolan'),
    ('Quentin', 'Tarantino'),
    ('Steven', 'Spielberg'),
    ('Greta', 'Gerwig'),
    ('Jordan', 'Peele'),
    ('Ava', 'DuVernay'),
    ('Martin', 'Scorsese'),
    ('Patty', 'Jenkins'),
    ('Denis', 'Villeneuve'),
    ('Taika', 'Waititi');

-- Insert data into the Cast table (Important cast only)
INSERT INTO movie_cast (first_name, last_name) VALUES
    ('Brad', 'Pitt'),
    ('Meryl', 'Streep'),
    ('Leonardo', 'DiCaprio'),
    ('Scarlett', 'Johansson'),
    ('Denzel', 'Washington'),
    ('Margot', 'Robbie'),
    ('Tom', 'Hanks'),
    ('Gal', 'Gadot'),
    ('Ryan', 'Reynolds'),
    ('Natalie', 'Portman');

-- Insert data into the Movie table
INSERT INTO movie_movie (title, year_released, duration, description, director_id) VALUES
    ('Inception', 2010, 148, 'A mind-bending heist movie directed by Christopher Nolan.', 1),
    ('Pulp Fiction', 1994, 154, 'A nonlinear crime drama directed by Quentin Tarantino.', 2),
    ('Jurassic Park', 1993, 127, 'An adventure film about cloned dinosaurs directed by Steven Spielberg.', 3),
    ('Little Women', 2019, 135, 'A classic novel adaptation directed by Greta Gerwig.', 4),
    ('Get Out', 2017, 104, 'A horror-thriller directed by Jordan Peele.', 5),
    ('Selma', 2014, 128, 'A historical drama about the civil rights movement directed by Ava DuVernay.', 6),
    ('Goodfellas', 1990, 146, 'A crime film directed by Martin Scorsese.', 7),
    ('Wonder Woman', 2017, 141, 'A superhero film directed by Patty Jenkins.', 8),
    ('Blade Runner 2049', 2017, 163, 'A sci-fi sequel directed by Denis Villeneuve.', 9),
    ('Thor: Ragnarok', 2017, 130, 'A Marvel superhero film directed by Taika Waititi.', 10);

-- Insert genre associations for movies
-- Adjust this based on the actual genres of each movie
INSERT INTO movie_movie_genre (movie_id, genre_id) VALUES
    (1, 4), (1, 9), (1, 10),
    (2, 3), (2, 10),
    (3, 1), (3, 7),
    (4, 3), (4, 6),
    (5, 3), (5, 10),
    (6, 3),
    (7, 3), (7, 10),
    (8, 1), (8, 10),
    (9, 4),
    (10, 1), (10, 7);

-- Insert cast associations for movies
-- Adjust this based on the actual cast of each movie
INSERT INTO movie_moviecast (movie_id, cast_id) VALUES
    (1, 1), (1, 2),
    (2, 2), (2, 6),
    (3, 3), (3, 7),
    (4, 4), (4, 5),
    (5, 5),
    (6, 6),
    (7, 3), (7, 7),
    (8, 8),
    (9, 9),
    (10, 10), (10, 9);