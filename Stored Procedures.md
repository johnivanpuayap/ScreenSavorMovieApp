# Like/Dislike A Movie
IN username
IN movie_id

BEGIN
    DECLARE liked INT;

    SELECT COUNT(*) INTO liked
    FROM user_user_liked_movies as ulm
    WHERE ulm.user_id = username AND ulm.movie_id = movie_id;

    IF liked = 0 THEN
    	INSERT INTO user_user_liked_movies(user_id, movie_id) VALUES (username, movie_id);
    ELSE
        DELETE FROM user_user_liked_movies WHERE user_id = user_id AND movie_id = movie_id;
    END IF;
END


# Add A Movie
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddMovie`(IN `p_title` VARCHAR(100), IN `p_year_released` INT, IN `p_duration` INT, IN `p_description` TEXT, IN `p_director_first_name` VARCHAR(100), IN `p_director_last_name` VARCHAR(100), IN `p_cast_data` JSON, IN `p_genre` JSON)
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
        CALL AddCast(p_cast_data, movie_id);
        
        SELECT "Created New Movie" AS outputmessage;
    ELSE
        SELECT "Movie Already Exists" AS outputmessage;
    END IF;
END$$
DELIMITER ;


# Add Movie Genre
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddMovieGenre`(IN `p_genre` JSON, IN `p_movie_id` INT)
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
END$$
DELIMITER ;

# Add Cast Members
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddCast`(IN `p_cast_data` JSON, IN `p_movie_id` INT)
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
            FROM movie_moviecast as mmc
            WHERE mmc.movie_id = p_movie_id AND mmc.cast_id = cast_id AND mmc.role = role;

            IF added = 0 THEN 
                -- Insert into MovieCast with role
                INSERT INTO movie_moviecast (movie_id, cast_id, role)
                VALUES(p_movie_id, cast_id, role);
                SELECT "Added Cast Member to Movie" AS outputmessage;
            END IF;

            SET i = i + 1;
            SET cast_id = 0;
            SET added = 0;
        END WHILE;
    END IF;
END$$
DELIMITER ;


# Delete Orphaned Cast Members
BEGIN
    -- Create a temporary table to store deleted cast members
    CREATE TEMPORARY TABLE deleted_cast_members AS
    SELECT * FROM movie_cast
    WHERE NOT EXISTS (
        SELECT 1
        FROM movie_moviecast
        WHERE movie_cast.id = movie_moviecast.cast_id
    );

    -- Delete orphaned cast members
    DELETE FROM movie_cast
    WHERE NOT EXISTS (
        SELECT 1
        FROM movie_moviecast
        WHERE movie_cast.id = movie_moviecast.cast_id
    );

    -- Select the deleted cast members from the temporary table
    SELECT * FROM deleted_cast_members;

    -- Drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS deleted_cast_members;
    
    SELECT "Orphaned Cast Members Deleted Successfully" AS outputmessage;
END


# Get All Movies

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetAllMovies`()
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
END$$
DELIMITER ;

# GetMovieDetails

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetMovieDetails`(IN `movie_id` INT, IN `username` VARCHAR(255))
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
        m.id = movie_id;

    -- Second result set: Genres
    SELECT
        g.name AS Genre
    FROM
        movie_movie_genre AS mg
    INNER JOIN
        movie_genre AS g ON mg.genre_id = g.id
    WHERE
        mg.movie_id = movie_id;

    -- Third result set: Cast details
    SELECT
        CONCAT(c.first_name, ' ', c.last_name) AS Cast,
        mc.role AS Role
    FROM
        movie_moviecast AS mc
    INNER JOIN
        movie_cast AS c ON mc.cast_id = c.id
    WHERE
        mc.movie_id = movie_id;

    -- Fourth result set: Movie Reviews and Average Rating if there are reviews
    IF review_count > 0 THEN
        SELECT
            r.user_id as Username,
            r.rating as Rating,
            r.description as Description
        FROM review_review AS r
        INNER JOIN user_user AS u ON r.user_id = u.username
        WHERE r.movie_id = movie_id;

        -- Fifth result set: Average Rating
        SELECT CAST(AVG(r.rating) AS INT) AS average_rating
        FROM review_review AS r
        WHERE r.movie_id = movie_id;
    ELSE
        -- If no reviews, return a message
        SELECT 'No reviews found.' AS Review;
        
        SELECT 0 AS Rating;
    END IF;
	
    -- Check if there are collections
    SELECT COUNT(*) INTO collection_count
    FROM collection_collection_movies AS ccm
    WHERE ccm.movie_id = movie_id;

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
            ccm.movie_id = movie_id;
    ELSE
        -- If no collections, return a message
        SELECT 'No collections found.' AS CollectionMessage;
    END IF;

    -- Check if the user likes the movie
    SELECT COUNT(*) INTO user_like_count
    FROM user_user_liked_movies as liked
    WHERE liked.user_id = username AND liked.movie_id = movie_id;
    
     -- Seventh result set: Whether the user likes the movie
    SELECT CAST(user_like_count > 0 AS SIGNED) AS Liked;
END$$
DELIMITER ;

# GetTopGenresForUser
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetTopGenresForUser`(IN `p_user_id` VARCHAR(32))
BEGIN
    SELECT g.name, COUNT(l.id) AS like_count
    FROM movie_genre g
    LEFT JOIN movie_movie_genre mmg ON mmg.genre_id = g.id
    LEFT JOIN movie_movie m ON m.id = mmg.movie_id
    LEFT JOIN user_like l ON l.movie_id = m.id
    WHERE l.user_id = p_user_id
    GROUP BY g.id
    ORDER BY like_count DESC
    LIMIT 5; -- Adjust the limit as needed
END$$
DELIMITER ;

# SearchMoviesByCast
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `SearchMoviesByCast`(IN `search_actor_name` VARCHAR(100))
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
        movie_moviecast AS mc ON m.id = mc.movie_id
    LEFT JOIN 
        movie_cast AS c ON mc.cast_id = c.id
    WHERE
        CONCAT(c.first_name, ' ', c.last_name) LIKE CONCAT('%', search_actor_name, '%')
    GROUP BY 
        m.id
    ORDER BY
        m.title;
END$$
DELIMITER ;

# SearchMoviesByDirector
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `SearchMoviesByDirector`(IN `search_director` VARCHAR(100))
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
        m.title$$
DELIMITER ;

# SearchMoviesByTitle
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `SearchMoviesbyTitle`(IN `search_title` VARCHAR(255))
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
END$$
DELIMITER ;

# Top10LikedMoviesToday
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `Top10LikedMoviesToday`()
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
END$$
DELIMITER ;

#Top10LikeMovesAllTime
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `Top10LikedMoviesAllTime`()
BEGIN
    SELECT m.title as movie_name, COUNT(ul.movie_id) as like_count
    FROM user_like ul
    JOIN movie_movie m ON ul.movie_id = m.id
    GROUP BY ul.movie_id
    ORDER BY like_count DESC
    LIMIT 10;
END$$
DELIMITER ;



       
