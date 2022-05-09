sql_dict = {
"actor" : '''
CREATE TABLE IF NOT EXISTS myschema.actor
(
	actor_id INTEGER,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45)  NOT NULL,
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
	PRIMARY KEY (actor_id)
);''',
"address" : '''
CREATE TABLE IF NOT EXISTS myschema.address
(
	address_id INTEGER,
    address VARCHAR(50) NOT NULL,
	address2 VARCHAR(50) NOT NULL,
	district VARCHAR(20) NOT NULL,
	city_id SMALLINT NOT NULL,
	postal_code VARCHAR(10) NOT NULL,
	phone VARCHAR(20) NOT NULL,
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
	PRIMARY KEY (address_id)
);''',
"category" : '''
CREATE TABLE IF NOT EXISTS myschema.category
(
	category_id INTEGER,
    name VARCHAR(25) NOT NULL,
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
	PRIMARY KEY (category_id)
);''',
"city" : '''
CREATE TABLE IF NOT EXISTS myschema.city
(
	city_id INTEGER,
    city VARCHAR(50) NOT NULL,
	country_id SMALLINT NOT NULL,
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
	PRIMARY KEY (city_id)	
);''',
"country" : '''
CREATE TABLE IF NOT EXISTS myschema.country
(
	country_id INTEGER,
    country VARCHAR(50) NOT NULL,
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
	PRIMARY KEY (country_id)
);''',
"customer" : '''
CREATE TABLE IF NOT EXISTS myschema.customer
(
	customer_id INTEGER,
	store_id SMALLINT NOT NULL,
	first_name VARCHAR(45) NOT NULL,
	last_name VARCHAR(45) NOT NULL,
	email VARCHAR(50),
	address_id SMALLINT NOT NULL,
	activebool BOOLEAN NOT NULL DEFAULT true,
	create_date DATE NOT NULL DEFAULT ('now'::text)::date,
	last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
	active INTEGER,
	PRIMARY KEY (customer_id)
);''',
"film" : '''
CREATE TABLE IF NOT EXISTS myschema.film
(
	film_id INTEGER,
	title VARCHAR(255) NOT NULL,
	description TEXT,
	release_year INTEGER,
    language_id SMALLINT NOT NULL,
    rental_duration SMALLINT NOT NULL DEFAULT 3,
    rental_rate DECIMAL(4,2) NOT NULL DEFAULT 4.99,
    length SMALLINT,
    replacement_cost DECIMAL(5,2) NOT NULL DEFAULT 19.99,
    rating VARCHAR(10),
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
	PRIMARY KEY (film_id)
);''',
"film_actor" : '''
CREATE TABLE IF NOT EXISTS myschema.film_actor
(
	actor_id SMALLINT NOT NULL,
    film_id SMALLINT NOT NULL,
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (actor_id, film_id)
);''',
"film_category" : '''
CREATE TABLE IF NOT EXISTS myschema.film_category
(
	film_id SMALLINT NOT NULL,
    category_id SMALLINT NOT NULL,
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (film_id, category_id)
);''',
"inventory" : '''
CREATE TABLE IF NOT EXISTS myschema.inventory
(
	inventory_id INTEGER NOT NULL,
    film_id SMALLINT NOT NULL,
    store_id SMALLINT NOT NULL,
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (inventory_id)
);''',
"language" : '''
CREATE TABLE IF NOT EXISTS myschema.language
(
	language_id INTEGER NOT NULL,
    name CHAR(20) NOT NULL,
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (language_id)
);''',
"payment" : '''
CREATE TABLE IF NOT EXISTS myschema.payment
(
	payment_id INTEGER NOT NULL,
    customer_id SMALLINT NOT NULL,
    staff_id SMALLINT NOT NULL,
    rental_id INTEGER NOT NULL,
    amount DECIMAL(5,2) NOT NULL,
    payment_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (payment_id)
);''',
"rental" : '''
CREATE TABLE IF NOT EXISTS myschema.rental
(
	rental_id INTEGER NOT NULL,
    rental_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    inventory_id INTEGER NOT NULL,
    customer_id SMALLINT NOT NULL,
    return_date TIMESTAMP WITHOUT TIME ZONE,
    staff_id SMALLINT NOT NULL,
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (rental_id)
);''',
"staff" : '''
CREATE TABLE IF NOT EXISTS myschema.staff
(
	staff_id INTEGER NOT NULL,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45) NOT NULL,
    address_id SMALLINT NOT NULL,
    email VARCHAR(50),
    store_id SMALLINT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT true,
    username VARCHAR(16) NOT NULL,
    password VARCHAR(40),
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (staff_id)
);''',
"store" : '''
CREATE TABLE IF NOT EXISTS myschema.store
(
	store_id INTEGER NOT NULL,
    manager_staff_id SMALLINT NOT NULL,
    address_id SMALLINT NOT NULL,
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (store_id)
);'''
}
