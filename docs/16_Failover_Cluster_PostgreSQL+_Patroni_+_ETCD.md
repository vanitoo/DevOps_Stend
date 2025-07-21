---
layout: default
title: 16_Failover Cluster PostgreSQL+ Patroni + ETCD
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Failover Cluster PostgreSQL+ Patroni + ETCD 


**1\. Подготовим 3 виртуальных машины**  
  
Клонируем шаблон k8s-UbuntuTemplate  
  
3 - pg ноды  
  
vCPU = 4  
vRAM = 4 Gb  
vHDD = 40 Gb  
vHDD = 100 Gb  
  
**!!! Добавляем диск !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-10-18 в 13.56.41.png Просмотров:	1 Размер:	65.3 Кб ID:	4128](..\images\\img_4128_1729249084.png)  
  
Убедимся в наличие диска  
  


Код:
    
    
    lsblk

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-18 в 21.39.35.png Просмотров:	0 Размер:	13.9 Кб ID:	4182](..\images\\img_4182_1731955235.png)  
  


Код:
    
    
    fdisk /dev/sdb

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-18 в 21.45.18.png Просмотров:	0 Размер:	96.8 Кб ID:	4184](..\images\\img_4184_1731955939.png)  
  


Код:
    
    
    mkfs.ext4 /dev/sdb1

**!!! Ждем завершение процесса !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-18 в 21.52.52.png Просмотров:	0 Размер:	51.5 Кб ID:	4185](..\images\\img_4185_1731956036.png)  
  


Код:
    
    
    mkdir -p /media/data

Код:
    
    
    mount /dev/sdb1 /media/data

Проверим  
  


Код:
    
    
    df -h /dev/sdb1

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-18 в 21.56.45.png Просмотров:	0 Размер:	17.7 Кб ID:	4186](..\images\\img_4186_1731956252.png)  
  


Код:
    
    
    blkid

**!!! Копируем только содержимое строки !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-18 в 21.57.50.png Просмотров:	0 Размер:	27.2 Кб ID:	4187](..\images\\img_4187_1731956407.png)  
  


Код:
    
    
    nano /etc/fstab

Добавляем в конец файла:  
  


Код:
    
    
    /media/data ext4 rw 0 1

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-18 в 22.01.39.png Просмотров:	8 Размер:	45.5 Кб ID:	4188](..\images\\img_4188_1731956555.png)  
  
Меняем IP и имена хостов на каждом узле  
  


Код:
    
    
    rm /etc/resolv.conf && nano /etc/resolv.conf

Код:
    
    
    nameserver 20.20.20.2

Код:
    
    
    nano /etc/netplan/01-netcfg.yaml

Код:
    
    
    20.20.20.24

Код:
    
    
    nano /etc/hostname

Код:
    
    
    pg01

Код:
    
    
    reboot

**!!! pg02 и pg03 настраиваем аналогично !!!**  
  
**2\. Добавим имена хостов на все ноды**  
  


Код:
    
    
    rm /etc/hosts && nano /etc/hosts

Код:
    
    
    127.0.0.1       localhost
    ::1     localhost
    #
    20.20.20.24 pg01
    20.20.20.25 pg02
    20.20.20.26 pg03
    #

**3\. Установка ETCD-кластера**  
  
Выполним настройку на все ноды  
  


Код:
    
    
    cd /root

Код:
    
    
    wget https://github.com/coreos/etcd/releases/download/v3.3.10/etcd-v3.3.10-linux-amd64.tar.gz

Код:
    
    
    tar -xvf etcd-v3.3.10-linux-amd64.tar.gz -C /usr/local/bin/ --strip-components=1

Код:
    
    
    mkdir -p /media/data/log/etcd

**4\. Добавьте содержимое в файл на каждой ноде!**  
  
Выполним настройку на все ноды  
  


Код:
    
    
    touch /etc/etcd.env && echo PEER_NAME=$(hostname)> /etc/etcd.env && echo PRIVATE_IP=$(hostname -i)>> /etc/etcd.env

**!!! Внимательно редактируем !!!**  
  
**!!! Настройка для pg01 !!!**  
  


Код:
    
    
    nano /etc/systemd/system/etcd.service

