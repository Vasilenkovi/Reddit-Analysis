FROM mysql:8.0.33
COPY ./clustering_db/ /docker-entrypoint-initdb.d/
COPY ./id_database/ /docker-entrypoint-initdb.d/
COPY ./parser_database/ /docker-entrypoint-initdb.d/
COPY ./user_database/ /docker-entrypoint-initdb.d/
ENV MYSQL_DATABASE clusteringdb
ENV MYSQL_DATABASE reddit_job_id
ENV MYSQL_DATABASE reddit_parsing
ENV MYSQL_DATABASE reddit_test_accounts
ENV MYSQL_ROOT_PASSWORD root
COPY my.cnf /etc/