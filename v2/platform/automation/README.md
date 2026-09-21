# Platform — Automation

Цель: перенести платформенные сервисы из ручной установки в декларативное управление.

Предварительный путь:

```text
Helm / Kustomize
       ↓
Git repository
       ↓
Argo CD
       ↓
Kubernetes
```

Secrets не хранятся открытым текстом в Git.

Планируемые направления:

- GitOps bootstrap;
- Harbor;
- GitLab / Runner;
- Keycloak;
- observability;
- logging;
- databases;
- backup;
- secrets management.
