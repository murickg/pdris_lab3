# pdris_lab3
Laboratory work on Docker

Скрипт ```start.sh``` собирает и запускает приложение.

Скрипт ```stop.sh``` останавливает все контейнеры, запущенные docker-compose, и удаляет их. 

Чтобы добавить данные ```name```, ```last_name``` в БД, пишем в терминал
```bash
 curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"name":"<name>", "last_name":"<last_name>"}' \
    http://127.0.0.1:8000/add_user
```

Чтобы посмотреть все данные в таблице пишем в терминал
```bash
curl --header "Content-Type: application/json" \
    --request GET \
    http://127.0.0.1:8000/get_users
```