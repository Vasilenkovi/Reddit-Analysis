CREATE USER 'test_accounts_client'@'localhost' IDENTIFIED BY 't9a!4Ic1G+X';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER ON reddit_test_accounts.* TO 'test_accounts_client'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'test_accounts_client'@'%' IDENTIFIED BY 't9a!4Ic1G+X';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER ON reddit_test_accounts.* TO 'test_accounts_client'@'%';
FLUSH PRIVILEGES;