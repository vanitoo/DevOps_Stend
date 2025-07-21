---
layout: default
title: 58_Настроим_GitLab_Runner_в_Kubernetes
---
<a class="back-link" href="../index.html">⬅ Назад к списку</a>


##  Настроим GitLab Runner в Kubernetes 

  
**1\. Установка Helm на свой ПК**  
  


Код:
    
    
    sudo wget https://get.helm.sh/helm-v3.12.1-linux-amd64.tar.gz

Код:
    
    
    sudo tar -xvzf helm-v3.12.1-linux-amd64.tar.gz -C /usr/local/bin --strip-components=1

Код:
    
    
    sudo helm version

**2\. Установка Kubectl**  
  


Код:
    
    
    sudo curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl

Код:
    
    
    sudo chmod +x ./kubectl

Код:
    
    
    sudo mv ./kubectl /usr/local/bin/kubectl

Код:
    
    
    sudo kubectl version --client

Код:
    
    
    sudo mkdir -p /root/.kube

Код:
    
    
    sudo nano /root/.kube/config

Проверка  
  


Код:
    
    
    sudo kubectl get nodes

![Нажмите на изображение для увеличения.  Название:	image_2984.png Просмотров:	0 Размер:	14.4 Кб ID:	3886](..\images\\img_3886_1720420036.png)​  
  
**3\. Добавим secret**  
  
Переходим в директорию с _[**Wildcard**](https://forum.kubeadm.ru/node/3514)_ корневым сертификатом  
  


Код:
    
    
    kubectl create secret generic wildcard-tls-kubeadm-ru \
    --namespace gitlab-runner \
    --from-file=kubeadm.ru_ca.crt

![Нажмите на изображение для увеличения.



Название:	Снимок экрана 2024-07-21 в 7.41.17.png

Просмотров:	17

Размер:	24.6 Кб

ID:	3899](..\images\\img_3899_1721537010.png)  
  


Код:
    
    
    kubectl create secret docker-registry harbor-pull-secret \
    --namespace gitlab-runner \
    --docker-server=harbor.kubeadm.ru \
    --docker-username=admin \
    --docker-password=Harbor12345 \
    --docker-email=admin@kubeadm.ru

**5\. Редактируем конфиг файл**  
  
  
Открываем веб интерфейс [_GitLab_](https://forum.kubeadm.ru/node/3604)  
  
![Нажмите на изображение для увеличения.  Название:	image_2929.png Просмотров:	0 Размер:	20.9 Кб ID:	3889](..\images\\img_3889_1719852817.png)  
  
![Нажмите на изображение для увеличения.  Название:	image_2928.png Просмотров:	0 Размер:	43.6 Кб ID:	3890](..\images\\img_3890_1719852783.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-07-20 в 9.53.52.png Просмотров:	0 Размер:	12.3 Кб ID:	3893](..\images\\img_3893_1721458556.png)  
  
**6\. Установка helm репозитория**  
  


Код:
    
    
    helm repo add gitlab https://charts.gitlab.io

Код:
    
    
    sudo helm search repo -l gitlab/gitlab-runner

Код:
    
    
    sudo helm show values gitlab/gitlab-runner --version 0.66.0 > values.yaml

Код:
    
    
    nano values.yaml

Код:
    
    
    registry: harbor.kubeadm.ru

Код:
    
    
    image: mirror.hub.docker.com/gitlab/gitlab-runner

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-07-20 в 11.04.36.png Просмотров:	0 Размер:	10.6 Кб ID:	3898](..\images\\img_3898_1721462710.png)  
  


Код:
    
    
    gitlabUrl: https://gitlab.kubeadm.ru

Код:
    
    
    runnerRegistrationToken: "glrt-XXXXXXXXX"

Код:
    
    
    certsSecretName: wildcard-tls-kubeadm-ru

Код:
    
    
    rbac:
    create: true

Код:
    
    
    name: "harbor-pull-secret"

**7\. Загружаем образ Gitlab Runner**  
  


Код:
    
    
    docker login -u admin -p Harbor12345 harbor.kubeadm.ru

Код:
    
    
    docker pull harbor.kubeadm.ru/mirror.hub.docker.com/gitlab/gitlab-runner:latest

**8\. Установка в Kubernetes**  
  


Код:
    
    
    sudo kubectl --kubeconfig ~/.kube/config create namespace gitlab-runner

При добавлении новых runner меняем имена gitlab-runner-02, gitlab-runner-03 и т.д.  
  


Код:
    
    
    sudo helm --kubeconfig ~/.kube/config install --namespace gitlab-runner gitlab-runner-01 -f values.yaml gitlab/gitlab-runner --version 0.66.0

​  
  
Проверим  
  
​  
  
  
  
**Поздравляю, настройка завершена!**


---

