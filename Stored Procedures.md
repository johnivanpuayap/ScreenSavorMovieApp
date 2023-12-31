# AddMovie
IN `p_title` VARCHAR(100)
IN `p_year_released` INT
IN `p_duration` INT
IN `p_description` TEXT
IN `p_director_first_name` VARCHAR(100)
IN `p_director_last_name` VARCHAR(100)
IN `p_cast_data` JSON
IN `p_genre` JSON
BEGIN
    DECLARE movie_id INT;
    DECLARE director_id INT;
    
    -- Check if the movie already exists based on title, year released, and director
    SELECT id INTO movie_id
    FROM movie_movie
    WHERE title = p_title
      AND year_released = p_year_released
      AND director_id = (SELECT id FROM movie_director WHERE first_name = p_director_first_name AND last_name = p_director_last_name LIMIT 1)
    LIMIT 1;

    -- If the movie doesn't exist, insert it
    IF movie_id IS NULL THEN
        -- If the director doesn't exist, insert them
        SELECT id INTO director_id FROM movie_director WHERE first_name = p_director_first_name AND last_name = p_director_last_name LIMIT 1;

        IF director_id IS NULL THEN
            INSERT INTO movie_director (first_name, last_name) VALUES (p_director_first_name, p_director_last_name);
            SET director_id = LAST_INSERT_ID();
        END IF;

        -- Insert movie
        INSERT INTO movie_movie (title, year_released, duration, description, director_id)
        VALUES (
            p_title,
            p_year_released,
            p_duration,
            p_description,
            director_id
        );

        -- Get the movie ID
        SET movie_id = LAST_INSERT_ID();
        
        -- Add genre to the movie
        CALL AddMovieGenre(p_genre, movie_id);

        -- Insert cast data
        CALL AddMovieCast(p_cast_data, movie_id);
        
        SELECT "Created New Movie" AS outputmessage;
    ELSE
        SELECT "Movie Already Exists" AS outputmessage;
    END IF;
END


# AddMovieCast
IN `p_cast_data` JSON
IN `p_movie_id` INT
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE cast_count INT DEFAULT JSON_LENGTH(p_cast_data, '$.cast_data');
    DECLARE cast_id INT DEFAULT 0;
    DECLARE first_name VARCHAR(100);
    DECLARE last_name VARCHAR(100);
    DECLARE role VARCHAR(100);
    DECLARE added BIT DEFAULT 0;
    DECLARE movie_exists BIT DEFAULT 0;

    -- Check if the movie exists
    SELECT 1 INTO movie_exists FROM movie_movie WHERE id = p_movie_id LIMIT 1;

    IF movie_exists = 0 THEN
        SELECT "Movie does not exist" AS outputmessage;
    ELSE
        WHILE i < cast_count DO
            SET first_name = JSON_UNQUOTE(JSON_EXTRACT(p_cast_data, CONCAT('$.cast_data[', i, '].first_name')));
            SET last_name = JSON_UNQUOTE(JSON_EXTRACT(p_cast_data, CONCAT('$.cast_data[', i, '].last_name')));
            SET role = JSON_UNQUOTE(JSON_EXTRACT(p_cast_data, CONCAT('$.cast_data[', i, '].role')));

            SELECT id INTO cast_id FROM movie_cast as mc WHERE mc.first_name = first_name AND mc.last_name = last_name;

            -- Check if the combination doesn't already exist
            IF cast_id = 0 THEN
                INSERT INTO movie_cast (first_name, last_name)
                VALUES (first_name, last_name);
                SET cast_id = LAST_INSERT_ID();
                SELECT "Created New Cast Member" AS outputmessage;
            END IF;

            SELECT 1 INTO added
            FROM movie_role as mr
            WHERE mr.movie_id = p_movie_id AND mr.cast_id = cast_id AND mr.role = role;

            IF added = 0 THEN 
                -- Insert into MovieCast with role
                INSERT INTO movie_role (movie_id, cast_id, role)
                VALUES(p_movie_id, cast_id, role);
                SELECT "Added Cast Member to Movie" AS outputmessage;
            END IF;

            SET i = i + 1;
            SET cast_id = 0;
            SET added = 0;
        END WHILE;
    END IF;
END

