# Platform layer

Platform отвечает на вопрос: **какие готовые сервисы получает команда поверх инфраструктуры?**

Основные домены:

- SCM/CI: GitLab, GitLab Runner, Jenkins;
- Registry: Harbor, registry mirror;
- IAM: FreeIPA, Keycloak, OIDC;
- Data: PostgreSQL/Patroni;
- Messaging: Kafka;
- Observability: metrics, dashboards, logging, alerting;
- Backup/DR: Velero, Wal-G.

Треки:

- [Manual](manual/README.md);
- [Automation](automation/README.md).
