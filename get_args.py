import argparse
from ldap_query import check_form

def get_args():
  parser = argparse.ArgumentParser(add_help=False,
    prog="http2ldap",
    description="""
      Сервер аутентификации через подключение к LDAP-серверу с параметрами пользователя переданных в HTTP-запросе.
      """,
    epilog="""
      * Набор опций для тестирования подключения к LDAP серверу из Apache Directory Studio \
        запущеному с настройками по умолчанию:
      --test-query-string "USERNAME=admin&PASSWORD=secret"
      --ldap-server "localhost:10389" --ldap-user "uid={USERNAME},ou=system"
      --search-base "ou=system" --search-filter "(uid={USERNAME})"
      """
  )
  parser.add_argument("-h","--help", help = "Вывести это  собщение и завершить работу", action="help")

  http_options = parser.add_argument_group("Параметры HTTP")
  http_options.add_argument("--http-interface", default="127.0.0.1",
                            help = "Сетевой интерфей для HTTP-запросов (по умолчанию: \"%(default)s\")")
  http_options.add_argument("--http-port", default="8080", type=int,
                            help = "Сетевой порт для HTTP-запросов (по умолчанию: \"%(default)s\")")

  ldap_options = parser.add_argument_group("Параметры LDAP, \
                                           во всех этих параметрах может использоваться подстановка \
                                           {имя_поля_из_строки_запроса} (см. сноску *)")
  ldap_options.add_argument("--ldap-server", default="ldap://{DOMAIN}",
                            help = "URL LDAP сервера (по умолчанию: \"%(default)s\").")
  ldap_options.add_argument("--ldap-user", default="{USERNAME}@{DOMAIN}",
                            help = "DN или иное представление пользователя в LDAP (по умолчанию: \"%(default)s\").")
  ldap_options.add_argument("--ldap-password", default="{PASSWORD}",
                            help = "Пароль пользователя в LDAP (по умолчанию: \"%(default)s\").")
  ldap_options.add_argument("--search-base", default="{DOMAIN}",
                            help = "Базовый (корневой) элемент для поиска в LDAP (по умолчанию: \"%(default)s\").\n\
                            Если значение похоже на имя домена второго и выше уровня оно преобразуется в DN нотацию, \
                            например, \"example.com\" станет \"dc=example,dc=com\".")
  ldap_options.add_argument("--search-filter", default="(sAMAccountName={USERNAME})",
                            help = "Условие фильтра для поиска объектов в LDAP (по умолчанию: \"%(default)s\").")
  ldap_options.add_argument("--attributes", default="*",
                            help = "Список (разделитель запятая) возвращаемых из LDAP атрибутов (по умолчанию все).")

  test_options = parser.add_argument_group("Опции тестирования, при их указании запска сервера не происходит")
  test_options.add_argument("--test-query-string", default="",
                            help = "Тестовая строка параметров эмитирующая поступивший HTTP-запрос")
  return parser.parse_args()

if __name__ == "__main__":
  args = get_args()
  print( args )
  if args.test_query_string:
    print( check_form(args.test_query_string, args.ldap_server, args.ldap_user, args.ldap_password, args.search_base, args.search_filter, args.attributes) )
