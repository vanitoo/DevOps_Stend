---
layout: default
title: 55_Настроим_CICD_Jenkins
---


##  Настроим CI/CD Jenkins 

12-22-2024, 08:53 AM

Источник [тут](https://timeweb.cloud/tutorials/ci-cd/avtomatizaciya-nastrojki-jenkins-s-pomoshchyu-docker?ysclid=m4z4ftvq2j495832749)  
Источник [тут](https://dev.to/andresfmoya/install-jenkins-using-docker-compose-4cab?ysclid=m4z69ezjq7421661973)  
  
vCPU = 4  
vRAM = 8 Gb  
vHDD = 40 Gb  
  
**1\. Подготовим 1 виртуальную машину**  
  
Клонируем шаблон k8s-UbuntuTemplate  
  
**!!! Добавляем оперативной памяти !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-22 в 8.55.17.png Просмотров:	0 Размер:	53.4 Кб ID:	4398](images\\img_4398_1734846989.jpg)  
  
Меняем IP и имена хостов на каждом узле  
  


Код:
    
    
    rm /etc/resolv.conf && nano /etc/resolv.conf

Код:
    
    
    nameserver 20.20.20.2

Код:
    
    
    nano /etc/netplan/01-netcfg.yaml

Код:
    
    
    20.20.20.51

Код:
    
    
    nano /etc/hostname

Код:
    
    
    jenkins

Код:
    
    
    reboot

**2\. Установка Docker & Docker-Compose**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/398)  
  
**3\. Настроим Docker-Compose**  
  


Код:
    
    
    mkdir -p /media/data/jenkins

Код:
    
    
    nano docker-compose.yml

Код:
    
    
    version: '3.9'
    #*****************************************************************************
    services:
      jenkins:
        image: 'harbor.kubeadm.ru/mirror.docker.hub/jenkins/jenkins:lts'
        privileged: true
        user: root
        container_name: jenkins-server
        ports:
          - "8081:8080"
          - "50000:50000"
        volumes:
          - "/media/data/jenkins/home:/var/jenkins_home"
        networks:
          - jenkins-network
    #*****************************************************************************
      jenkins-agent:
        image: 'harbor.kubeadm.ru/mirror.docker.hub/jenkins/inbound-agent'
        container_name: jenkins-agent
        environment:
          - JENKINS_URL=http://20.20.20.51:8081
          - JENKINS_AGENT_NAME=agent
          - JENKINS_AGENT_WORKDIR=/home/jenkins/agent
          #- JENKINS_SECRET=
        volumes:
          - "/media/data/jenkins/agent:/home/jenkins/agent"
        depends_on:
          - jenkins
        networks:
          - jenkins-network
    #*****************************************************************************
    networks:
      jenkins-network:

Код:
    
    
    docker-compose up -d

Проверим  
  


Код:
    
    
    http://20.20.20.51:8081

Код:
    
    
    login: root
    pass: из консоли

Код:
    
    
    cat /media/data/jenkins/home/secrets/initialAdminPassword

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-22 в 9.40.29.png Просмотров:	0 Размер:	11.3 Кб ID:	4399](images\\img_4399_1734849656.jpg)  
  
**4\. Настроим Jenkins**  
  
Выбераем «Install suggested plugins».  
  
**!!! Ждем завершение процесса !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-22 в 9.43.04.png Просмотров:	0 Размер:	78.3 Кб ID:	4400](images\\img_4400_1734849831.jpg)  
  
Пропускаем настройку первого пользователя  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-22 в 9.45.55.png Просмотров:	0 Размер:	3.8 Кб ID:	4401](images\\img_4401_1734850149.jpg)  
  
Принимаем настройку  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-22 в 9.47.22.png Просмотров:	0 Размер:	53.0 Кб ID:	4402](images\\img_4402_1734850174.jpg)  
  
**!!! Меняем на свой логин и пароль !!!**  
  
**5\. Настроим агент**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-22 в 9.55.09.png Просмотров:	0 Размер:	77.7 Кб ID:	4403](images\\img_4403_1734850632.jpg)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-22 в 9.57.28.png Просмотров:	0 Размер:	49.8 Кб ID:	4404](images\\img_4404_1734850686.jpg)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-22 в 9.59.17.png Просмотров:	0 Размер:	50.2 Кб ID:	4405](images\\img_4405_1734850788.jpg)  
  
  


Код:
    
    
    /home/jenkins/agent

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-22 в 10.02.18.png Просмотров:	0 Размер:	44.2 Кб ID:	4406](images\\img_4406_1734851042.jpg)  
  
**6\. Подключаем агент**  
  
**!!! Копируем ключ !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-22 в 10.06.57.png Просмотров:	0 Размер:	44.8 Кб ID:	4407](images\\img_4407_1734851276.jpg)  
  
Добавляем в переменные  
  


Код:
    
    
    nano docker-compose.yml

Код:
    
    
    - JENKINS_SECRET=

**!!! Соблюдаем отступы !!!**  
  
![Нажмите на изображение для увеличения.



Название:	Снимок экрана 2024-12-22 в 10.26.59.png

Просмотров:	5

Размер:	41.9 Кб

ID:	4411](images\\img_4411_1734852517.jpg)  
  
Перезапускаем Docker-Compose  
  


Код:
    
    
    docker-compose restart

  
  
**Поздравляю! настройка завершена.**


---

