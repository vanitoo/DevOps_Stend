---
layout: default
title: 09_Настройка Harbor (Ubuntu 20.04)
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Настройка Harbor (Ubuntu 20.04) 

03-03-2023, 10:55 AM

Источник [тут](https://goharbor.io/docs/2.5.0/install-config/configure-https/)  
  
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
    
    
    20.20.20.55

Код:
    
    
    nano /etc/hostname

Код:
    
    
    harbor

Код:
    
    
    reboot

**1\. Установка Docker & Docker-Compose**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/398)  
  
**2\. Скачиваем и распакуем инсталлятор Harbor**  
  


Код:
    
    
    mkdir -p /media/data/harbor

Код:
    
    
    cd /root

Код:
    
    
    wget https://github.com/goharbor/harbor/releases/download/v2.4.1/harbor-offline-installer-v2.4.1.tgz

Код:
    
    
    tar -xvzf harbor-offline-installer-v2.4.1.tgz -C /media/data/harbor --strip-components=1

**3\. Настроим минимальный конфиг**  
  


Код:
    
    
    mkdir -p /media/data/harbor-data

Код:
    
    
    cp /media/data/harbor/harbor.yml.tmpl /media/data/harbor/harbor.yml

**!!! Имя домена вводим свое !!!**  
  


Код:
    
    
    nano /media/data/harbor/harbor.yml

Код:
    
    
    /media/data/cert/harbor.kubeadm.ru.crt
    /media/data/cert/harbor.kubeadm.ru.key

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-25 в 14.17.38.png Просмотров:	0 Размер:	46.6 Кб ID:	2221](images\\img_2221_1690283921.png)  
  


Код:
    
    
    /media/data/harbor-data

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-25 в 14.20.32.png Просмотров:	0 Размер:	5.5 Кб ID:	2222](images\\img_2222_1690284067.png)  
  
**4\. Покупаем Wildcard сертификат**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/3514)  
  
**5\. Добавляем SSL сертификаты**  
  
  


Код:
    
    
    mkdir -p /media/data/cert

Копируем содержимое сертификатов  
  


Код:
    
    
    nano /usr/local/share/ca-certificates/ca.crt

Код:
    
    
    nano /media/data/cert/harbor.kubeadm.ru.crt

Код:
    
    
    nano /media/data/cert/harbor.kubeadm.ru.key

Код:
    
    
    chown www-data:www-data -R /media/data/cert
    chmod 777 -R /media/data/cert

Код:
    
    
    update-ca-certificates --fresh

**5\. Выполним установку**  
  


Код:
    
    
    cd /media/data/harbor

Код:
    
    
    chmod +x ./install.sh

Код:
    
    
    ./install.sh

**!!! Ждем завершения процесса !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-25 в 14.42.11.png Просмотров:	0 Размер:	38.8 Кб ID:	2226](images\\img_2226_1690285422.png)  
  
**6\. Добавим новый узел в файл host на своём ПК**  
  
**MacOS**  
  


Код:
    
    
    sudo nano /private/etc/hosts

**Linux**  
  


Код:
    
    
    nano /etc/hosts

**Windows**  
  


Код:
    
    
    C:\Windows\System32\drivers\etc\hosts

**!!! Имя домена вводим свое !!!**  
  


Код:
    
    
    20.20.20.55 harbor.kubeadm.ru

**7\. Откроем в браузере по имени узла**  
  


Код:
    
    
    https://harbor.kubeadm.ru

В водим логин и пароль  
  


Код:
    
    
    admin
    Harbor12345

  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-05-03 в 12.28.35.png Просмотров:	0 Размер:	11.1 Кб ID:	1482](images\\img_1482_1683106253.png)  
  
**!!! Если после рестарта виртуальной машины нет доступа к веб интерфейсу, выполните рестар контейнеров !!!**  
  


Код:
    
    
    cd /media/data/harbor

Код:
    
    
    docker-compose restart

  
**8\. Сбросим пароль (по желанию)**  
  


Код:
    
    
    docker exec -it harbor-db bash

Код:
    
    
    psql -U postgres -d registry

Код:
    
    
    update harbor_user set salt='', password='Harbor12345' where user_id = 1;

Код:
    
    
    \q

Код:
    
    
    exit

Код:
    
    
    cd /media/data/harbor

Код:
    
    
    docker-compose restart

**9\. Обновляем сертификат (по желанию)**  
  


Код:
    
    
    cd /media/data/harbor

Код:
    
    
    ./prepare

Код:
    
    
    docker-compose restart

**Поздравляю! настройка завершена.**

Вложения 

  * [ ![Нажмите на изображение для увеличения.



Название:	Снимок экрана 2023-07-25 в 12.59.41.png

Просмотров:	287

Размер:	7.2 Кб

ID:	2227](images\\img_2227_0.png) ](filedata/fetch?id=2227)
  * [ ![Нажмите на изображение для увеличения.



Название:	Снимок экрана 2023-07-25 в 15.01.43.png

Просмотров:	283

Размер:	7.7 Кб

ID:	2228](images\\img_2228_0.png) ](filedata/fetch?id=2228)




---

