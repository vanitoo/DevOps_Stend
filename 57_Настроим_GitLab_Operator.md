---
layout: default
title: 57_Настроим_GitLab_Operator
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Настроим GitLab Operator 


Источник [тут](https://docs.gitlab.com/operator/installation.html?tab=Kubernetes)  
  
**1\. Установим Cert-Manager**  
  
**Для MacOS**  
  
В консоли терминала на своем ПК  
  


Код:
    
    
    sudo kubectl --kubeconfig ~/.kube/config apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.5/cert-manager.yaml

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-05-19 в 9.27.20.png Просмотров:	0 Размер:	52.1 Кб ID:	3563](images\\img_3563_1716100092.png)  
  
**2\. Устанавливаем оператор**  
  
Проверим актуальную версию [тут](https://gitlab.com/gitlab-org/cloud-native/gitlab-operator/-/releases)  
  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-05-19 в 10.15.39.png Просмотров:	0 Размер:	60.0 Кб ID:	3564](images\\img_3564_1716103027.png)  
  
**Для MacOS**  
  
В консоли терминала на своем ПК  
  


Код:
    
    
    sudo kubectl --kubeconfig ~/.kube/config create namespace gitlab-system

Код:
    
    
    GL_OPERATOR_VERSION=1.0.0

Код:
    
    
    PLATFORM=kubernetes

Код:
    
    
    sudo kubectl --kubeconfig ~/.kube/config apply -f https://gitlab.com/api/v4/projects/18899486/packages/generic/gitlab-operator/${GL_OPERATOR_VERSION}/gitlab-operator-${PLATFORM}-${GL_OPERATOR_VERSION}.yaml

**!!! Ждем завершение процесса !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-04-20 в 20.12.39.png Просмотров:	0 Размер:	40.0 Кб ID:	3320](images\\img_3320_1713633249.png)  
  
  
**3\. Настроим свой конфиг**  
  
Источник [тут](https://docs.gitlab.com/operator/installation.html)  
  


Код:
    
    
    apiVersion: apps.gitlab.com/v1beta1
    kind: GitLab
    metadata:
      name: gitlab
      namespace: gitlab-system
    spec:
      chart:
        version: "8.0.0"
        values:
          nginx-ingress:
            enabled: false
            hosts:
              domain: kubeadm.ru
            ingress:
              configureCertmanager: false
          certmanager-issuer:
            email: admin@kubeadm.ru

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-05-19 в 10.20.30.png Просмотров:	6 Размер:	35.5 Кб ID:	3565](images\\img_3565_1716103262.png)  
  
**!!! Ждем завершение процесса !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-04-25 в 22.00.58.png Просмотров:	3 Размер:	47.7 Кб ID:	3328](images\\img_3328_1714071778.png)  
  
**4\. Открываем веб интерфейс**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-05-06 в 18.16.16.png Просмотров:	4 Размер:	86.8 Кб ID:	3432](images\\img_3432_1715008634.png)  
  
Добавляем записи на свой ПК  
  


Код:
    
    
    sudo nano /private/etc/hosts

Код:
    
    
    10.10.10.78 gitlab.kubeadm.ru

Код:
    
    
    https://gitlab.kubeadm.ru

Логин  
  


Код:
    
    
    root

Пароль для первого входа из секрета  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-05-06 в 17.20.00.png Просмотров:	0 Размер:	57.1 Кб ID:	3429](images\\img_3429_1715005278.png)  
  
  
**Поздравляю, настройка завершена!**


---

