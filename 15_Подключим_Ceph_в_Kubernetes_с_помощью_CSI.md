---
layout: default
title: 15_Подключим Ceph в Kubernetes с помощью CSI
---


##  Подключим Ceph в Kubernetes с помощью CSI 

12-01-2024, 09:01 AM

  
Загружаем [**_архив_**](https://galkin-vladimir.ru:5446/d/s/119wnMMuR5g1iCaFKOwg6POL02YUbRgN/WGBp1ka-KI8hcd3rjpupgUfgzFfMEGoY-iL3Ahjia3Qs)  
  
Распаковываем и переходим в папку YAML_CSI  
  
**!!! Заменяем своими параметрами !!!**  
  
FSID = ClusterID  
  


Код:
    
    
    nano 1-csi-config-map.yaml

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 9.14.16.png Просмотров:	0 Размер:	19.6 Кб ID:	4265](images\\img_4265_1733033916.jpg)  
  


Код:
    
    
    nano 2-csi-rbd-secret.yaml

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 9.15.40.png Просмотров:	0 Размер:	15.1 Кб ID:	4266](images\\img_4266_1733033933.jpg)  
  


Код:
    
    
    nano 7-csi-rbd-sc.yaml

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 9.16.45.png Просмотров:	0 Размер:	31.4 Кб ID:	4267](images\\img_4267_1733033946.jpg)  
  
**Для MacOS (Intel x64****)**  
  


Код:
    
    
    sudo kubectl --kubeconfig ~/.kube/config apply -f 1-csi-config-map.yaml
    sudo kubectl --kubeconfig ~/.kube/config apply -f 2-csi-rbd-secret.yaml
    sudo kubectl --kubeconfig ~/.kube/config apply -f 3-csi-provisioner-rbac.yaml
    sudo kubectl --kubeconfig ~/.kube/config apply -f 4-csi-nodeplugin-rbac.yaml
    sudo kubectl --kubeconfig ~/.kube/config apply -f 5-csi-rbdplugin-provisioner.yaml
    sudo kubectl --kubeconfig ~/.kube/config apply -f 6-csi-rbdplugin.yaml
    sudo kubectl --kubeconfig ~/.kube/config apply -f 7-csi-rbd-sc.yaml

Проверим  
  


Код:
    
    
    sudo kubectl --kubeconfig ~/.kube/config get po -n default

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 20.02.04.png Просмотров:	0 Размер:	21.6 Кб ID:	4289](images\\img_4289_1733072602.jpg)  
  
Проверим  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 21.30.16 \(2\).png Просмотров:	3 Размер:	12.4 Кб ID:	4293](images\\img_4293_1733078025.jpg)  
  
  


Код:
    
    
    nano ceph-rbd-claim.yml

Код:
    
    
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: ceph-rbd-claim
    spec:
      accessModes:
      - ReadWriteOnce
      resources:
        requests:
          storage: 1Gi
      storageClassName: csi-rbd-sc

Код:
    
    
    sudo kubectl --kubeconfig ~/.kube/config apply -f ceph-rbd-claim.yml

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 21.08.53 \(2\).png Просмотров:	0 Размер:	20.7 Кб ID:	4292](images\\img_4292_1733076604.jpg)  
  
**Поздравляю, настройка завершена!**


---

