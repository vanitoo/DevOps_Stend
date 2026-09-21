# Legacy version inventory

Это инвентаризация обнаруженных в v1 версий. Она **не является рекомендацией** для v2.

| Component | Version/tag found in v1 | Status for v2 |
|---|---:|---|
| Ubuntu | 20.04 LTS | review required |
| GitLab CE | 14.4.0-ce.0 | legacy |
| GitLab Runner chart | 0.64.0 in one guide | review required |
| PostgreSQL | 13 / 14.0 | review required |
| Redis | 6.2.6 and latest | remove latest, review |
| Keycloak | 20.0.2 | review required |
| Ceph | 15 Octopus | legacy |
| OpenSearch | 2.10.0 | review required |
| OpenSearch Dashboards | 2.10.0 | review required |
| Logstash OSS plugin image | 8.9.0 | review required |
| Airflow | 2.7.1 | review required |
| Cassandra | 4.0 | review required |
| Prometheus | latest in several examples | must pin |
| VictoriaMetrics | latest | must pin |
| Alertmanager | latest | must pin |
| Kafka/Zookeeper Confluent images | latest | must pin |
| Bitnami Redis | latest | must pin |
| OpenShift Console | 4.12.0 | legacy/review |
| cert-manager | 1.14.5 in guide | review required |

## Kubernetes API inventory

Найдены legacy API:

```text
extensions/v1beta1
```

в DEX deployment/ingress.

Это нельзя переносить в v2 без миграции на поддерживаемые API.

## Policy

Для v2 версия выбирается не по принципу "самая новая", а по цепочке:

```text
supported upstream
      +
compatibility
      +
security support
      +
tested in stand
      =
pinned v2 version
```

Следующий шаг — сверить каждый компонент с актуальной upstream-документацией и собрать проверенную compatibility matrix.
