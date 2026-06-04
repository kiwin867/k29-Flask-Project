-- Insert sample photo tags
-- Associate photos with tags (many-to-many relationship)
-- Photo IDs: 1-8, Tag IDs: 1-10

INSERT INTO phototags (photoid, tagid) VALUES
(1, 5),   -- Beach Day -> beach
(1, 1),   -- Beach Day -> vacation
(2, 4),   -- Sunset -> sunset
(2, 5),   -- Sunset -> beach
(3, 2),   -- Family Dinner -> family
(3, 9),   -- Family Dinner -> fun
(4, 3),   -- Mountain View -> nature
(4, 6),   -- Mountain View -> mountains
(5, 3),   -- Forest Path -> nature
(5, 6),   -- Forest Path -> mountains
(6, 2),   -- Park Picnic -> family
(6, 9),   -- Park Picnic -> fun
(7, 7),   -- Downtown -> city
(8, 7),   -- Night Lights -> city
(8, 9);   -- Night Lights -> fun
