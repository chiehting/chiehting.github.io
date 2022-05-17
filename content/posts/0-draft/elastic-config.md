bootstrap.memory_lock: true
cluster.initial_master_nodes:
- node1
cluster.name: elasticsearch
indices.breaker.fielddata.limit: 40%
indices.breaker.request.limit: 40%
indices.breaker.total.limit: 70%
indices.fielddata.cache.size: 25%
network.host: 0.0.0.0
node.name: node1




#################################### Paths ####################################

# Path to directory containing configuration (this file and logging.yml):

path.data: /opt/elasticsearch/data

path.logs: /opt/elasticsearch/logs


action.auto_create_index: true

xpack.security.enabled: true

xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: "certificate"
xpack.security.transport.ssl.keystore.path: "/etc/elasticsearch/certs/keystore-password.p12"
xpack.security.transport.ssl.truststore.path: "/etc/elasticsearch/certs/truststore-password.p12"
