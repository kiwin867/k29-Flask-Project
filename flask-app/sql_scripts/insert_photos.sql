-- Insert sample photos into photos table with base64 encoded image data
-- Define photo data variables for all images in folder
\set frierenboss_photo `cat $BASE_DIR/frierenboss.b64`
\set frierenflowers_photo `cat $BASE_DIR/frierenflowers.b64`
\set frierensleep_photo `cat $BASE_DIR/frierensleep.b64`
\set frierensleep2_photo `cat $BASE_DIR/frierensleep2.b64`
\set gruvbox_photo `cat $BASE_DIR/gruvbox.b64`
\set luffygear5_photo `cat $BASE_DIR/luffygear5.b64`
\set road_photo `cat $BASE_DIR/road.b64`
\set subnautica_photo `cat $BASE_DIR/subnautica.b64`
\set teamoartist_photo `cat $BASE_DIR/teamoartist.b64`

-- Insert photos with base64 encoded image data (18 total photos)
INSERT INTO photos (albumid, phdata, phname, doc) VALUES
-- Album 1: Summer Vacation 2024
(1, decode(:'frierenboss_photo', 'base64'), 'Frieren - Boss Battle', '2024-06-15'),
(1, decode(:'frierenflowers_photo', 'base64'), 'Frieren - Flowers', '2024-06-15'),
(1, decode(:'frierensleep_photo', 'base64'), 'Frieren - Sleep Portrait', '2024-06-15'),

-- Album 2: Family Events
(2, decode(:'frierensleep2_photo', 'base64'), 'Frieren - Peaceful Sleep', '2024-06-17'),
(2, decode(:'luffygear5_photo', 'base64'), 'Luffy Gear 5 Transform', '2024-06-17'),

-- Album 3: Travel Photos
(3, decode(:'road_photo', 'base64'), 'Road to Adventure', '2024-06-18'),
(3, decode(:'gruvbox_photo', 'base64'), 'Gruvbox art souvenir', '2024-06-18'),

-- Album 4: Weekend Fun
(4, decode(:'subnautica_photo', 'base64'), 'Subnautica Leviathan', '2024-06-19'),
(4, decode(:'teamoartist_photo', 'base64'), 'Team Artist Collab', '2024-06-19');