# AddMovieGenre
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE genre_count INT;
    DECLARE genre_name VARCHAR(100);
    DECLARE genre_id INT DEFAULT 0;
    DECLARE added BIT DEFAULT 0;
    DECLARE movie_exists BIT DEFAULT 0;
    
    -- Check if the movie exists
    SELECT 1 INTO movie_exists FROM movie_movie WHERE id = p_movie_id LIMIT 1;
    
    IF movie_exists = 0 THEN
        SELECT "Movie does not exist" AS outputmessage;
    ELSE
        SET genre_count = JSON_LENGTH(p_genre, '$');
        
        WHILE i < genre_count DO
            SET genre_name = JSON_UNQUOTE(JSON_EXTRACT(p_genre, CONCAT('$[', i, ']')));
            
            -- Check if genre exists
            SELECT id INTO genre_id FROM movie_genre WHERE name = genre_name LIMIT 1;

            -- If genre does not exist, insert it
            IF genre_id = 0 THEN
                INSERT INTO movie_genre (name) VALUES (genre_name);
                SET genre_id = LAST_INSERT_ID();
                SELECT "Created New Genre" AS outputmessageone;
            END IF;

            -- Insert into movie_movie_genre if not exists
            SELECT 1 INTO added
            FROM movie_movie_genre as m
            WHERE m.movie_id = p_movie_id AND m.genre_id = genre_id;

            IF added = 0 THEN
                INSERT INTO movie_movie_genre (movie_id, genre_id)
                VALUES (p_movie_id, genre_id);
                SELECT "Added new genre to movie" AS outputmessagetwo;
            END IF;
            
            SET i = i+1;
            SET genre_id = 0;
            SET added = 0;
        END WHILE;
    END IF;
END

# DeleteMovie
IN `p_movie_id` INT
BEGIN
    DECLARE movie_exists BIT DEFAULT 0;

    -- Check if the movie exists
    SELECT 1 INTO movie_exists FROM movie_movie WHERE id = p_movie_id LIMIT 1;

    IF movie_exists = 1 THEN
        -- Delete from user_watchlist
        DELETE FROM user_watchlist WHERE movie_id = p_movie_id;

        -- Delete from user_user_liked_movies
        DELETE FROM user_like WHERE movie_id = p_movie_id;
		
        -- Delete from user_watchhistory
        DELETE FROM user_watchhistory WHERE movie_id = p_movie_id;
        
        -- Delete from movie_movie_genre
        DELETE FROM movie_movie_genre WHERE movie_id = p_movie_id;

        -- Delete from movie_moviecast
        DELETE FROM movie_role WHERE movie_id = p_movie_id;

        -- Delete the movie
        DELETE FROM movie_movie WHERE id = p_movie_id;
        
        SELECT "Movie Deleted Successfully" AS outputmessage;
    ELSE
        SELECT "Movie Not Found" AS outputmessage;
    END IF;
END

# DeleteOrphanedCastMembers
BEGIN
    -- Create a temporary table to store deleted cast members
    CREATE TEMPORARY TABLE deleted_cast_members AS
    SELECT * FROM movie_cast
    WHERE NOT EXISTS (
        SELECT 1
        FROM movie_role
        WHERE movie_cast.id = movie_role.cast_id
    );

    -- Delete orphaned cast members
    DELETE FROM movie_cast
    WHERE NOT EXISTS (
        SELECT 1
        FROM movie_role
        WHERE movie_cast.id = movie_role.cast_id
    );

    -- Select the deleted cast members from the temporary table
    SELECT * FROM deleted_cast_members;

    -- Drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS deleted_cast_members;
    
    SELECT "Orphaned Cast Members Deleted Successfully" AS outputmessage;
END

