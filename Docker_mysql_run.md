docker run `
-itd `
--name mysql-wxf2 `
-p 3307:3306 `
-e MYSQL_ROOT_PASSWORD=123456 `
-e MYSQL_DATABASE=stocks `
-e MYSQL_USER=tushare `
-e MYSQL_PASSWORD=pass `
mysql `
--character-set-server=utf8mb4 `
--collation-server=utf8mb4_unicode_ci

docker exec -it mysql bash
mysql -u tushare -p
show databases;
show tables;
select * from "tables"