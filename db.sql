CREATE TABLE IF NOT EXISTS clients
(
client_id  serial PRIMARY KEY,
username varchar unique NOT null,
passwd varchar NOT null,
registration_date int not null,
friend_list text[],
room_list text[]
);
