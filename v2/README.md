# DevOps Stend v2

> v2 развивается параллельно с существующим стендом. Содержимое v1 (`docs/`, `YAML/`, текущий GitHub Pages) на этом этапе не изменяется.

## Идея

DevOps Stend v2 сохраняет два способа обучения:

1. **Manual — "Собери руками"**: студент проходит инфраструктуру вручную и понимает каждый компонент.
2. **Automation — "Автоматизируй"**: те же задачи переводятся в Infrastructure as Code, Configuration as Code и GitOps.

Поверх них постепенно появляется третий этап — **Platform Engineering**, где инфраструктура становится внутренней платформой для разработчиков.

## Архитектурные слои

- **Infrastructure** — Proxmox, VM, network, DNS/DHCP/VPN, Kubernetes, load balancing, storage/Ceph/CSI.
- **Platform** — GitLab, Runner, Harbor, IAM/Keycloak/FreeIPA, databases, messaging, observability, backup.
- **Applications** — Flask/Django, контейнеризация, CI/CD, конфигурация, деплой, rollback и эксплуатация.

Главное правило:

> **Layer = что строим. Level = насколько это автоматизировано.**

## Структура

```text
v2/
├── audit/
├── architecture/
├── infrastructure/
│   ├── manual/
│   └── automation/
├── platform/
│   ├── manual/
│   └── automation/
├── applications/
│   ├── manual/
│   └── automation/
└── platform-engineering/
```

## Принцип миграции

v1 не переносится массово и не переписывается. Сначала для каждого существующего шага определяется:

- слой;
- учебная цель;
- зависимости;
- что студент должен сделать руками;
- что потом автоматизируется;
- какие текущие примеры можно переиспользовать;
- какие конфиги небезопасны или устарели и должны остаться только как legacy/reference.

См. [аудит v1](audit/v1-inventory.md) и [карту миграции](architecture/migration-map.md).
