---
layout: default
title: 26_Настроим LDAP аутентификацию (FreeIPA)
---
<a class="back-link" href="../index.html">⬅ Назад к списку</a>


##  Настроим LDAP аутентификацию (FreeIPA) 


Источник [тут](https://computingforgeeks.com/run-freeipa-server-in-docker-podman-containers/)  
Источник [тут](https://computingforgeeks.com/harbor-registry-ldap-integration/)  
Источник [тут](https://computingforgeeks.com/how-to-configure-gitlab-freeipa-authentication/)  
  
  
vCPU = 4  
vRAM = 4 Gb  
vHDD1 = 40 Gb  
  
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
    
    
    20.20.20.3

Код:
    
    
    nano /etc/hostname

Код:
    
    
    ldap

Код:
    
    
    rm /etc/hosts && nano /etc/hosts

Код:
    
    
    127.0.1.1 ldap.kubeadm.ru ldap
    127.0.0.1 localhost
    ::1     localhost

Код:
    
    
    reboot

Проверим  
  


Код:
    
    
    hostname -f

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-01-26 в 9.01.06.png Просмотров:	0 Размер:	5.0 Кб ID:	4444](..\images\\img_4444_1737871313.png)  
  
**2\. Установка Docker & Docker-Compose**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/398)  
  
**3\. Обновляем сертификаты**  
  


Код:
    
    
    mkdir -p /media/data/ldap

Код:
    
    
    nano /media/data/ldap/ldap.kubeadm.ru.crt

Копируем содержимое из консоли [_**ns**_](https://forum.kubeadm.ru/node/770)  
  


Код:
    
    
    cat /media/data/easy-rsa/pki/issued/ldap.kubeadm.ru.crt

Код:
    
    
    nano /media/data/ldap/ldap.kubeadm.ru.key

Копируем содержимое из консоли [_**ns**_](https://forum.kubeadm.ru/node/770)  
  


Код:
    
    
    cat /media/data/easy-rsa/pki/private/ldap.kubeadm.ru.key

Код:
    
    
    chmod 755 -R /media/data/ldap/ldap.kubeadm.ru.key

**4\. Отключим NTP клиента**  
  


Код:
    
    
    systemctl stop ntp && systemctl disable ntp

**5._Клонируем Git_**  
  


Код:
    
    
    git clone https://github.com/freeipa/freeipa-container.git

Код:
    
    
    cd freeipa-container

Код:
    
    
    docker build -t harbor.kubeadm.ru/freeipa/freeipa-alma8:latest -f Dockerfile.almalinux-8 .

Код:
    
    
    docker login -u admin -p Harbor12345 harbor.kubeadm.ru

Код:
    
    
    docker push "harbor.kubeadm.ru/freeipa/freeipa-alma8:latest"

**6\. Производим первичную настройку**  
  


Код:
    
    
    mkdir -p /media/data/ldap/ipa-central/data

Код:
    
    
    docker run --name freeipa-server -ti \
    -h ldap.kubeadm.ru \
    -p 53:53/udp \
    -p 53:53 \
    -p 80:80 \
    -p 443:443 \
    -p 389:389 \
    -p 636:636 \
    -p 88:88 \
    -p 88:88/udp \
    -p 464:464 \
    -p 464:464/udp \
    -p 123:123/udp \
    --read-only \
    --sysctl net.ipv6.conf.all.disable_ipv6=0 \
    -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
    -v /media/data/ldap/ipa-central/data:/data:Z \
    harbor.kubeadm.ru/freeipa/freeipa-alma8:latest

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-01-31 в 23.15.04.png Просмотров:	0 Размер:	65.1 Кб ID:	4449](..\images\\img_4449_1738354626.png)  
  
**!!! Вводим свои пароли !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-01-31 в 23.18.09.png Просмотров:	0 Размер:	19.8 Кб ID:	4450](..\images\\img_4450_1738354726.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-01-31 в 23.19.33.png Просмотров:	0 Размер:	46.5 Кб ID:	4451](..\images\\img_4451_1738354932.png)  
  
**!!! Ждем завершение процесса !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-01-31 в 23.01.18.png Просмотров:	0 Размер:	91.2 Кб ID:	4448](..\images\\img_4448_1738353740.png)  
  
**7\. Добавим новый узел в файл host на своём ПК**  
  
**MacOS**  
  


Код:
    
    
    sudo nano /private/etc/hosts

**Linux**  
  


Код:
    
    
    nano /etc/hosts

**Windows**  
  


Код:
    
    
    C:\Windows\System32\drivers\etc\hosts

!!! Имя домена вводим свое !!!  
  


