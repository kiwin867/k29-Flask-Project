-- Insert sample users into flusers table
-- Note: photo column uses base64 encoded image data stored in variables

-- Define photo data variables
\set frieren_photo_data `cat /home/kiwin867/vscode/k29-Flask-Project/flask-app/static/frieren.b64`
\set serie_photo_data `cat /home/kiwin867/vscode/k29-Flask-Project/flask-app/static/serie.b64`
\set musashi_photo_data `cat /home/kiwin867/vscode/k29-Flask-Project/flask-app/static/asuka.b64`
\set asuka_photo_data `cat /home/kiwin867/vscode/k29-Flask-Project/flask-app/static/asuka.b64`
\set shin_photo_data `cat /home/kiwin867/vscode/k29-Flask-Project/flask-app/static/dorohedoroshin.b64`
\set coco_photo_data `cat /home/kiwin867/vscode/k29-Flask-Project/flask-app/static/coco.b64`
\set agott_photo_data `cat /home/kiwin867/vscode/k29-Flask-Project/flask-app/static/Agott.b64`
\set richeh_photo_data `cat /home/kiwin867/vscode/k29-Flask-Project/flask-app/static/Richeh.b64`
\set tetia_photo_data `cat /home/kiwin867/vscode/k29-Flask-Project/flask-app/static/Tetia.b64`
\set qifrey_photo_data `cat /home/kiwin867/vscode/k29-Flask-Project/flask-app/static/qifrey.b64`
\set olly_photo_data `cat /home/kiwin867/vscode/k29-Flask-Project/flask-app/static/Olruggio.b64`
\set yachio_photo_data `cat /home/kiwin867/vscode/k29-Flask-Project/flask-app/static/yachio.b64`
\set kaguya_photo_data `cat /home/kiwin867/vscode/k29-Flask-Project/flask-app/static/kaguya.b64`

-- Insert users with their photos
INSERT INTO flusers (fname, lname, email, pass, photo, dob) VALUES
('Frieren', 'The Slayer', 'frieren@journey.com', 'pass123', decode(:'frieren_photo_data', 'base64'), '1000-01-01'),
('Serie', 'The Master', 'serie@journey.com', 'pass456', decode(:'serie_photo_data', 'base64'), '1000-01-01'),
('Musashi', 'Miyamoto', 'musashi@vagabond.com', 'pass789', decode(:'musashi_photo_data', 'base64'), '1583-03-12'),
('Asuka', 'Langley Souryuu', 'asuka@evangelion.com', 'passabc', decode(:'asuka_photo_data', 'base64'), '2001-12-04'),
('Shin', 'Cleaner', 'shin@dorohendoro.com', 'passdef', decode(:'shin_photo_data', 'base64'), '1991-09-09'),
('Coco', 'Magic Lover', 'coco@brushbuddy.com', 'passdef', decode(:'coco_photo_data', 'base64'), '1990-05-20'),
('Agott', 'Arklaum', 'agott@brushbuddy.com', 'passdef', decode(:'agott_photo_data', 'base64'), '1989-07-15'),
('Richeh', 'Richehlette', 'richeh@brushbuddy.com', 'passdef', decode(:'richeh_photo_data', 'base64'), '1992-02-28'),
('Tetia', 'Tetianna', 'tetia@brushbuddy.com', 'passdef', decode(:'tetia_photo_data', 'base64'), '1993-11-10'),
('Qifrey', 'Big Q', 'qifrey@brushbuddy.com', 'passdef', decode(:'qifrey_photo_data', 'base64'), '1985-04-05'),
('Olly', 'Olruggio', 'olly@brushbuddy.com', 'passdef', decode(:'olly_photo_data', 'base64'), '1991-08-22'),
('Yachio', 'Big Princess', 'yachio@moon.com', 'passdef', decode(:'yachio_photo_data', 'base64'), '1990-10-15'),
('Kaguya', 'Small Princess', 'kaguya@moon.com', 'passdef', decode(:'kaguya_photo_data', 'base64'), '1995-06-30');
