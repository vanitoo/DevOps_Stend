# Applications — Automation

Целевой delivery flow:

```text
git push
   ↓
CI: lint / test / scan / build
   ↓
Harbor
   ↓
update desired state
   ↓
Argo CD
   ↓
Kubernetes
   ↓
verification / rollback
```

CI и CD разделяются: pipeline собирает и проверяет artifact, а состояние Kubernetes контролируется GitOps.
