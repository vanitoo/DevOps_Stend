# Infrastructure — Automation

Цель: автоматизировать уже понятую вручную инфраструктуру.

Предварительный стек:

```text
OpenTofu/Terraform
        ↓
Proxmox VM provisioning
        ↓
Ansible
        ↓
Linux + Kubernetes bootstrap
        ↓
Declarative cluster add-ons
```

Первый технический milestone: **из описания в Git получить готовые VM и Kubernetes-кластер без ручного создания узлов**.

Планируемые каталоги:

```text
opentofu/
ansible/
kubernetes/
storage/
```

Конкретные provider/module версии будут выбраны после проверки совместимости с текущим Proxmox и целевой версией Kubernetes.