# GetAMovie
IN `p_movie_id` INT
BEGIN
    DECLARE collection_count INT;
    DECLARE review_count INT;
    DECLARE user_like_count INT;

    -- First result set: Movie details up to director last name
    SELECT
        m.title AS Title,
        m.year_released AS YearReleased,
        m.duration AS Duration,
        m.description AS Description,
        CONCAT(d.first_name, ' ', d.last_name) AS Director
    FROM
        movie_movie AS m
    INNER JOIN
        movie_director AS d ON m.director_id = d.id
    WHERE
        m.id = p_movie_id;

    -- Second result set: Genres
    SELECT
        g.name AS Genre
    FROM
        movie_movie_genre AS mg
    INNER JOIN
        movie_genre AS g ON mg.genre_id = g.id
    WHERE
        mg.movie_id = p_movie_id;

    -- Third result set: Cast details
    SELECT
        CONCAT(c.first_name, ' ', c.last_name) AS Cast,
        mr.role AS Role
    FROM
        movie_role AS mr
    INNER JOIN
        movie_cast AS c ON mr.cast_id = c.id
    WHERE
        mr.movie_id = p_movie_id;
        
    SELECT Count(*) INTO review_count
    FROM review_review
    WHERE review_review.movie_id = p_movie_id;

    -- Fourth result set: Movie Reviews and Average Rating if there are reviews
    IF review_count > 0 THEN
        SELECT
            r.user_id as Username,
            r.rating as Rating,
            r.description as Description
        FROM review_review AS r
        INNER JOIN user_user AS u ON r.user_id = u.username
        WHERE r.movie_id = p_movie_id;

        -- Fifth result set: Average Rating
        SELECT CAST(AVG(r.rating) AS INT) AS average_rating
        FROM review_review AS r
        WHERE r.movie_id = p_movie_id;
    ELSE
        -- If no reviews, return a message
        SELECT 'No reviews found.' AS Review;
        
        SELECT 0 AS Rating;
    END IF;
	
    -- Check if there are collections
    SELECT COUNT(*) INTO collection_count
    FROM collection_collection_movies AS ccm
    WHERE ccm.movie_id = p_movie_id;

    -- Sixth result set: Collections the movie belongs to
    IF collection_count > 0 THEN
        SELECT
            c.name AS CollectionName,
            u.username AS CollectionUser
        FROM
            collection_collection AS c
        INNER JOIN
            user_user AS u ON c.user_id = u.username
        INNER JOIN
            collection_collection_movies AS ccm ON c.id = ccm.collection_id
        WHERE
            ccm.movie_id = p_movie_id;
    ELSE
        -- If no collections, return a message
        SELECT 'No collections found.' AS CollectionMessage;
    END IF;

    -- Check if the user likes the movie
    SELECT COUNT(*) INTO user_like_count
    FROM user_like as ul
    WHERE ul.user_id = p_username AND ul.movie_id = p_movie_id;
    
     -- Seventh result set: Whether the user likes the movie
    SELECT CAST(user_like_count > 0 AS SIGNED) AS Liked;
END

# GetAllMovies
BEGIN
    SELECT 
        m.id AS id,
        m.title AS Title,
        m.year_released AS YearReleased,
        m.duration AS Duration,
        m.description AS Description,
        CONCAT(d.first_name, ' ', d.last_name) AS Director,
        IFNULL(AVG(r.rating), 0) AS AverageRating,
        GROUP_CONCAT(DISTINCT g.name) AS Genres
    FROM 
        movie_movie AS m
    INNER JOIN 
        movie_director AS d ON m.director_id = d.id
    LEFT JOIN 
        review_review AS r ON m.id = r.movie_id
    LEFT JOIN 
        movie_movie_genre AS mg ON m.id = mg.movie_id
    LEFT JOIN
        movie_genre AS g ON mg.genre_id = g.id
    GROUP BY 
        m.id
    ORDER BY
        m.title;
END

# LikeUnlikeMovie
IN `p_username` VARCHAR(32)
IN `p_movie_id` INT
BEGIN
    DECLARE liked INT;

    -- Check if the movie exists
    SELECT COUNT(*) INTO liked
    FROM user_like as ulm
    WHERE ulm.user_id = p_username AND ulm.movie_id = p_movie_id;

    IF liked = 0 THEN
        -- Add the movie to the liked movies
        INSERT INTO user_like(user_id, movie_id, date_liked) VALUES (p_username, p_movie_id, CURRENT_DATE());
        SELECT "Movie Liked Successfully" AS outputmessage;
    ELSE
        -- Remove the movie from the liked movies
        DELETE FROM user_like WHERE user_id = p_username AND movie_id = p_movie_id;
        SELECT "Movie Unliked Successfully" AS outputmessage;
    END IF;
END

