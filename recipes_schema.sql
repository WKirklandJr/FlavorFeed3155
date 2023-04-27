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

-- Create recipes table (to be updated as variables are implemented)
CREATE TABLE IF NOT EXISTS recipes (
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
user_id INT NULL,
PRIMARY KEY (recipe_id),
FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- n:n relationship b/w users and recipes
CREATE TABLE IF NOT EXISTS bookmarks (
    user_id INT,
    recipe_id INT,
    PRIMARY KEY (user_id, recipe_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id)
);

-- table for tags
CREATE TABLE IF NOT EXISTS tags (
    tag_id SERIAL NOT NULL,
    tag VARCHAR(255) NOT NULL,
    PRIMARY KEY (tag_id)
);

-- n:n relationship b/w recipes and tags
CREATE TABLE IF NOT EXISTS recipe_tag (
    recipe_id INT,
    tag_id INT,
    PRIMARY KEY (recipe_id, tag_id),
    FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY(tag_id) REFERENCES tags(tag_id)
);

-- n:n relationship b/w users and recipes
CREATE TABLE IF NOT EXISTS user_recipe_comments (
    user_id INT,
    recipe_id INT,
    comment TEXT NOT NULL,
    PRIMARY KEY (user_id, recipe_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id)
);
