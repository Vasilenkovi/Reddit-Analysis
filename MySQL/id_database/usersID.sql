CREATE USER 'job_id_client'@'localhost' IDENTIFIED BY '~X+qPJX<w:FKu$O';
GRANT SELECT, INSERT, UPDATE, DELETE ON reddit_job_id.* TO 'job_id_client'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'job_id_client'@'%' IDENTIFIED BY '~X+qPJX<w:FKu$O';
GRANT SELECT, INSERT, UPDATE, DELETE ON reddit_job_id.* TO 'job_id_client'@'%';
FLUSH PRIVILEGES;