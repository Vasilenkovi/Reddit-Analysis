CREATE USER 'clusterizer_save'@'%' IDENTIFIED BY ';4U9i2efuVkfpTT#';
GRANT SELECT, INSERT, UPDATE on clusteringdb.* to 'clusterizer_save'@'%';
FLUSH PRIVILEGES;