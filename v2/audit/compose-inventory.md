# docker-compose inventory from v1

Проверены все 10 compose-файлов v1.

## Airflow

Обнаружено:

- Airflow 2.7.1;
- PostgreSQL 13;
- Redis latest;
- default Airflow credentials в example configuration.

## Cassandra

Обнаружено:

- Cassandra 4.0.

## GitLab

Обнаружено:

- PostgreSQL 14.0;
- Redis 6.2.6;
- GitLab CE 14.4.0;
- nginx 1.22;
- literal database password;
- прямые host port mappings.

## Kafka

Обнаружено:

- Confluent Kafka/Zookeeper с `latest`;
- Kafka UI без явного pin tag в compose.

## Keycloak

Обнаружено:

- PostgreSQL 14.0;
- Keycloak 20.0.2;
- default/simple database/admin credentials;
- relaxed hostname/http options, которые требуют отдельного review.

## OpenSearch

Обнаружено:

- OpenSearch 2.10.0;
- OpenSearch Dashboards 2.10.0;
- Logstash-based plugin image 8.9.0.

## Patroni helper compose

Обнаружен pgAdmin с простым default password.

Сами Patroni nodes описаны отдельными YAML-конфигами.

## Prometheus

Обнаружено:

- Prometheus latest;
- node-exporter без pin;
- Grafana без pin;
- node-exporter запускается как root и монтирует host proc/sys.

## Prometheus + VictoriaMetrics

Обнаружены непинованные версии для нескольких компонентов:

- Prometheus;
- Grafana;
- VictoriaMetrics;
- vmagent;
- Alertmanager;
- alertmanager-bot.

## Redis

Обнаружено:

- Bitnami Redis latest;
- `ALLOW_EMPTY_PASSWORD=yes`;
- containers запускаются от root.

## Вывод для v2

Compose из v1 используется как **reference**, а не как источник готовых production-конфигов.

Перед переносом каждого сервиса:

1. выбрать поддерживаемую версию;
2. pin image;
3. убрать literal credentials;
4. определить volumes/storage;
5. определить health checks;
6. определить network exposure;
7. определить backup;
8. определить upgrade/rollback.
