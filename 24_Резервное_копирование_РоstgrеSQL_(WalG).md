---
layout: default
title: 24_Резервное копирование РоstgrеSQL (WalG)
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Резервное копирование РоstgrеSQL (WalG) 

11-17-2023, 01:01 PM

  
**1\. Создадим Buckets в CEPH S3 API**  
  


Код:
    
    
    https://ceph01:8443

Код:
    
    
    pg-backups

![Нажмите на изображение для увеличения.  Название:	image_2216.png Просмотров:	47 Размер:	45.0 Кб ID:	2880](images\\img_2880_1699164313.jpg)  
  
**2\. Включим архивацию PotgreeSQL на все ноды**  
  
  


Код:
    
    
    echo "wal_level=replica" >> /etc/postgresql/13/main/postgresql.conf
    echo "archive_mode=on" >> /etc/postgresql/13/main/postgresql.conf
    echo "archive_command='/usr/local/bin/wal-g wal-push \"%p\" >> /var/log/postgresql/archive_command.log 2>&1' " >> /etc/postgresql/13/main/postgresql.conf
    echo “archive_timeout=60” >> /etc/postgresql/13/main/postgresql.conf
    echo "restore_command='/usr/local/bin/wal-g wal-fetch \"%f\" \"%p\" >> /var/log/postgresql/restore_command.log 2>&1' " >> /etc/postgresql/13/main/postgresql.conf

Код:
    
    
    systemctl restart patroni

Код:
    
    
    systemctl status patroni

[Ctrl]+[C]  
  
Проверим  
  


Код:
    
    
    patronictl -c /etc/patroni.yml list

**3\. Загружаем утилиту на все ноды**  
  


Код:
    
    
    cd /root

Код:
    
    
    wget https://github.com/wal-g/wal-g/releases/download/v0.2.15/wal-g.linux-amd64.tar.gz

Код:
    
    
    tar -xvf wal-g.linux-amd64.tar.gz -C /usr/local/bin

Проверка  
  


Код:
    
    
    wal-g --version

![Нажмите на изображение для увеличения.  Название:	image_2218.png Просмотров:	49 Размер:	12.0 Кб ID:	2881](images\\img_2881_1699173598.jpg)  
  
**4\. Настроим конфиг** **на все ноды**  
  


Код:
    
    
    nano /var/lib/postgresql/.walg.json

Код:
    
    
    {
        "AWS_ENDPOINT": "http://s3.kubeadm.ru:8000",
        "AWS_ACCESS_KEY_ID": "XXXXXXXXXXXXXXXXXXXX",
        "AWS_SECRET_ACCESS_KEY": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "AWS_S3_FORCE_PATH_STYLE": "true",
        "AWS_REGION": "eu-central-1",
    
        "WALG_S3_PREFIX": "s3://pg-backups/",
        "WALG_COMPRESSION_METHOD": "brotli",
        "WALG_DELTA_MAX_STEPS": "5",
    
        "PGDATA": "/media/data/patroni",
        "PGHOST": "/var/run/postgresql/.s.PGSQL.5432"
    }

Получим наши ключи  
  
  
B консоли ceph01  
  
AWS_ACCESS_KEY_ID  
  


Код:
    
    
    cat /root/access_key

AWS_SECRET_ACCESS_KEY  
  


Код:
    
    
    cat /root/secret_key

Код:
    
    
    chown postgres: /var/lib/postgresql/.walg.json

**5\. Выполним архивацию с любой ноды**  
  


Код:
    
    
    su - postgres -c 'wal-g --config /var/lib/postgresql/.walg.json backup-push /media/data/patroni'

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-13 в 18.01.08.png Просмотров:	0 Размер:	89.5 Кб ID:	4171](images\\img_4171_1731510148.jpg)  
  
**6\. Проверим**  
  


Код:
    
    
    https://ceph01:8443

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-13 в 18.03.45.png Просмотров:	0 Размер:	21.0 Кб ID:	4172](images\\img_4172_1731510302.jpg)  
  
**7\. Настроим архивацию по расписанию на всех нодах**  
  


Код:
    
    
    nano backup.sh

Код:
    
    
    #!/bin/bash
    
    #Backup DB PostgreSQL
    su - postgres -c 'wal-g --config /var/lib/postgresql/.walg.json backup-push /media/data/patroni'

Код:
    
    
    chmod u+x backup.sh

Код:
    
    
    nano /etc/crontab

Код:
    
    
    00 23 * * * root sh /root/backup.sh

![Нажмите на изображение для увеличения.  Название:	image_2222.png Просмотров:	48 Размер:	47.8 Кб ID:	2884](images\\img_2884_1699457601.jpg)  
  


Код:
    
    
    systemctl restart cron

Код:
    
    
    systemctl status cron

[Ctrl] + [C]  
  
  
**Поздравляю, настройка завершена!**


---

