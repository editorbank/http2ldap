# http2ldap (HTTP to LDAP)

Адаптер для проксирования запросов из HTTP-запросов в LDAP каталог.

Принимет HTTP-запрос, где в теле запроса указаны логин и пароль пользователя.
С этими данными приложение пытается присоединиться к LDAP-каталогу.
В случае успеха возвращается код статуса 200 и в HTTP-заголовках информация из LDAP-а о пользователе.
Статусы 400 и более возвращается в других случаях и свидетельствуют о неудачной аутентификации пользователя.

Предназначается для аутентификации пользователя через LDAP-каталог.

Написано на Python-е, компилируется [py2bin](https://github.com/editorbank/py2bin)-ом в единый независимый от установок Python-а бинарный файл.
Бинарный файл заварачивается в Docker-образ на основе чистой Ubuntu.

## Требования к среде сборки

* ОС Linux семейства Ubuntu
* Установленный Docker или Podman

## Настройка

Среду поддержки образов можно указать в переменой `docker` указав в значении `podman` или `docker` в файлах `config.sh` и `py2bin.sh`.
Там же можно указать имя контейнера и образ.

## Сборка

Для (пере)сборки образа выполните команду:

```bash
./build.sh
```