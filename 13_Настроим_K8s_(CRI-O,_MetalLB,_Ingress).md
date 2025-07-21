---
layout: default
title: 13_Настроим K8s (CRI-O, MetalLB, Ingress)
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Настроим K8s (CRI-O, MetalLB, Ingress) 


Источник [тут](https://timeweb.cloud/tutorials/kubernetes/kak-ustanovit-i-nastroit-kubernetes-ubuntu?ysclid=lv10t3tx40397374261)  
  
  
**Подготовим 4 виртуальных машин**  
  


Код:
    
    
    20.20.20.11 master01
    20.20.20.14 worker01
    20.20.20.15 worker02
    20.20.20.16 worker03

Клонируем шаблон k8s-UbuntuTemplate  
  
1 - master нода  
  
vCPU = 8  
vRAM = 8 Gb  
vHDD = 40 Gb  
  
**!!! Добавляем оперативной памяти и ядер !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-10-08 в 16.06.44.png Просмотров:	26 Размер:	58.4 Кб ID:	4112](images\\img_4112_1728392979.png)  
  
Меняем IP и имена хостов на каждом узле  
  


Код:
    
    
    rm /etc/resolv.conf && nano /etc/resolv.conf

Код:
    
    
    nameserver 20.20.20.2

Код:
    
    
    nano /etc/netplan/01-netcfg.yaml

Код:
    
    
    20.20.20.11

Код:
    
    
    nano /etc/hostname

Код:
    
    
    master01

Код:
    
    
    reboot

3 - worker ноды  
  
vCPU = 8  
vRAM = 20 Gb  
vHDD1 = 40 Gb  
vHDD2 = 100 Gb  
  
**!!! Добавляем оперативной памяти, ядер и диск !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-10-08 в 16.07.44.png Просмотров:	26 Размер:	65.0 Кб ID:	4113](images\\img_4113_1728393048.png)  
  
Меняем IP и имена хостов на каждом узле  
  


Код:
    
    
    rm /etc/resolv.conf && nano /etc/resolv.conf

Код:
    
    
    nameserver 20.20.20.2

Код:
    
    
    nano /etc/netplan/01-netcfg.yaml

Код:
    
    
    20.20.20.14

Код:
    
    
    nano /etc/hostname

Код:
    
    
    worker01

Код:
    
    
    reboot

**!!!****worker02****и****worker03****настраиваем аналогично !!!**  
  
**2\. Подключим новый диск на worker нодах**  
  
Убедимся в его наличии  
  


Код:
    
    
    lsblk

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 7.24.15.png Просмотров:	0 Размер:	14.3 Кб ID:	4249](images\\img_4249_1733027126.png)  
  


Код:
    
    
    fdisk /dev/sdb

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 9.50.43.png Просмотров:	0 Размер:	99.2 Кб ID:	4268](images\\img_4268_1733035997.png)  
  


Код:
    
    
    mkfs.ext4 /dev/sdb1

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 7.31.47.png Просмотров:	0 Размер:	51.9 Кб ID:	4251](images\\img_4251_1733027577.png)  
  


Код:
    
    
    mkdir -p /var/lib/containers

Код:
    
    
    mount /dev/sdb1 /var/lib/containers

Код:
    
    
    blkid

Копируем UUID диска /dev/sdb1  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 7.34.30.png Просмотров:	0 Размер:	27.6 Кб ID:	4252](images\\img_4252_1733027795.png)  
  


Код:
    
    
    nano /etc/fstab

Код:
    
    
    UUID=xxxxxxxx /var/lib/containers ext4 rw 0 1

**3\. Отключаем swap раздел (на всех нодах)**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 7.42.57.png Просмотров:	0 Размер:	18.6 Кб ID:	4254](images\\img_4254_1733028293.png)  
  


Код:
    
    
    reboot

Проверим на worker нодах  
  


Код:
    
    
    lsblk

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 7.52.31.png Просмотров:	0 Размер:	17.1 Кб ID:	4255](images\\img_4255_1733028891.png)  
  
**4\. Включим доп. модули сети (на всех нодах)**  
  


