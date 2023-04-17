-- Create recipes table (to be updated as variables are implemented)
CREATE TABLE IF NOT EXISTS recipe (
recipe_id SERIAL NOT NULL,
title VARCHAR(255) NOT NULL,
is_vegan BOOL NOT NULL DEFAULT FALSE,
ingredients VARCHAR(255) NOT NULL,
equipment VARCHAR(255) NOT NULL,
difficulty VARCHAR(255) NOT NULL,
text TEXT NOT NULL,
PRIMARY KEY (recipe_id)
);

-- Create user table (updated as new varibles are implemented)
CREATE TABLE IF NOT EXISTS users (
user_id SERIAL NOT NULL,
user_name VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL,
user_image BYTEA,
skill_level VARCHAR(255) NOT NULL,
PRIMARY KEY (user_id)
);