Код:
    
    
    20.20.20.3 ldap.kubeadm.ru

**8\. Открываем Web интерфейс**  
  


Код:
    
    
    https://ldap.kubeadm.ru

Код:
    
    
    login: admin
    pass: твой пароль

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-01-31 в 23.28.58.png Просмотров:	0 Размер:	27.4 Кб ID:	4452](..\images\\img_4452_1738355658.png)  
  
**10\. Настроим файл для запуска**  
  
**!!! Соблюдаем отступы !!!**  
  


Код:
    
    
    nano /root/docker-compose.yml

Код:
    
    
    version: "3.9"
    services:
      "central-ipa":
        container_name: "ipa-central"
        image: harbor.kubeadm.ru/freeipa/freeipa-alma8:latest
        volumes:
          - "/sys/fs/cgroup:/sys/fs/cgroup:ro"
          - "/media/data/ldap/ipa-central/data:/data"
        read_only: true
        ports:
          - 53:53/udp
          - 53:53
          - 80:80
          - 443:443
          - 389:389
          - 636:636
          - 88:88
          - 88:88/udp
          - 464:464
          - 464:464/udp
          - 123:123/udp
        hostname: "ldap.kubeadm.ru"
        sysctls:
          net.ipv6.conf.all.disable_ipv6: 0

Код:
    
    
    docker-compose up -d

Проверим  
  


Код:
    
    
    https://ldap.kubeadm.ru

Код:
    
    
    login: admin
    pass: ваш пароль

**9\. Добавим обычного пользователя и служебного**  
  


Код:
    
    
    login: jane
    password: foo_password

Код:
    
    
    login: service
    password: ваш пароль

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 8.19.37.png Просмотров:	0 Размер:	35.8 Кб ID:	4454](..\images\\img_4454_1738387333.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 23.02.26.png Просмотров:	3 Размер:	43.4 Кб ID:	4475](..\images\\img_4475_1738440219.png)  
  
**10\. Настроим LDAP аутентификацию в Harbor**  
  


Код:
    
    
    ldap.kubeadm.ru

Код:
    
    
    uid=service,cn=users,cn=accounts,dc=kubeadm,dc=ru

Код:
    
    
    cn=users,cn=accounts,dc=kubeadm,dc=ru

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 8.29.18.png Просмотров:	0 Размер:	47.4 Кб ID:	4456](..\images\\img_4456_1738387906.png)  
  
Проверим  
  


Код:
    
    
    https://harbor.kubeadm.ru

Код:
    
    
    login: jane
    password: foo_password

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-04 в 14.38.13.png Просмотров:	0 Размер:	11.3 Кб ID:	4512](..\images\\img_4512_1738669119.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-04 в 14.39.02.png Просмотров:	0 Размер:	17.1 Кб ID:	4513](..\images\\img_4513_1738669183.png)  
  
**11\. Настроим LDAP аутентификацию в GitLab**  
  
Копируем и вставляем в начало файла.  
  
**!!! Соблюдаем отступы !!!**  
  


Код:
    
    
    nano /media/data/gitlab/config/gitlab.rb

Код:
    
    
    #
    gitlab_rails['ldap_enabled'] = true
    gitlab_rails['ldap_servers'] = YAML.load <<-'EOS'
      main:
        label: 'LDAP'
        host: 'ldap.kubeadm.ru'
        port: 389
        uid: 'uid'
        method: 'tls'
        bind_dn: 'uid=service,cn=users,cn=accounts,dc=kubeadm,dc=ru '
        password: '**ваш пароль** '
        encryption: 'plain'
        base: 'cn=accounts,dc=kubeadm,dc=ru'
        verify_certificates: false
        attributes:
          username: ['uid']
          email: ['mail']
          name: 'displayName'
          first_name: 'givenName'
          last_name: 'sn'
     EOS
    #

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 10.20.21.png Просмотров:	0 Размер:	75.0 Кб ID:	4463](..\images\\img_4463_1738395090.png)  
  


Код:
    
    
    docker-compose restart

Код:
    
    
    docker exec -ti gitlab_app /bin/bash

Код:
    
    
    gitlab-rake gitlab:ldap:check

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-01 в 10.00.15.png Просмотров:	0 Размер:	29.0 Кб ID:	4461](..\images\\img_4461_1738393278.png)  
  
Проверим  
  


Код:
    
    
    https://gitlab.kubeadm.ru

Код:
    
    
    login: jane
    password: foo_password

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-04 в 9.33.46.png Просмотров:	0 Размер:	11.1 Кб ID:	4507](..\images\\img_4507_1738664558.png)  
  
  
  
**Поздравляю, настройка завершена!**


---

