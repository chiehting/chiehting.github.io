  170  ldapsearch
  171  apt install ldap-utils
  172  ldapsearch -x uid=admin
  173  ldapsearch -x uid=justin.lee
  174  ldapsearch -x uid=admin
  175  ldapsearch -x uid=admin dc=example,dc=com
  176  ldapsearch -x uid=admin,dc=example,dc=com
  177  ldapsearch -x uid=admin
  178  ldapsearch -x dc=example,dc=com
  179  ldapsearch -x uid=admin
  
  
  awx 
  
```
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