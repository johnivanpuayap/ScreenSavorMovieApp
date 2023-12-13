# Get Movie Rating

IN movie_id
DECLARE review_count INT;

-- Check if there are reviews
SELECT COUNT(*) INTO review_count
FROM review_review AS r
WHERE r.movie_id = movie_id;

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
IN p_title VARCHAR(100)
IN p_year_released INT
IN p_duration INT
IN p_description TEXT
IN p_director_first_name VARCHAR(100)
IN p_director_first_name VARCHAR(100)
IN p_cast_data JSON
IN p_genre JSON

BEGIN
    DECLARE movie_id INT;
    DECLARE director_id INT;
    
    SELECT id INTO director_id FROM movie_director WHERE first_name = p_director_first_name AND last_name = p_director_last_name LIMIT 1;

    -- If the director doesn't exist, insert them
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
	
    CALL AddMovieGenre(p_genre, movie_id);
    -- Insert cast data
    CALL InsertCastMembers(p_cast_data, movie_id);
END


# Add Movie Genre
IN genre JSON
IN movie_id
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE genre_count INT DEFAULT JSON_LENGTH(@p_genres, '$[*]');
    DECLARE genre_name VARCHAR(100)
    DECLARE genre_id DEFAULT 0
    DECLARE added BIT DEFAULT 0

    WHILE i < genre_count DO
        SET genre_name = JSON_UNQUOTE(JSON_EXTRACT(@p_genres, CONCAT('$[', i, ']')));

        SELECT id INTO genre_id FROM movie_genre WHERE name = genre_name;

        IF genre_id = 0
            INSERT INTO movie_genre (name)
            VALUES (genre_name)
            SET genre_id 
        ENDIF

        
        SELECT 1 INTO added
        FROM movie_movie_genre 
        WHERE movie_id = movie_id AND genre_id = @genre_id

        IF added = 0:
            -- Insert into movie_movie_genre
            INSERT INTO movie_movie_genre (movie_id, genre_id) VALUES (p_movie_id, genre_id)

        SET i = i + 1;
        SET genre_id = 0
        SET added = 0 
    END WHILE;
END

# Insert Cast Members

BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE cast_count INT DEFAULT JSON_LENGTH(p_cast_data, '$.cast_data');
    Declare cast_id INT;

    WHILE i < cast_count DO
        SET @first_name = JSON_UNQUOTE(JSON_EXTRACT(p_cast_data, CONCAT('$.cast_data[', i, '].first_name')));
        SET @last_name = JSON_UNQUOTE(JSON_EXTRACT(p_cast_data, CONCAT('$.cast_data[', i, '].last_name')));
        SET @role = JSON_UNQUOTE(JSON_EXTRACT(p_cast_data, CONCAT('$.cast_data[', i, '].role')));

        SELECT id INTO cast_id FROM movie_cast WHERE first_name = @first_name AND last_name = @last_name
        
        -- Check if the combination doesn't already exist
        IF cast_id IS NULL THEN
            INSERT INTO movie_cast (first_name, last_name)
            VALUES (@first_name, @last_name);
            SELECT "Created a New Cast" AS InsertCast
        END IF;

        -- Get the cast_id for the current cast member
        SET @cast_id = (SELECT id FROM movie_cast WHERE first_name = @first_name AND last_name = @last_name);

        -- Insert into MovieCast with role
        INSERT INTO movie_moviecast (movie_id, cast_id, role)
        SELECT movie_id, @cast_id, @role
        FROM dual
        WHERE NOT EXISTS (
            SELECT 1 
            FROM movie_moviecast 
            WHERE movie_id = movie_id AND cast_id = @cast_id AND role = @role
        );

        SET i = i + 1;
    END WHILE;
END


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



## Test
INSERT INTO movie_cast (first_name, last_name)
VALUES
    ('John', 'Doe'),
    ('Jane', 'Smith'),
    ('Alice', 'Johnson'),
    ('Bob', 'Williams'),
    ('Charlie', 'Brown');



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


       