# SearchMoviesByCast
IN `search_actor` VARCHAR(100)
BEGIN
    SELECT 
        m.id AS id,
        m.title AS Title,
        m.year_released AS YearReleased,
        m.duration AS Duration,
        m.description AS Description,
        CONCAT(d.first_name, ' ', d.last_name) AS Director,
        CAST(IFNULL(AVG(r.rating), 0) AS UNSIGNED) AS AverageRating,
        GROUP_CONCAT(DISTINCT g.name) AS Genres
    FROM 
        movie_movie AS m
    INNER JOIN 
        movie_director AS d ON m.director_id = d.id
    LEFT JOIN 
        review_review AS r ON m.id = r.movie_id
    LEFT JOIN 
        movie_movie_genre AS mg ON m.id = mg.movie_id
    LEFT JOIN
        movie_genre AS g ON mg.genre_id = g.id
    LEFT JOIN 
        movie_role AS mr ON m.id = mr.movie_id
    LEFT JOIN 
        movie_cast AS c ON mr.cast_id = c.id
    WHERE
        CONCAT(c.first_name, ' ', c.last_name) LIKE CONCAT('%', search_actor, '%')
    GROUP BY 
        m.id
    ORDER BY
        m.title;
END

# SearchMoviesByDirector
IN `search_director` VARCHAR(100)
BEGIN
	SELECT 
        m.id AS id,
        m.title AS Title,
        m.year_released AS YearReleased,
        m.duration AS Duration,
        m.description AS Description,
        CONCAT(d.first_name, ' ', d.last_name) AS Director,
        CAST(IFNULL(AVG(r.rating), 0) AS UNSIGNED) AS AverageRating,
        GROUP_CONCAT(DISTINCT g.name) AS Genres
    FROM 
        movie_movie AS m
    INNER JOIN 
        movie_director AS d ON m.director_id = d.id
    LEFT JOIN 
        review_review AS r ON m.id = r.movie_id
    LEFT JOIN 
        movie_movie_genre AS mg ON m.id = mg.movie_id
    LEFT JOIN
        movie_genre AS g ON mg.genre_id = g.id
    WHERE
        CONCAT(d.first_name, ' ', d.last_name) LIKE CONCAT('%', search_director, '%')
    GROUP BY 
        m.id
    ORDER BY
        m.title;
END


# SearchMoviesByTitle
IN `search_title` VARCHAR(100)
BEGIN
    SELECT 
        m.id AS id,
        m.title AS Title,
        m.year_released AS YearReleased,
        m.duration AS Duration,
        m.description AS Description,
        CONCAT(d.first_name, ' ', d.last_name) AS Director,
        CAST(IFNULL(AVG(r.rating), 0) AS UNSIGNED) AS AverageRating,
        GROUP_CONCAT(DISTINCT g.name) AS Genres
    FROM 
        movie_movie AS m
    INNER JOIN 
        movie_director AS d ON m.director_id = d.id
    LEFT JOIN 
        review_review AS r ON m.id = r.movie_id
    LEFT JOIN 
        movie_movie_genre AS mg ON m.id = mg.movie_id
    LEFT JOIN
        movie_genre AS g ON mg.genre_id = g.id
    WHERE
        m.title LIKE CONCAT('%', search_title, '%')
    GROUP BY 
        m.id
    ORDER BY
        m.title;
END


# Top10LikedMoviesAllTime
BEGIN
    SELECT m.title as movie_name, COUNT(ul.movie_id) as like_count
    FROM user_like ul
    JOIN movie_movie m ON ul.movie_id = m.id
    GROUP BY ul.movie_id
    ORDER BY like_count DESC
    LIMIT 10;
END


# Top10LikedMoviesToday
BEGIN
    DECLARE today DATE;
    SET today = CURDATE();

    SELECT m.title as movie_name, COUNT(ul.movie_id) as like_count
    FROM user_like ul
    JOIN movie_movie m ON ul.movie_id = m.id
    WHERE ul.date_liked = today
    GROUP BY ul.movie_id
    ORDER BY like_count DESC
    LIMIT 10;
END

# TopGenresForUser
IN `p_username` VARCHAR(32)
BEGIN
    SELECT g.name, COUNT(l.id) AS like_count
    FROM movie_genre g
    LEFT JOIN movie_movie_genre mmg ON mmg.genre_id = g.id
    LEFT JOIN movie_movie m ON m.id = mmg.movie_id
    LEFT JOIN user_like l ON l.movie_id = m.id
    WHERE l.user_id = p_user_id
    GROUP BY g.id
    ORDER BY like_count DESC
    LIMIT 5;
END