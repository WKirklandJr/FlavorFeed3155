-- Create recipes table (to be updated as variables are implemented)
CREATE TABLE IF NOT EXISTS recipe (
recipe_id SERIAL NOT NULL,
title VARCHAR(255) NOT NULL,
is_vegan BOOL  DEFAULT FALSE NOT NULL,
ingredients VARCHAR(255) NOT NULL,
equipment VARCHAR(255) NOT NULL,
duration SMALLINT NOT NULL,
difficulty VARCHAR(255) NOT NULL,
instructions TEXT NOT NULL,
recipe_image VARCHAR(255) NOT NULL,
date_posted TIMESTAMP NOT NULL,
PRIMARY KEY (recipe_id)
);

-- Create user table (updated as new varibles are implemented)
CREATE TABLE IF NOT EXISTS users (
user_id SERIAL NOT NULL,
email VARCHAR(255) NOT NULL,
username VARCHAR(255) NOT NULL,
"password" VARCHAR(255) NOT NULL,
profile_picture VARCHAR(255) NOT NULL,
skill VARCHAR(255) NOT NULL,
social VARCHAR(255) NOT NULL,
about TEXT NOT NULL,
PRIMARY KEY (user_id)
);
