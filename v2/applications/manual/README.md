# Applications — Manual

Студент проходит путь приложения вручную:

```text
source
  ↓
Dockerfile
  ↓
docker build
  ↓
registry
  ↓
Kubernetes manifests
  ↓
kubectl apply
  ↓
logs / metrics / database
```

Цель — понять каждый переход до внедрения автоматического pipeline.
