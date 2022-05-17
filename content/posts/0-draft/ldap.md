ldapsearch -x uid=admin
ldapsearch -x uid=admin
ldapsearch -x uid=justin.lee
ldapsearch -x uid=admin,dc=example,dc=com
ldapsearch -x uid=admin dc=example,dc=com
ldapsearch -x uid=admin
ldapsearch -x dc=example,dc=com
ldapsearch -x uid=admin
ldapsearch -x -b "dc=example,dc=tw" "(uid=justin.lee)"
ldapsearch -x -b "dc=example,dc=tw" "(cn=*)"

## awx
```yaml
# LDAP SERVER URI
ldap://ldap.example.com:389 

# LDAP BIND DN
uid=admin,cn=users,cn=accounts,dc=example,dc=com

#LDAP USER DN TEMPLATE
uid=%(user)s,cn=users,cn=accounts,dc=example,dc=com

# LDAP GROUP TYPE
NestedMemberDNGroupType

# LDAP USER SEARCH
[
 "cn=groups,dc=example,dc=com",
 "SCOPE_SUBTREE",
 "(uid=%(user)s)"
]

# LDAP GROUP SEARCH
[
 "cn=groups,cn=accounts,dc=example,dc=com",
 "SCOPE_SUBTREE",
 "(objectClass=groupOfNames)"
]

# LDAP USER ATTRIBUTE MAP
{
 "first_name": "givenName",
 "last_name": "sn",
 "email": "mail"
}

# LDAP GROUP TYPE PARAMETERS
{
 "name_attr": "cn",
 "member_attr": "member"
}

# LDAP USER FLAGS BY GROUP
{
 "is_superuser": [
  "cn=admins,cn=groups,cn=accounts,dc=example,dc=com"
 ]
}

```



grafana

```yaml
[[servers]]
host = "ldap.example.tw"
port = 389
use_ssl = false
start_tls = false
ssl_skip_verify = false
bind_dn = "uid=admin,cn=users,cn=accounts,dc=example,dc=tw"
bind_password = 'password'
search_filter = "(uid=%s)"
search_base_dns = ["cn=users,cn=accounts,dc=example,dc=tw"]

[servers.attributes]
name = "givenName"
surname = "sn"
username = "uid"
member_of = "memberOf"
email =  "email"

[[servers.group_mappings]]
group_dn = "cn=admins,cn=groups,cn=accounts,dc=example,dc=tw"
org_role = "Admin"

[[servers.group_mappings]]
group_dn = "cn=groups,ou=accounts,dc=example,dc=tw"
org_role = "Editor"

[[servers.group_mappings]]
group_dn = "*"
org_role = "Editor"
```
