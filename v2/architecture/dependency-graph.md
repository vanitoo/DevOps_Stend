# Dependency graph

Рабочая зависимость компонентов v2.

```text
Proxmox
   │
   ▼
Virtual Machines
   │
   ├───────────────┐
   ▼               ▼
Network          Linux baseline
   │               │
   ├──── DNS       │
   ├──── DHCP      │
   └──── VPN       │
                   │
                   ▼
               Kubernetes
                /   |   \
               /    |    \
              ▼     ▼     ▼
          Ingress  CSI   GitOps
                    │      │
                    ▼      ▼
                  Ceph   Platform
                           │
          ┌────────────────┼─────────────────┐
          ▼                ▼                 ▼
       GitLab           Harbor            Keycloak
          │                │                 │
          └──────┬─────────┘                 │
                 ▼                           │
            Applications ◄───────────────────┘
                 │
        ┌────────┼─────────┐
        ▼        ▼         ▼
     Database  Logging  Monitoring
        │                  │
        └──── Backup/DR ────┘
```

## Bootstrap boundary

Нужно отдельно решить bootstrap-проблему:

- что устанавливается Ansible до появления GitOps;
- какой минимальный набор нужен, чтобы стартовал Argo CD;
- какие компоненты после этого управляются уже только GitOps.

Предварительно:

```text
OpenTofu
   ↓
VM
   ↓
Ansible
   ↓
Kubernetes
   ↓
Argo CD bootstrap
   ↓
Everything else from Git
```

## Ownership boundary

### Infrastructure

Владеет:

- compute;
- OS baseline;
- network;
- Kubernetes lifecycle;
- storage.

### Platform

Владеет:

- source/CI;
- registry;
- IAM;
- data services;
- observability;
- backup.

### Applications

Владеет:

- app source;
- build;
- runtime config;
- deployment definition;
- app SLI/logging/metrics;
- release lifecycle.
