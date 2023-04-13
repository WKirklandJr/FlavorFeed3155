-- Create user table (updated as new varibles are implemented)
CREATE TABLE IF NOT EXISTS users (
user_id SERIAL NOT NULL,
user_name VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL,
user_image IMAGE,
skill_level VARCHAR(255) NOT NULL,
PRIMARY KEY (user_id)
);