$ docker-compose exec web aerich init -t app.db.TORTOISE_ORM
$ docker-compose exec web aerich init-db
$ docker-compose exec web-db psql -U postgres

psql (14.1)
Type "help" for help.

postgres=# \c web_dev
You are now connected to database "web_dev" as user "postgres".

web_dev=# \dt
            List of relations
 Schema |    Name     | Type  |  Owner
--------+-------------+-------+----------
 public | aerich      | table | postgres
 public | textsummary | table | postgres
(2 rows)

web_dev=# \q

# 修改docker镜像源
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "features": {
    "buildkit": true
  },
  "registry-mirrors": [
    "https://reg-mirror.qiniu.com/"
  ]
}