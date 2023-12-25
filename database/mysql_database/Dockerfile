FROM mysql:latest

EXPOSE 3306

COPY my.cnf /etc/mysql/my.cnf

COPY init.sql /docker-entrypoint-initdb.d/

CMD ["mysqld"]