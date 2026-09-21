# Roadmap DevOps Stend v2

## Phase 0 — Preserve v1

- [x] создать отдельную ветку v2;
- [x] не менять `master`;
- [x] провести первичный структурный/security audit;
- [x] зафиксировать слои и уровни обучения.

## Phase 1 — Inventory and validation

- [ ] проверить все инструкции v1 на ссылки и изображения;
- [ ] составить version matrix;
- [ ] составить dependency graph;
- [ ] классифицировать literal secrets;
- [ ] определить canonical документы для дублей;
- [ ] проверить YAML/Compose на поддерживаемые API и версии;
- [ ] определить lab-only небезопасные настройки.

## Phase 2 — Infrastructure automation

- [ ] выбрать OpenTofu/Terraform provider для Proxmox;
- [ ] описать VM inventory;
- [ ] создать reusable VM module;
- [ ] создать Ansible inventory;
- [ ] Linux baseline role;
- [ ] Kubernetes bootstrap;
- [ ] networking;
- [ ] storage.

## Phase 3 — Platform automation

- [ ] Argo CD bootstrap;
- [ ] secrets management;
- [ ] Harbor;
- [ ] GitLab/Runner;
- [ ] IAM;
- [ ] observability;
- [ ] logging;
- [ ] backup.

## Phase 4 — Applications

- [ ] Flask reference app;
- [ ] Django reference app;
- [ ] CI pipeline;
- [ ] image scanning;
- [ ] Helm/Kustomize packaging;
- [ ] GitOps deployment;
- [ ] rollback exercise.

## Phase 5 — Platform Engineering

- [ ] environments;
- [ ] golden path;
- [ ] templates;
- [ ] policy as code;
- [ ] self-service workflow;
- [ ] SLO/DR exercises.
