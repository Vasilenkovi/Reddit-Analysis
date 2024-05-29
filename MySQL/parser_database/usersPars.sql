CREATE USER 'reddit_client'@'%' IDENTIFIED BY 'f2O$$a6rA39Jcq]Y';
GRANT SELECT, INSERT, UPDATE, DELETE ON reddit_parsing.* TO 'reddit_client'@'%';
FLUSH PRIVILEGES;

CREATE USER 'parser_read'@'%' IDENTIFIED BY 'bgqld9(#_5]Y]86';
GRANT SELECT ON reddit_parsing.* TO 'parser_read'@'%';
FLUSH PRIVILEGES;

CREATE USER 'clusterizer'@'%' IDENTIFIED BY '5AP@32%/VtDo_J+9';
GRANT SELECT on reddit_parsing.* to 'clusterizer'@'%';
FLUSH PRIVILEGES;
