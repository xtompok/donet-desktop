DROP TABLE IF EXISTS events;
CREATE TABLE events (
	id SERIAL PRIMARY KEY,
	sender INT,
	node INT,
	datetime TIMESTAMP DEFAULT now(),
	module VARCHAR(50),
	state VARCHAR(20),
	comment TEXT
);
CREATE INDEX ON events(sender);
CREATE INDEX ON events(node);
CREATE INDEX ON events(datetime);


DROP TABLE IF EXISTS state;
CREATE TABLE state (
	node INT PRIMARY KEY,
	name VARCHAR(30),
	type INT,
	changed INT,
	red INT,
	green INT,
	blue INT,
	white INT
);

