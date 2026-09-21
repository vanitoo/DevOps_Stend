# Архитектура v2

## Две оси

DevOps Stend v2 строится одновременно по двум независимым осям.

### Слои

```text
Infrastructure
     ↓
Platform
     ↓
Applications
```

### Уровни обучения

```text
Manual
  ↓
Automation
  ↓
Platform Engineering
```

Их нельзя смешивать: Infrastructure/Platform/Application описывают предметную область, а Manual/Automation — способ работы с ней.

## Полная модель

| Layer | Manual | Automation |
|---|---|---|
| Infrastructure | VM, Linux, network, kubeadm, Ceph руками | OpenTofu + Ansible + declarative Kubernetes |
| Platform | GitLab, Harbor, Keycloak, monitoring, backup руками | Helm/Kustomize + GitOps + secrets management |
| Applications | Docker, kubectl, CI/CD и эксплуатация руками | pipeline + registry + GitOps + progressive delivery |

После прохождения Automation появляется Platform Engineering: стандартизация, self-service, policy-as-code, templates и developer experience.
