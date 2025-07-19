---
layout: default
title: 12_Настройка GitLab Runner (v14.4.0)
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Настройка GitLab Runner (v14.4.0) 

02-13-2022, 07:33 PM

vCPU = 4  
vRAM = 4 Gb  
vHDD = 40 Gb  
  
**Подготовим 1 виртуальную машину**  
  
Клонируем шаблон k8s-UbuntuTemplate  
  
Меняем IP и имена хостов на каждом узле  
  


Код:
    
    
    rm /etc/resolv.conf && nano /etc/resolv.conf

Код:
    
    
    nameserver 20.20.20.2

Код:
    
    
    nano /etc/netplan/01-netcfg.yaml

Код:
    
    
    20.20.20.41

Код:
    
    
    nano /etc/hostname

Код:
    
    
    runner01

Код:
    
    
    reboot

**1\. Установка Docker & Docker-Compose**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/398)  
  
**2\. Покупаем Wildcard сертификат**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/3514)  
  
**3\. Добавляем корневые сертификаты**  
  
Копируем содержимое сертификатов  
  


Код:
    
    
    nano /usr/local/share/ca-certificates/ca.crt

Код:
    
    
    update-ca-certificates --fresh

Код:
    
    
    mkdir -p /etc/gitlab-runner/certs/client

Код:
    
    
    cp /usr/local/share/ca-certificates/ca.crt /etc/gitlab-runner/certs/client/ca.crt

**!!! Имя домена вводим свое !!!**  
  


Код:
    
    
    mkdir -p /etc/docker/certs.d/harbor.kubeadm.ru

Код:
    
    
    cp /usr/local/share/ca-certificates/ca.crt /etc/docker/certs.d/harbor.kubeadm.ru/ca.crt

**4\. Загружаем runner**  
  


Код:
    
    
    curl -L https://s3.dualstack.us-east-1.amazonaws.com/gitlab-runner-downloads/**v14.4.0** /binaries/gitlab-runner-linux-386 > /usr/local/bin/gitlab-runner

**5\. Настройка**  
  


Код:
    
    
    chmod +x /usr/local/bin/gitlab-runner

Код:
    
    
    useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash

Код:
    
    
    gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner

Код:
    
    
    gitlab-runner start

**6\. Получим наш токен**  
  
Нужно выбрать как мы будем привязывать runner  
  
Все runner будут **общими** или у каждого проекта будет **свой** (персональный) runner.  
  
  
**Общий для всех проектов**  
  
Откроем в браузере  
  


Код:
    
    
    [https://gitlab.kubeadm.ru](https://gitlab.kubeadm.ru)

![Нажмите на изображение для увеличения.  Название:	3.png Просмотров:	2 Размер:	31.7 Кб ID:	619](images\\img_619_1644733343.png)  
  
  
![Нажмите на изображение для увеличения.  Название:	4.png Просмотров:	2 Размер:	52.3 Кб ID:	620](images\\img_620_1644733469.png)  
  
**7\. Копируем свой токен**  
  
![Нажмите на изображение для увеличения.  Название:	5.png Просмотров:	2 Размер:	21.6 Кб ID:	621](images\\img_621_1644733553.png)  
  
**Персональный**  
  
![Нажмите на изображение для увеличения.  Название:	экрана 2022-02-23 в 9.17.15.png Просмотров:	0 Размер:	83.4 Кб ID:	787](images\\img_787_1645597218.png)  
  
![Нажмите на изображение для увеличения.  Название:	экрана 2022-02-23 в 9.31.50.png Просмотров:	0 Размер:	117.7 Кб ID:	788](images\\img_788_1645597978.png)  
  
**8\. Регистрация Runner**  
  
  
Заменяем --url - своим доменом!  
Заменяем XXXXXXXXXXXX - своим токеном!  
  
  


Код:
    
    
    rm -r /etc/gitlab-runner

Код:
    
    
    gitlab-runner register -n \
    --url https://gitlab.kubeadm.ru/ \
    --registration-token XXXXXXXXXXXX \
    --executor docker \
    --description "Runner01" \
    --docker-image "harbor.kubeadm.ru/mirror.docker.hub/library/docker:latest" \
    --docker-privileged \
    --docker-tlsverify \
    --tls-ca-file "/etc/gitlab-runner/certs/client/ca.crt" \
    --docker-volumes "/cache" \
    --docker-volumes "/certs/client" \
    --docker-volumes "/etc/docker/certs.d:/etc/docker/certs.d:ro"

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-09-29 в 7.17.43.png Просмотров:	0 Размер:	16.7 Кб ID:	3966](images\\img_3966_1727583595.png)  
  


Код:
    
    
    reboot

**9\. Проверим регистрацию**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-25 в 12.50.44.png Просмотров:	0 Размер:	55.7 Кб ID:	2219](images\\img_2219_1690278717.png)  
  
**10\. Ограничим использование проектом только своим runner (по желанию)**  
  
![Нажмите на изображение для увеличения.  Название:	экрана 2022-02-23 в 10.45.03.png Просмотров:	2 Размер:	142.9 Кб ID:	794](images\\img_794_1645602465.png)  
  
  
**11\. Очистка**  
  


Код:
    
    
    cd /root

Код:
    
    
    nano /root/clean.sh

Код:
    
    
    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)
    docker rmi $(docker images -q)

Код:
    
    
    chmod u+x clean.sh

Код:
    
    
    nano /etc/crontab

Код:
    
    
    00 23 * * * root sh /root/clean.sh

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-10-08 в 8.18.26.png Просмотров:	0 Размер:	81.8 Кб ID:	2735](images\\img_2735_1696742459.png)  
  


Код:
    
    
    systemctl restart cron

Код:
    
    
    systemctl status cron

  
**Поздравляю, настройка завершена!**

Вложения 

  * [ ![Нажмите на изображение для увеличения.



Название:	экрана 2022-02-20 в 8.21.33.png

Просмотров:	299

Размер:	68.7 Кб

ID:	766](images\\img_766_0.png) ](filedata/fetch?id=766)
  * [ ![Нажмите на изображение для увеличения.



Название:	экрана 2022-02-20 в 11.50.13.png

Просмотров:	288

Размер:	3.4 Кб

ID:	767](images\\img_767_0.png) ](filedata/fetch?id=767)
  * [ ![Нажмите на изображение для увеличения.



Название:	3.png

Просмотров:	290

Размер:	31.7 Кб

ID:	783](images\\img_783_0.png) ](filedata/fetch?id=783)
  * [ ![Нажмите на изображение для увеличения.



Название:	1.png

Просмотров:	297

Размер:	28.0 Кб

ID:	821](images\\img_821_0.png) ](filedata/fetch?id=821)




---