Код:
    
    
    [Unit]
    Description=etcd
    Documentation=https://github.com/coreos/etcd
    Conflicts=etcd.service
    Conflicts=etcd2.service
    
    [Service]
    EnvironmentFile=/etc/etcd.env
    Type=notify
    Restart=always
    RestartSec=5s
    LimitNOFILE=40000
    TimeoutStartSec=0
    SyslogIdentifier=etcd
    
    ExecStart=/usr/local/bin/etcd\
    --name pg01\
    --data-dir /media/data/etcd\
    --listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001\
    --advertise-client-urls http://20.20.20.24:2379,http://20.20.20.24:4001\
    --listen-peer-urls http://0.0.0.0:2380\
    --initial-advertise-peer-urls http://20.20.20.24:2380\
    --initial-cluster pg01=http://20.20.20.24:2380,pg02=http://20.20.20.25:2380,pg03=http://20.20.20.26:2380\
    --initial-cluster-token 9489bf67bdfe1b3ae077d6fd9e7efefd\
    --initial-cluster-state new
    
    [Install]
    WantedBy=multi-user.target

**!!! Настройка для pg02 !!!**  
  


Код:
    
    
    nano /etc/systemd/system/etcd.service

Код:
    
    
    [Unit]
    Description=etcd
    Documentation=https://github.com/coreos/etcd
    Conflicts=etcd.service
    Conflicts=etcd2.service
    
    [Service]
    EnvironmentFile=/etc/etcd.env
    Type=notify
    Restart=always
    RestartSec=5s
    LimitNOFILE=40000
    TimeoutStartSec=0
    SyslogIdentifier=etcd
    
    ExecStart=/usr/local/bin/etcd\
    --name pg02\
    --data-dir /media/data/etcd\
    --listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001\
    --advertise-client-urls http://20.20.20.25:2379,http://20.20.20.25:4001\
    --listen-peer-urls http://0.0.0.0:2380\
    --initial-advertise-peer-urls http://20.20.20.25:2380\
    --initial-cluster pg01=http://20.20.20.24:2380,pg02=http://20.20.20.25:2380,pg03=http://20.20.20.26:2380\
    --initial-cluster-token 9489bf67bdfe1b3ae077d6fd9e7efefd\
    --initial-cluster-state new
    
    [Install]
    WantedBy=multi-user.target

**!!! Настройка для pg03 !!!**  
  


Код:
    
    
    nano /etc/systemd/system/etcd.service

Код:
    
    
    [Unit]
    Description=etcd
    Documentation=https://github.com/coreos/etcd
    Conflicts=etcd.service
    Conflicts=etcd2.service
    
    [Service]
    EnvironmentFile=/etc/etcd.env
    Type=notify
    Restart=always
    RestartSec=5s
    LimitNOFILE=40000
    TimeoutStartSec=0
    SyslogIdentifier=etcd
    
    ExecStart=/usr/local/bin/etcd\
    --name pg03\
    --data-dir /media/data/etcd\
    --listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001\
    --advertise-client-urls http://20.20.20.26:2379,http://20.20.20.26:4001\
    --listen-peer-urls http://0.0.0.0:2380\
    --initial-advertise-peer-urls http://20.20.20.26:2380\
    --initial-cluster pg01=http://20.20.20.24:2380,pg02=http://20.20.20.25:2380,pg03=http://20.20.20.26:2380\
    --initial-cluster-token 9489bf67bdfe1b3ae077d6fd9e7efefd\
    --initial-cluster-state new
    
    [Install]
    WantedBy=multi-user.target

**5\. Включаем автозагрузку и запускаем базу ETCD на всех нодах!**  
  
Выполним настройку на все ноды  
  


Код:
    
    
    chown -R root:root /usr/local/bin/etcd
    chmod 777 /usr/local/bin/etcd

Код:
    
    
    systemctl enable etcd.service

Код:
    
    
    systemctl daemon-reload

Код:
    
    
    systemctl start etcd

Код:
    
    
    systemctl status etcd

[Ctrl]+[C]  
  
**6\. Проверим работу кластера:**  
  


