CREATE TABLE IF NOT EXISTS clients
(
client_id  serial PRIMARY KEY,
username varchar unique NOT null,
passwd varchar NOT null,
registration_date int not null
);

CREATE TABLE IF NOT EXISTS clients_groups
(
username varchar unique not null,
client_group varchar not null,

CONSTRAINT FK_clients_groups_clients FOREIGN KEY (username) REFERENCES clients(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS clients_friends
(
username varchar unique not null,
client_friend varchar not null,

CONSTRAINT FK_clients_friends_clients FOREIGN KEY (username) REFERENCES clients(username) ON DELETE CASCADE
);
