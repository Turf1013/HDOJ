-- Schema for hdu question application.

-- problem describe the problems info
create table problem (
	id	INTEGER primary key,
	title	TEXT,
	ratio	REAL,
	Accepted	INTEGER,
	Submissions	INTEGER,
	solved	INTEGER
);