Код:
    
    
    modprobe overlay
    modprobe br_netfilter

Код:
    
    
    nano /etc/modules-load.d/k8s.conf

Код:
    
    
    overlay
    br_netfilter

Проверим  
  


Код:
    
    
    lsmod | egrep "br_netfilter|overlay"

​![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 10.05.22.png Просмотров:	0 Размер:	13.2 Кб ID:	4269](images\\img_4269_1733036782.png)  
  


Код:
    
    
    nano /etc/sysctl.d/k8s.conf

Код:
    
    
    net.bridge.bridge-nf-call-iptables = 1
    net.bridge.bridge-nf-call-ip6tables = 1
    net.ipv4.ip_forward = 1

Проверим  
  


Код:
    
    
    sysctl --system

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 7.59.02.png Просмотров:	0 Размер:	33.8 Кб ID:	4256](images\\img_4256_1733029220.png)  
  
**5\. Установка Kubernetes (на всех нодах)**  
  
Выбираем актуальную версию  
  


Код:
    
    
    https://kubernetes.io/releases/

Add the Kubernetes repository  
  


Код:
    
    
    mkdir -p /etc/apt/keyrings

Код:
    
    
    curl -fsSL https://pkgs.k8s.io/core:/stable:/**v1.30** /deb/Release.key |gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

