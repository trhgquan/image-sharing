DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS sharing;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  public_key TEXT NOT NULL,
  api_token TEXT,
  verify_token TEXT
);

CREATE TABLE images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  location TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE sharing (
  image_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  passphrase TEXT NOT NULL,
  FOREIGN KEY (image_id) REFERENCES images (id),
  FOREIGN KEY (user_id) REFERENCES user (id)
);
