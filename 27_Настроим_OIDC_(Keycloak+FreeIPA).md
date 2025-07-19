---
layout: default
title: 27_Настроим OIDC (Keycloak+FreeIPA)
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Настроим OIDC (Keycloak+FreeIPA) 

01-03-2025, 08:26 AM

Источник [тут](https://habr.com/ru/articles/716232/)  
Источник [тут](https://telegra.ph/Ustanovka-kontejnerizirovannyh-servisov-FreeIPA--KeyCloak-Single-Sign-On-03-10?ysclid=m5leobgf1b769557154)  
Источник [тут](https://habr.com/ru/articles/441112/)  
  
vCPU = 4  
vRAM = 4 Gb  
vHDD = 40 Gb  
  
**1\. Подготовим 1 виртуальную машину**  
  
Клонируем шаблон k8s-UbuntuTemplate  
  
Меняем IP и имена хостов на каждом узле  
  


Код:
    
    
    rm /etc/resolv.conf && nano /etc/resolv.conf

Код:
    
    
    nameserver 20.20.20.2

Код:
    
    
    nano /etc/netplan/01-netcfg.yaml

Код:
    
    
    20.20.20.4

Код:
    
    
    nano /etc/hostname

Код:
    
    
    keycloak

Код:
    
    
    reboot

**2\. Установка Docker & Docker-Compose**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/398)  
  
**3\. Покупаем Wildcard сертификат**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/3514)  
  
**4\. Обновляем сертификаты**  
  


Код:
    
    
    mkdir -p /media/data/keycloak

Код:
    
    
    nano /media/data/keycloak/keycloak.kubeadm.ru.crt

Код:
    
    
    nano /media/data/keycloak/keycloak.kubeadm.ru.key

Код:
    
    
    chmod 755 -R /media/data/keycloak/keycloak.kubeadm.ru.key

**5\. Загружаем[ _архив_](https://galkin-vladimir.ru:5446/d/s/11axXwvlUtKuEqZcEJQlt2rfPoVinsjV/_SCcZu5oonzhHMUVrg31LS_aCqZK5Kol-I_IAMOON8gs)**  
  
Копируем содержимое в файл **docker-compose.yml**  
  


Код:
    
    
    nano /root/docker-compose.yml

Код:
    
    
    docker-compose up -d

**!!! Ждем завершение процесса !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-01-03 в 9.55.12.png Просмотров:	0 Размер:	11.1 Кб ID:	4423](images\\img_4423_1735887356.jpg)  
  
**6\. Добавим запись на свой ПК**  
  
**Mac OS**  
  


Код:
    
    
    sudo nano /private/etc/hosts

Код:
    
    
    20.20.20.4 keycloak.kubeadm.ru

**7\. Проверим**  
  


Код:
    
    
    https://keycloak.kubeadm.ru

Код:
    
    
    login: admin
    pass: admin

**8\. Добавим новое пространство**  
  


Код:
    
    
    kubernetes

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 22.15.51.png Просмотров:	0 Размер:	13.3 Кб ID:	4464](images\\img_4464_1738437391.jpg)  
  
Удалим требование подтверждать e-mail  
  
Client scopes --> Email --> Mappers --> Email verified (Delete)  
  
**9\. Добавим User federation**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 22.17.47.png Просмотров:	0 Размер:	10.4 Кб ID:	4465](images\\img_4465_1738437559.jpg)  
  
**10\. Настроим подключение к LDAP серверу FreeIPA**  
  


Код:
    
    
    ldap://ldap.kubeadm.ru

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 22.19.49.png Просмотров:	0 Размер:	40.3 Кб ID:	4466](images\\img_4466_1738437665.jpg)  
  


Код:
    
    
    uid=service,cn=users,cn=accounts,dc=kubeadm,dc=ru

Вводим пароль от учетной записи [**service**](https://forum.kubeadm.ru/node/4426)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 22.25.03.png Просмотров:	0 Размер:	15.1 Кб ID:	4467](images\\img_4467_1738437968.jpg)  
  


Код:
    
    
    cn=users,cn=accounts,dc=kubeadm,dc=ru

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 22.26.25.png Просмотров:	0 Размер:	39.3 Кб ID:	4468](images\\img_4468_1738438015.jpg)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 22.27.08.png Просмотров:	0 Размер:	29.1 Кб ID:	4469](images\\img_4469_1738438052.jpg)  
  
**11\. Добавим параметр**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 22.30.16.png Просмотров:	0 Размер:	44.6 Кб ID:	4470](images\\img_4470_1738438297.jpg)  
  


Код:
    
    
    cn=groups,cn=accounts,dc=kubeadm,dc=ru

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 22.32.01.png Просмотров:	0 Размер:	42.4 Кб ID:	4471](images\\img_4471_1738438406.jpg)  
  
  
**12\. Синхронизируем пользователей**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 22.02.56.png Просмотров:	0 Размер:	38.3 Кб ID:	4474](images\\img_4474_1738438815.jpg)  
  
  
Проверим  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 22.35.13.png Просмотров:	0 Размер:	13.8 Кб ID:	4472](images\\img_4472_1738438568.jpg)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 22.36.17.png Просмотров:	0 Размер:	34.3 Кб ID:	4473](images\\img_4473_1738438606.jpg)  
  
  
**Поздравляю, настройка завершена!**


---

