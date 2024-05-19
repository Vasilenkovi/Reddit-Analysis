CREATE USER 'reddit_test_client'@'localhost' IDENTIFIED BY 't9a!4Ic1G+X';
GRANT SELECT, INSERT, UPDATE, DELETE ON reddit_test_accounts.* TO 'reddit_test_client'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'reddit_test_client'@'%' IDENTIFIED BY 't9a!4Ic1G+X';
GRANT SELECT, INSERT, UPDATE, DELETE ON reddit_test_accounts.* TO 'reddit_test_client'@'%';
FLUSH PRIVILEGES;