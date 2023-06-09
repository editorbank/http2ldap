# coding: utf-8
import ldap3
import json
import re
import urllib

def ldap_query(server_uri:str, user:str, password:str, search_base=None, search_filter=None, **search_args):
    #print((server_uri, user, password, search_base, search_filter, search_args))
    server = ldap3.Server(server_uri)
    with ldap3.Connection(server, user, password) as connect:
        connect.search(search_base, search_filter, **search_args)
        return json.loads(connect.response_to_json())

def domain2dn(domain_or_dn):
    if re.compile(r"^([a-z][a-z0-9\-]*)(\.[a-z][a-z0-9\-]*)+$").match(domain_or_dn):
        return ",".join(["dc="+i for i in domain_or_dn.split(".")])
    else:
        return domain_or_dn

def check_form(query_string, server_uri, ldap_user, ldap_password, search_base, search_filter, attributes):
    try:
        query_params_dict = dict(urllib.parse.parse_qsl(query_string))
        def expand(value:str, variables:dict=query_params_dict)->str:
            return value.format(**variables)
        return ldap_query(expand(server_uri), expand(ldap_user), expand(ldap_password),
                          domain2dn(expand(search_base)), expand(search_filter),
                          attributes = expand(attributes).split(','))
    except Exception as e:
        return {"error": f"{e}"}

if __name__ == "__main__":
    assert (domain2dn("example.com")=="dc=example,dc=com")
    assert (domain2dn("example")=="example")
    assert (domain2dn("ou=xxxx")=="ou=xxxx")
    # Test for the default LDAP server in Apache Directory Studio
    assert (
        check_form(
            "USERNAME=admin&PASSWORD=secret",
            "localhost:10389",
            "uid={USERNAME},ou=system",
            "{PASSWORD}",
            "ou=system",
            "(uid={USERNAME})",
            "displayName",
        )=={'entries': [{ 'dn': 'uid=admin,ou=system', 'attributes': {'displayName': 'Directory Superuser'} }]}
    )