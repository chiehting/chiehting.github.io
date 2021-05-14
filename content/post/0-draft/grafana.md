rate(container_cpu_usage_seconds_total{image!="",container="tequila-backstage-api"}[1m])

---

container_memory_usage_bytes{container="baccarat-backend"}

sum (rate (container_cpu_usage_seconds_total{image!="",container="game-merchant-backstage-api"}[1m])) by (pod_name)

sum(container_memory_usage_bytes{container="game-merchant-backstage-api"}) by (pod_name)

---
rate(container_cpu_usage_seconds_total{image!="",container="tequila-backstage-api"}[1m])

container_memory_usage_bytes{container="tequila-backstage-api"}


game-merchant-backstage-api