Код:
    
    
    echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/**v1.30** /deb/ /" |tee /etc/apt/sources.list.d/kubernetes.list

Add the CRI-O repository  
  


Код:
    
    
    curl -fsSL https://pkgs.k8s.io/addons:/cri-o:/prerelease:/main/deb/Release.key |gpg --dearmor -o /etc/apt/keyrings/cri-o-apt-keyring.gpg

Код:
    
    
    echo "deb [signed-by=/etc/apt/keyrings/cri-o-apt-keyring.gpg] https://pkgs.k8s.io/addons:/cri-o:/prerelease:/main/deb/ /" |tee /etc/apt/sources.list.d/cri-o.list

Код:
    
    
    apt-get update

Код:
    
    
    apt-get install -y cri-o kubelet kubeadm kubectl

Код:
    
    
    apt-mark hold cri-o kubelet kubeadm kubectl

Код:
    
    
    systemctl start crio && systemctl enable crio

Код:
    
    
    systemctl status crio

**6\. Покупаем Wildcard сертификат**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/3514)  
  
Копируем содержимое корневых сертификатов (на всех нодах)  
  


Код:
    
    
    nano /etc/containers/certs.d/ca.crt

Код:
    
    
    cp /etc/containers/certs.d/ca.crt /usr/local/share/ca-certificates/ca.crt

Код:
    
    
    update-ca-certificates --fresh

**!!! Для всех****worker****нод переходим п.5 !!!**  
  
**7\. Инициализация кластера Kubernetes  
  
!!! Только для первой master01 ноды в кластере!!!**  
  


Код:
    
    
    kubeadm init --pod-network-cidr=10.244.0.0/16

Код:
    
    
    mkdir -p $HOME/.kube
    cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    chown $(id -u):$(id -g) $HOME/.kube/config
    export KUBECONFIG=/etc/kubernetes/admin.conf

**8\. Добавляем worker ноды**  
  
В водим в консолях worker строку подключения  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 18.44.53.png Просмотров:	0 Размер:	15.7 Кб ID:	4273](images\\img_4273_1733067950.png)  
  
Проверим в консоли master01 ноды  
  


Код:
    
    
    kubectl get nodes

​![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 18.47.00.png Просмотров:	0 Размер:	16.2 Кб ID:	4274](images\\img_4274_1733068068.png)  
  
Меняем роль ноды  
  


Код:
    
    
    kubectl label node worker01 node-role.kubernetes.io/worker=worker
    kubectl label node worker02 node-role.kubernetes.io/worker=worker
    kubectl label node worker03 node-role.kubernetes.io/worker=worker

Код:
    
    
    kubectl get nodes

​![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 18.48.25.png Просмотров:	0 Размер:	16.7 Кб ID:	4275](images\\img_4275_1733068141.png)  
  
**9\. Ставим сетевой плагин CNI Flannel**  
  
В консоли master01 ноды  
  


Код:
    
    
    kubectl apply -f https://github.com/flannel-io/flannel/releases/download/v0.26.1/kube-flannel.yml

​![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 18.49.47.png Просмотров:	0 Размер:	28.7 Кб ID:	4276](images\\img_4276_1733068263.png)  
  
Проверим  
  


Код:
    
    
    kubectl get po -n kube-flannel

​![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 18.51.15.png Просмотров:	0 Размер:	24.3 Кб ID:	4277](images\\img_4277_1733068310.png)  
  


Код:
    
    
    kubectl get nodes

​​![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 18.52.05.png Просмотров:	0 Размер:	17.6 Кб ID:	4278](images\\img_4278_1733068382.png)  
  


Код:
    
    
    kubectl get po -A

​![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 18.53.15.png Просмотров:	0 Размер:	77.4 Кб ID:	4279](images\\img_4279_1733068444.png)  
  


Код:
    
    
    crictl pods

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 18.54.22.png Просмотров:	0 Размер:	41.7 Кб ID:	4280](images\\img_4280_1733068488.png)  
  


Код:
    
    
    crictl images

​  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 18.55.00.png Просмотров:	0 Размер:	64.7 Кб ID:	4281](images\\img_4281_1733068533.png)  
  
**10\. Настроим Metallb**  
  
Источник [тут](https://metallb.io/installation/)  
  
В консоли master01 ноды  
  


Код:
    
    
    kubectl get configmap kube-proxy -n kube-system -o yaml | sed -e "s/strictARP: false/strictARP: true/" | kubectl apply -f - -n kube-system

Выбираем актуальную версию  
  


Код:
    
    
    https://metallb.io/

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-05-18 в 5.51.52.png Просмотров:	0 Размер:	10.7 Кб ID:	3547](images\\img_3547_1716000783.png)​  
  


Код:
    
    
    kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.5/config/manifests/metallb-native.yaml

Проверим  
  


Код:
    
    
    kubectl get po -n metallb-system

​![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 18.58.11.png Просмотров:	0 Размер:	30.0 Кб ID:	4282](images\\img_4282_1733068730.png)  
  
Выбираем 3 свободных IP адреса  
  
**!!! IP адреса приведены для примера !!!**  
  
metallb_pool: 20.20.20.77 - 20.20.20.79  
  


Код:
    
    
    nano metall-lb.yml

Код:
    
    
    apiVersion: metallb.io/v1beta1
    kind: IPAddressPool
    metadata:
      name: default
      namespace: metallb-system
    spec:
      addresses:
      - 20.20.20.77-20.20.20.79
      autoAssign: true
    ---
    apiVersion: metallb.io/v1beta1
    kind: L2Advertisement
    metadata:
      name: default
      namespace: metallb-system
    spec:
      ipAddressPools:
      - default

Код:
    
    
    kubectl apply -f metall-lb.yml

​![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 19.00.45.png Просмотров:	0 Размер:	9.6 Кб ID:	4283](images\\img_4283_1733068878.png)  
  
**11\. Настроим NGINX Ingress Controller**  
  
Источник [тут](https://kubernetes.github.io/ingress-nginx/deploy/#bare-metal-clusters)  
  
Выбираем актуальную версию  
  


Код:
    
    
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/baremetal/deploy.yaml

Проверим  
  


Код:
    
    
    kubectl get po -n ingress-nginx

​![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 19.03.54.png Просмотров:	0 Размер:	24.8 Кб ID:	4284](images\\img_4284_1733069097.png)  
  
Добавим сервис LoadBalancer  
  


Код:
    
    
    nano loadbalancer.yml

Код:
    
    
    kind: Service
    apiVersion: v1
    metadata:
      name: ingress-nginx-lb
      namespace: ingress-nginx
      annotations:
        metallb.universe.tf/address-pool: default
    spec:
      ports:
        - name: http
          protocol: TCP
          port: 80
          targetPort: 80
        - name: https
          protocol: TCP
          port: 443
          targetPort: 443
      selector:
        app.kubernetes.io/component: controller
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/part-of: ingress-nginx
      type: LoadBalancer

Код:
    
    
    kubectl apply -f loadbalancer.yml

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 19.05.40.png Просмотров:	0 Размер:	8.7 Кб ID:	4285](images\\img_4285_1733069169.png)  
  
Проверим  
  


Код:
    
    
    kubectl -n ingress-nginx get svc

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 19.06.45.png Просмотров:	0 Размер:	30.8 Кб ID:	4286](images\\img_4286_1733069253.png)  
  
**12\. Обновляем корневые сертификаты (на всех нодах)**  
  
Копируем содержимое консоли  
  


Код:
    
    
    20.20.20.2

Код:
    
    
    cat /media/data/easy-rsa/pki/ca.crt

Код:
    
    
    -----BEGIN CERTIFICATE-----
    xxxxxx
    -----END CERTIFICATE-----

Вставляем в консоль на каждой ноде  
  


Код:
    
    
    mkdir -p /etc/containers/certs.d

Код:
    
    
    nano /etc/containers/certs.d/ca.crt

Код:
    
    
    cp /etc/containers/certs.d/ca.crt /usr/local/share/ca-certificates/ca.crt

Код:
    
    
    update-ca-certificates --fresh

Код:
    
    
    systemctl restart crio

**13\. Копируем утилиту kubectl на свой ПК**  
  
Смотрим актуальную версию для своей платформы  
  


Код:
    
    
    https://kubernetes.io/docs/tasks/tools/

**Для MacOS (Intel x64****)**  
  


Код:
    
    
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"

Код:
    
    
    chmod +x ./kubectl

Код:
    
    
    sudo mv ./kubectl /usr/local/bin/kubectl

Код:
    
    
    sudo chown root: /usr/local/bin/kubectl

Проверим  
  


Код:
    
    
    kubectl version --client

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-30 в 7.11.06.png Просмотров:	0 Размер:	11.3 Кб ID:	4243](images\\img_4243_1732939916.png)  
  
**14\. Копируем ключи на свой ПК**  
  
**Для MacOS**  
  


Код:
    
    
    sudo mkdir ./.kube

Код:
    
    
    sudo nano ./.kube/config

**Для Linux**  
  


Код:
    
    
    sudo mkdir ~/.kube

Код:
    
    
    sudo nano ~/.kube/config

**Для Windows**  
  


Код:
    
    
    C:\Users\example\.kube

Копируем содержимое из консоли master01  
  


Код:
    
    
    cat .kube/config

Проверим  
  
В консоли терминала на своем ПК  
  


Код:
    
    
    sudo kubectl --kubeconfig ~/.kube/config get nodes

​![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-01 в 19.37.28.png Просмотров:	4 Размер:	10.9 Кб ID:	4288](images\\img_4288_1733071121.png)  
  
**15\. Подключим панель управления Lens**  
  
Загрузим версию для своей ОС  
  


Код:
    
    
    https://k8slens.dev/

  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-04-17 в 12.19.37.png Просмотров:	0 Размер:	15.2 Кб ID:	3289](images\\img_3289_1713345708.png)​  
  
Активируйте свой Lens ID  
  


Код:
    
    
    https://app.k8slens.dev/home

Назначите пароль для своей учетной записи  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-04-20 в 6.57.24.png Просмотров:	0 Размер:	34.8 Кб ID:	3300](images\\img_3300_1713585522.png)​  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-04-30 в 11.17.57.png Просмотров:	0 Размер:	91.9 Кб ID:	3362](images\\img_3362_1714465275.png)​  
  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-04-30 в 11.22.28.png Просмотров:	0 Размер:	69.0 Кб ID:	3363](images\\img_3363_1714465413.png)​  
  
  
**Поздравляю, настройка завершена!**

Вложения 

  * [ ![Нажмите на изображение для увеличения.



Название:	Снимок экрана 2024-11-30 в 7.48.50.png

Просмотров:	96

Размер:	6.1 Кб

ID:	4248](images\\img_4248_0.png) ](filedata/fetch?id=4248)




---

