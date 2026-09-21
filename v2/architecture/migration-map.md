# Карта миграции v1 → v2

Это рабочая карта. Нумерация v1 сохраняется как историческая и учебная ссылка.

## Infrastructure layer

| v1 | Тема | v2 |
|---|---|---|
| 01 | Блок-схема | Architecture / topology |
| 02 | Proxmox | Infrastructure / Compute |
| 03 | Gateway | Infrastructure / Network |
| 04 | OpenVPN | Infrastructure / Network / VPN |
| 05 | VM template | Infrastructure / Compute / Templates |
| 06 | BIND DNS | Infrastructure / Network / DNS |
| 07 | DHCP | Infrastructure / Network / DHCP |
| 08 | Wildcard TLS | Infrastructure / Network / TLS |
| 13 | Kubernetes | Infrastructure / Kubernetes |
| 14 | Ceph S3 | Infrastructure / Storage |
| 15 | Ceph CSI | Infrastructure / Storage / Kubernetes |
| 20 | Node Exporter | Infrastructure observability agent |

## Platform layer

| v1 | Тема | v2 |
|---|---|---|
| 09 | Harbor | Platform / Registry |
| 10 | Docker Hub mirror | Platform / Registry |
| 11 | GitLab | Platform / SCM |
| 12 | GitLab Runner | Platform / CI |
| 16 | PostgreSQL + Patroni + ETCD | Platform / Data |
| 17 | Kafka | Platform / Messaging |
| 18 | OpenSearch | Platform / Logging |
| 19 | Prometheus + Grafana + VictoriaMetrics | Platform / Observability |
| 24 | Wal-G | Platform / Backup |
| 25 | Velero | Platform / Backup |
| 26 | FreeIPA | Platform / IAM |
| 27 | Keycloak + FreeIPA | Platform / IAM |
| 28 | Keycloak + GitLab | Platform / IAM |
| 29 | OKD Console + Keycloak | Platform / Access/UI |
| 55 | Jenkins CI/CD | Platform / CI |
| 57 | GitLab Operator | Platform / SCM |
| 58 | GitLab Runner in Kubernetes | Platform / CI |
| 59 | GitLab Runner | Platform / CI |

## Application layer

| v1 | Тема | v2 |
|---|---|---|
| 21 | Flask container | Applications / Flask |
| 22 | GitLab CI/CD | Applications / Delivery |
| 23 | Django deployment | Applications / Django |
| 30 | Django logging | Applications / Operations |
| 31 | Django + Patroni | Applications / Data integration |
| 54 | PyCharm + Django | Applications / Developer workflow |
| 56 | Clone project to GitLab | Applications / Source workflow |

## Supporting / prerequisites

| v1 | Тема | Решение |
|---|---|---|
| 50 | Wildcard TLS | дубликат/альтернативная нумерация 08; определить canonical |
| 51 | Ubuntu 20.04 | prerequisite/manual Linux track |
| 52 | BIND DNS | дубликат/альтернативная нумерация 06; определить canonical |
| 53 | Docker + Compose | prerequisite/container track |

## Следующий этап

Для каждого пункта составляется карточка:

```text
Prerequisites
Manual objective
Manual verification
Automation equivalent
Variables
Secrets
Security notes
Version constraints
Rollback / recovery
Links to v1
```
