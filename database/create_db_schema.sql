CREATE DATABASE worldfy;

-- create extension to use UUID datatype
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- create events table
CREATE TABLE events (
    "event_id" uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    "event_name" VARCHAR(50) NOT NULL UNIQUE,
    "date_start" TIMESTAMP NOT NULL,
    "date_end" TIMESTAMP NOT NULL,
    "is_public" BOOLEAN NOT NULL,
    "is_outdoor" BOOLEAN DEFAULT NULL,
    "address" INT NOT NULL,
    "description" TEXT NOT NULL,
    "participants_limit" VARCHAR(20) DEFAULT NULL,
    "age_limit" VARCHAR(5) NOT NULL,
    "place" BOOLEAN DEFAULT NULL
);

-- create event_type
CREATE TABLE event_type (
    "type_id" TYPE INT NOT NULL,
    "name" TYPE VARCHAR(50) NOT NULL
)

-- create event_type_bridge
CREATE TABLE event_type_bridge (
    "event_id" TYPE UUID DEFAULT uuid_generate_v4 () NOT NULL,
    "type_id" TYPE VARCHAR(50) NOT NULL,
    "details" TYPE VARCHAR(50)
)

-- create user table
CREATE TABLE user (
    "user_id" TYPE UUID DEFAULT uuid_generate_v4 () PRIMARY KEY,
    "email" TYPE VARCHAR(50) NOT NULL UNIQUE,
    "password" TYPE VARCHAR(100) NOT NULL,
    "description" TYPE TEXT DEFAULT NULL,
    "photo" TYPE varchar(250) DEFAULT NULL,
    "private_data" TYPE UUID,
    "organization_data" TYPE UUID
)

-- create private_data table
CREATE TABLE private_data (
    "id" TYPE UUID DEFAULT uuid_generate_v4 () PRIMARY KEY,
    "username" TYPE VARCHAR(50) NOT NULL UNIQUE,
    "name" TYPE VARCHAR(30) NOT NULL,
    "surname" TYPE VARCHAR(40) NOT NULL,
    "birthday" TYPE TIMESTAMP NOT NULL
)

-- create organization_data table
CREATE TABLE organization_data (
    "id" TYPE UUID DEFAULT uuid_generate_v4 () PRIMARY KEY,
    "name" TYPE VARCHAR(50) NOT NULL UNIQUE,
    "address" TYPE INT,
    "phone_number" TYPE VARCHAR(12) NOT NULL,
    "type" TYPE VARCHAR(20)
)

-- create event_user table
CREATE TABLE event_user (
    "user_id" TYPE INT PRIMARY KEY,
    "event_id" TYPE VARCHAR(50) NOT NULL UNIQUE,
    "role" TYPE INT NOT NULL
)

-- create event_roles table
CREATE TABLE event_roles(
    "role_id" TYPE int PRIMARY KEY,
    "name" TYPE VARCHAR(50) NOT NULL,
    "description" TYPE TEXT NOT NULL
)

-- create media table
CREATE TABLE media(
    "id" TYPE int PRIMARY KEY,
    "event_id" TYPE UUID NOT NULL,
    "link" TYPE VARCHAR(250) NOT NULL
    "type" TYPE INT NOT NULL
)

-- create media_types table
CREATE TABLE media_types(
    "id" TYPE INT PRIMARY KEY,
    "name" TYPE varchar(30) NOT NULL,
    "icon" TYPE VARCHAR(250) NOT NULL
)

-- create places table
CREATE TABLE places(
    "id" TYPE INT PRIMARY KEY,
    "name" TYPE varchar(30) NOT NULL,
    "page_link" TYPE VARCHAR(250),
    "address" TYPE INT NOT NULL
)

-- create addresses table
CREATE TABLE addresses(
    "id" TYPE INT PRIMARY KEY,
    "country" TYPE varchar(40) NOT NULL,
    "city" TYPE VARCHAR(40) NOT NULL,
    "street" TYPE VARCHAR(50) NOT NULL,
    "street_number" TYPE VARCHAR(5) NOT NULL,
    "local_number" TYPE INT,
    "latitude" TYPE FLOAT NOT NULL,
    "longitude" TYPE FLOAT NOT NULL
)



INSERT INTO events (
    event_name,
    date_start,
    date_end,
    is_public,
    description,
    address,
    age_limit
)
VALUES
    (
        'concert1',
        TO_TIMESTAMP('2017-03-31 12:00:00', 'YYYY-MM-DD HH:MI:SS'),
        TO_TIMESTAMP('2017-04-01 2:30:00', 'YYYY-MM-DD HH:MI:SS'),
        TRUE,
        'coool music, letss go',
        1, 
        '18+'

    );

    INSERT INTO events("concert1","TO_TIMESTAMP("2017-03
-31 9:30:20", "YYYY-MM-DD HH:MI:SS"), TO_TIMESTAMP("2017-04
-01 2:30:00","YYYY-MM-DD HH:MI:SS"), True, False, 1, "good music, letssgo", "200","18+"
)