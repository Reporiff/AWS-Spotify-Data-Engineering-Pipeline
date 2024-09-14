
-- List All Albums Released in a Specific Year (e.g., 2023)
SELECT album_id, album_name, album_release_date
FROM album_data
WHERE album_release_date LIKE '2023%';

-- Top 10 Most Popular Tracks
SELECT track_name, track_popularity, track_url
FROM track_data
ORDER BY track_popularity DESC
LIMIT 10;

-- Average Track Popularity by Artist
SELECT a.artist_name, AVG(t.track_popularity) AS avg_track_popularity
FROM track_data t
JOIN artist_data a ON t.artist_id = a.artist_id
GROUP BY a.artist_name
ORDER BY avg_track_popularity DESC;

-- Tracks Longer Than a Certain Duration (e.g., 4 minutes = 240,000 ms)
SELECT track_name, track_duration, track_url
FROM track_data
WHERE track_duration > 240000;  

-- List All Tracks with Artist and Album Information
SELECT t.track_name, a.artist_name, al.album_name, t.track_popularity
FROM track_data t
JOIN artist_data a ON t.artist_id = a.artist_id
JOIN album_data al ON t.album_id = al.album_id;

-- Top 10 Most Popular Tracks with Artist and Album
SELECT t.track_name, a.artist_name, al.album_name, t.track_popularity
FROM track_data t
JOIN artist_data a ON t.artist_id = a.artist_id
JOIN album_data al ON t.album_id = al.album_id
ORDER BY t.track_popularity DESC
LIMIT 10;

-- Find Artists with Tracks Having Low Popularity (e.g., Below 40)
SELECT a.artist_name, t.track_name, t.track_popularity
FROM artist_data a
JOIN track_data t ON a.artist_id = t.artist_id
WHERE t.track_popularity < 40
ORDER BY t.track_popularity ASC;

-- List All Tracks by a Specific Artist (e.g., "Adam Port")
SELECT t.track_name, t.track_url
FROM track_data t
JOIN artist_data a ON t.artist_id = a.artist_id
WHERE a.artist_name = 'Adam Port';

-- Top 5 Albums with the Most Tracks
SELECT album_name, album_total_tracks
FROM album_data
ORDER BY album_total_tracks DESC
LIMIT 5;

-- Track Duration Statistics (Average, Min, Max)
SELECT 
    AVG(track_duration) AS avg_duration,
    MIN(track_duration) AS min_duration,
    MAX(track_duration) AS max_duration
FROM track_data;