Код:
    
    
    etcdctl cluster-health

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-10-20 в 7.00.12.png Просмотров:	0 Размер:	26.9 Кб ID:	4129](..\images\\img_4129_1729396895.png)  
  
**7\. Установка PostgreSQL v13 и Patroni**  
  
Выполним настройку на все ноды  
  


Код:
    
    
    sh -c 'echo "deb <http://apt.postgresql.org/pub/repos/apt> $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

Код:
    
    
    wget --quiet -O - <https://www.postgresql.org/media/keys/ACCC4CF8.asc> | sudo apt-key add -

Код:
    
    
    apt-get update && apt-get install -y postgresql-13 postgresql-server-dev-13

Код:
    
    
    systemctl stop postgresql

Код:
    
    
    ln -s /usr/lib/postgresql/13/bin/* /usr/sbin/

**8\. Install Patroni**  
  
Выполним настройку на все ноды  
  


Код:
    
    
    apt-get update && apt-get install -y python3-pip

Код:
    
    
    pip install psycopg

Код:
    
    
    pip install patroni

Код:
    
    
    pip install patroni[etcd]

Код:
    
    
    mkdir -p /media/data/patroni
    mkdir -p /media/data/log/patroni
    mkdir -p /media/data/log/postgresql

Код:
    
    
    chown -R postgres:postgres /media/data
    chmod 777 /media/data
    chmod 700 /media/data/patroni

**9\. Копируем содержимое файлов в соответствии каждой ноде!**  
  
Выполним настройку на все ноды  
  


Код:
    
    
    nano /etc/patroni.yml

**!!! Настройка для pg01 !!!**  
  


Код:
    
    
    scope: postgres
    namespace: /pg_cluster/
    name: pg01
    
    restapi:
      listen: 20.20.20.24:8008
      connect_address: 20.20.20.24:8008
    
    etcd:
      hosts:
        - 20.20.20.24:2379
        - 20.20.20.25:2379
        - 20.20.20.26:2379
    
    bootstrap:
      dcs:
        ttl: 30
        loop_wait: 10
        retry_timeout: 10
        maximum_lag_on_failover: 1048576
        postgresql:
          use_pg_rewind: true
          parameters:
    
      initdb:
        - encoding: UTF8
        - data-checksums
    
      pg_hba:
        - host replication replicator 127.0.0.1/32 md5
        - host replication replicator 20.20.20.24/0 md5
        - host replication replicator 20.20.20.25/0 md5
        - host replication replicator 20.20.20.26/0 md5
        - host all all 0.0.0.0/0 md5
    
      users:
        admin:
          password: admin
          options:
            - createrole
            - createdb
    
    postgresql:
      listen: 20.20.20.24:5432
      connect_address: 20.20.20.24:5432
      data_dir: /media/data/patroni
      bin_dir: /usr/sbin/
      pgpass: /tmp/pgpass0
      authentication:
        replication:
          username: replicator
          password: reppassword
        superuser:
          username: postgres
          password: secretpassword
      parameters:
    
    tags:
      nofailover: false
      noloadbalance: false
      clonefrom: false
      nosync: false

**!!! Настройка для pg02 !!!**  
  


Код:
    
    
    scope: postgres
    namespace: /pg_cluster/
    name: pg02
    
    restapi:
      listen: 20.20.20.25:8008
      connect_address: 20.20.20.25:8008
    
    etcd:
      hosts:
        - 20.20.20.24:2379
        - 20.20.20.25:2379
        - 20.20.20.26:2379
    
    bootstrap:
      dcs:
        ttl: 30
        loop_wait: 10
        retry_timeout: 10
        maximum_lag_on_failover: 1048576
        postgresql:
          use_pg_rewind: true
          parameters:
    
      initdb:
        - encoding: UTF8
        - data-checksums
    
      pg_hba:
        - host replication replicator 127.0.0.1/32 md5
        - host replication replicator 20.20.20.24/0 md5
        - host replication replicator 20.20.20.25/0 md5
        - host replication replicator 20.20.20.26/0 md5
        - host all all 0.0.0.0/0 md5
    
      users:
        admin:
          password: admin
          options:
            - createrole
            - createdb
    
    postgresql:
      listen: 20.20.20.25:5432
      connect_address: 20.20.20.25:5432
      data_dir: /media/data/patroni
      bin_dir: /usr/sbin/
      pgpass: /tmp/pgpass0
      authentication:
        replication:
          username: replicator
          password: reppassword
        superuser:
          username: postgres
          password: secretpassword
      parameters:
    
    tags:
      nofailover: false
      noloadbalance: false
      clonefrom: false
      nosync: false

**!!! Настройка для pg03 !!!**  
  


Код:
    
    
    scope: postgres
    namespace: /pg_cluster/
    name: pg03
    
    restapi:
      listen: 20.20.20.26:8008
      connect_address: 20.20.20.26:8008
    
    etcd:
      hosts:
        - 20.20.20.24:2379
        - 20.20.20.25:2379
        - 20.20.20.26:2379
    
    bootstrap:
      dcs:
        ttl: 30
        loop_wait: 10
        retry_timeout: 10
        maximum_lag_on_failover: 1048576
        postgresql:
          use_pg_rewind: true
          parameters:
    
      initdb:
        - encoding: UTF8
        - data-checksums
    
      pg_hba:
        - host replication replicator 127.0.0.1/32 md5
        - host replication replicator 20.20.20.24/0 md5
        - host replication replicator 20.20.20.25/0 md5
        - host replication replicator 20.20.20.26/0 md5
        - host all all 0.0.0.0/0 md5
    
      users:
        admin:
          password: admin
          options:
            - createrole
            - createdb
    
    postgresql:
      listen: 20.20.20.26:5432
      connect_address: 20.20.20.26:5432
      data_dir: /media/data/patroni
      bin_dir: /usr/sbin/
      pgpass: /tmp/pgpass0
      authentication:
        replication:
          username: replicator
          password: reppassword
        superuser:
          username: postgres
          password: secretpassword
      parameters:
    
    tags:
    nofailover: false
    noloadbalance: false
    clonefrom: false
    nosync: false

**11\. Создаём сервис**  
  
Выполним настройку на все ноды  
  


Код:
    
    
    nano /lib/systemd/system/patroni.service

Код:
    
    
    [Unit]
    Description=High availability PostgreSQL Cluster
    After=syslog.target network.target
    
    [Service]
    Type=simple
    User=postgres
    Group=postgres
    ExecStart=/usr/local/bin/patroni /etc/patroni.yml
    KillMode=process
    TimeoutSec=30
    Restart=no
    
    [Install]
    WantedBy=multi-user.target
    Alias=patroni.service

Код:
    
    
    systemctl enable patroni.service

Код:
    
    
    systemctl daemon-reload

Код:
    
    
    systemctl start patroni

Код:
    
    
    systemctl status patroni

[Ctrl]+[C]  
  
**12\. Проверка**  
  
Выполним на все ноды  
  


Код:
    
    
    patronictl -c /etc/patroni.yml list

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-10-20 в 9.17.36.png Просмотров:	0 Размер:	26.2 Кб ID:	4132](..\images\\img_4132_1729405150.png)  
  
**13\. Настройка балансировщика**  
  
**Подготовим 1 виртуальную машину**  
  
Клонируем шаблон k8s-UbuntuTemplate  
  
vCPU = 4  
vRAM = 4 Gb  
vHDD1 = 40 Gb  
  
Меняем IP и имена хостов на каждом узле  
  


Код:
    
    
    rm /etc/resolv.conf && nano /etc/resolv.conf

Код:
    
    
    nameserver 20.20.20.2

Код:
    
    
    nano /etc/netplan/01-netcfg.yaml

Код:
    
    
    20.20.20.23

Код:
    
    
    nano /etc/hostname

Код:
    
    
    pg-lb

Код:
    
    
    reboot

**14\. Установим доп. пакеты**  
  


Код:
    
    
    apt-get update && apt-get install -y haproxy

Код:
    
    
    mkdir -p /media/data/log/haproxy

Замени своим конфигом  
  


Код:
    
    
    rm /etc/haproxy/haproxy.cfg && nano /etc/haproxy/haproxy.cfg

Код:
    
    
    global
         maxconn 12000
         log /dev/log local0 debug
         chroot /var/lib/haproxy
    
    defaults
         log global
         mode tcp
         retries 2
         timeout client 30m
         timeout connect 4s
         timeout server 30m
         timeout check 5s
         maxconn 12000
    
    listen stats
         mode http
         bind *:7000
         stats enable
         stats uri /
    
    frontend database
         mode tcp
         option tcplog
         log-format "%ci:%cp [%t] %ft %fp %b/%s %Tw/%Tc/%Tt %B %ts %ac/%fc/%bc/%sc/%rc %sq/%bq"
         default_backend postgres
         bind *:5432
    
    backend postgres
         option httpchk
         http-check expect status 200
         default-server inter 3s fall 4 rise 2 on-marked-down shutdown-sessions
         server pg01 20.20.20.24:5432 maxconn 6000 check port 8008
         server pg02 20.20.20.25:5432 maxconn 6000 check port 8008
         server pg03 20.20.20.26:5432 maxconn 6000 check port 8008

Код:
    
    
    systemctl restart haproxy

Проверим  
  
Открываем в браузере:  
  
**!!! IP адреса у вас свои !!!**  
  


Код:
    
    
    http://20.20.20.23:7000

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-23 в 20.38.36.png Просмотров:	0 Размер:	47.9 Кб ID:	2153](..\images\\img_2153_1690134010.png)  
  
  
**15\. Настроим админ консоль**  
  
DBeaver  
  


Код:
    
    
    https://dbeaver.io/

Код:
    
    
    20.20.20.23

Код:
    
    
    superuser:
    username: postgres
    password: secretpassword

  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-12 в 15.40.27.png Просмотров:	2 Размер:	83.3 Кб ID:	4164](..\images\\img_4164_1731415305.png)  
  
![Нажмите на изображение для увеличения.  Название:	экрана 2022-05-21 в 8.52.38.png Просмотров:	13 Размер:	63.5 Кб ID:	1010](..\images\\img_1010_1653112421.png)  
  
**Поздравляю, кластер собран!**  
  
  
**!!! Восстановление работы кластера !!!  
  
!!! Внимание, удалены будут все данные !!!**  
  


Код:
    
    
    cat /var/log/syslog | grep patroni

Код:
    
    
    systemctl stop patroni && systemctl stop etcd

Код:
    
    
    rm -R /var/run/postgresql && rm -R /media/data

Код:
    
    
    mkdir -p /media/data/etcd
    mkdir -p /media/data/patroni
    mkdir -p /media/data/log/patroni
    mkdir -p /media/data/log/postgresql
    mkdir -p /var/run/postgresql

Код:
    
    
    chown -R postgres:postgres /var/run/postgresql
    chown -R postgres:postgres /media/data
    chmod 777 /media/data
    chmod 700 /media/data/patroni

Код:
    
    
    systemctl start etcd

Код:
    
    
    etcdctl cluster-health

Код:
    
    
    systemctl start patroni

Код:
    
    
    patronictl -c /etc/patroni.yml list

Вложения 

  * [ ![Нажмите на изображение для увеличения.



Название:	image_998.png

Просмотров:	263

Размер:	15.7 Кб

ID:	1369](..\images\\img_1369_0.png) ](filedata/fetch?id=1369)
  * [ ![Нажмите на изображение для увеличения.



Название:	Снимок экрана 2023-11-04 в 8.43.28.png

Просмотров:	177

Размер:	9.8 Кб

ID:	2835](..\images\\img_2835_0.png) ](filedata/fetch?id=2835)
  * [ ![Нажмите на изображение для увеличения.



Название:	Снимок экрана 2023-07-23 в 21.39.01.png

Просмотров:	217

Размер:	17.2 Кб

ID:	2155](..\images\\img_2155_0.png) ](filedata/fetch?id=2155)
  * [ ![Нажмите на изображение для увеличения.



Название:	image_1000.png

Просмотров:	275

Размер:	41.5 Кб

ID:	1371](..\images\\img_1371_0.png) ](filedata/fetch?id=1371)
  * [ ![Нажмите на изображение для увеличения.



Название:	image_999.png

Просмотров:	270

Размер:	30.9 Кб

ID:	1370](..\images\\img_1370_0.png) ](filedata/fetch?id=1370)




---

