# Security findings: v1 baseline

Этот документ фиксирует проблемы v1, которые **не должны автоматически переноситься в v2**.

## Severity: High

### Hardcoded credentials

Обнаружены literal credentials в документации и конфигурациях для нескольких сервисов, включая GitLab/PostgreSQL, Harbor, Keycloak, Patroni и OIDC.

Правило v2:

- реальные секреты не хранятся в Git;
- Manual-трек использует только явно фиктивные учебные значения;
- Automation-трек получает секреты из отдельного secret-management механизма;
- перед публикацией примеров выполняется secret scanning.

### OIDC client secret в Kubernetes manifest

В legacy-манифесте OpenShift Console client secret передаётся непосредственно аргументом контейнера.

Правило v2: secret должен приходить через Kubernetes Secret / External Secret и не быть частью открытого manifest.

### Отключение проверки TLS

В v1 обнаружены настройки, отключающие TLS verification.

Правило v2:

- корректная CA chain по умолчанию;
- insecure mode возможен только в отдельной лаборатории;
- любой insecure пример маркируется `LAB ONLY` и содержит объяснение риска.

## Severity: Medium

### Redis без аутентификации

Legacy compose содержит `ALLOW_EMPTY_PASSWORD=yes`.

В v2 это не используется как default.

### Broad RBAC

В legacy manifests встречаются:

- `cluster-admin`;
- wildcard resources/verbs;
- расширенные permissions.

Для v2 применяется least privilege. Если системный компонент действительно требует широких прав, это должно быть документировано.

### Privileged containers / hostPath

Legacy manifests используют privileged mode и hostPath для отдельных системных компонентов.

В v2 для каждого такого случая должны быть:

- причина;
- scope;
- минимальный набор capabilities;
- альтернатива, если она существует.

## Supply chain

В compose/manifests встречаются `:latest` и непинованные image tags.

Правило v2:

1. pin версии;
2. по возможности pin digest для критичных компонентов;
3. фиксировать совместимость;
4. обновления делать отдельным контролируемым изменением.

## Security gates для v2

Минимальный целевой pipeline:

```text
lint
  ↓
secret scan
  ↓
IaC scan
  ↓
container scan
  ↓
policy checks
  ↓
deploy
```

Конкретные инструменты выбираются позднее после проверки актуального состояния экосистемы.
