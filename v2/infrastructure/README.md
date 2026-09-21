# Infrastructure layer

Infrastructure отвечает на вопрос: **где и на чём работает платформа?**

Области:

- Proxmox и compute;
- VM templates;
- Linux baseline;
- network, gateway, DNS, DHCP, VPN;
- Kubernetes;
- load balancing и ingress;
- storage, Ceph и CSI.

Внутри слоя два трека:

- [Manual](manual/README.md) — собрать руками;
- [Automation](automation/README.md) — воспроизвести то же состояние кодом.
