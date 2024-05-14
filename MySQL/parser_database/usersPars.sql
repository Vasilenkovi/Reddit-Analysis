CREATE USER 'reddit_client'@'localhost' IDENTIFIED BY 'Reddit_Yarik_1984!';
GRANT SELECT, INSERT, UPDATE, DELETE ON reddit_parsing.* TO 'reddit_client'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'parser_read'@'localhost' IDENTIFIED BY 'bgqld9(#_5]Y]86';
GRANT SELECT ON reddit_parsing.* TO 'parser_read'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'clusterizer'@'localhost' IDENTIFIED BY 'Clusterizing1984!';
GRANT SELECT on reddit_parsing.* to 'clusterizer'@'localhost';
FLUSH PRIVILEGES;

CREATE DATABASE reddit_test_accounts;
CREATE USER 'test_accounts_client'@'localhost' IDENTIFIED BY 't9a!4Ic1G+X';
GRANT ALL PRIVILEGES on reddit_test_accounts.* to 'test_accounts_client'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'test_accounts_client'@'%' IDENTIFIED BY 't9a!4Ic1G+X';
GRANT ALL PRIVILEGES on reddit_test_accounts.* to 'test_accounts_client'@'%';
FLUSH PRIVILEGES;


