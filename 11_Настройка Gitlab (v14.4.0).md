
##  Настройка Gitlab (v14.4.0) 

02-21-2022, 10:04 AM

vCPU = 4  
vRAM = 8 Gb  
vHDD = 40 Gb  
  
**1\. Подготовим 1 виртуальную машину**  
  
Клонируем шаблон k8s-UbuntuTemplate  
  
**!!! Добавляем оперативной памяти !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-10-07 в 11.56.00.png Просмотров:	0 Размер:	57.9 Кб ID:	4101](images\\img_4101_1728291415.jpg)  
  
Меняем IP и имена хостов на каждом узле  
  


Код:
    
    
    rm /etc/resolv.conf && nano /etc/resolv.conf

Код:
    
    
    nameserver 20.20.20.2

Код:
    
    
    nano /etc/netplan/01-netcfg.yaml

Код:
    
    
    20.20.20.40

Код:
    
    
    nano /etc/hostname

Код:
    
    
    gitlab

Код:
    
    
    reboot

**2\. Установка Docker & Docker-Compose**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/398)  
  
**3\. Создадим структуру каталогов и пустые файлы**  
  


Код:
    
    
    mkdir -p /media/data/nginx/conf
    mkdir /media/data/nginx/logs

Код:
    
    
    touch /media/data/nginx/conf/gitlab.crt
    touch /media/data/nginx/conf/gitlab.key
    touch /media/data/nginx/conf/nginx.conf
    touch /media/data/nginx/conf/gitlab-http.conf

Код:
    
    
    cd /root

Скачиваем и распаковываем [_**архив**_](https://galkin-vladimir.ru:5446/d/s/10jMIFpxiq3pplHGj2kQzLUm3Yu3FnEO/o82FLXcDN8WTxGRWmkQs4VTb4_0VAS1Z-6LVAWfduyQs)  
  
Копируем содержимое в файл **docker-compose.yml**  
  


Код:
    
    
    nano /root/docker-compose.yml

Код:
    
    
    docker-compose up -d

**!!! Ждем завершение процесса !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-25 в 9.11.33.png Просмотров:	0 Размер:	11.2 Кб ID:	2201](images\\img_2201_1690265586.jpg)  
  


Код:
    
    
    cd /root

Код:
    
    
    docker-compose stop

Ждем остановки всех контейнеров  
  
  
Копируем и вставляем содержимое в файл **nginx.conf**  
  


Код:
    
    
    nano /media/data/nginx/conf/nginx.conf

Код:
    
    
    # This file is managed by gitlab-ctl. Manual changes will be
    # erased! To change the contents below, edit /etc/gitlab/gitlab.rb
    # and run `sudo gitlab-ctl reconfigure`.
    
    user nginx;
    worker_processes 1;
    error_log stderr;
    pid nginx.pid;
    
    
    events {
    worker_connections 10240;
    }
    
    http {
    log_format gitlab_access '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"';
    log_format gitlab_ci_access '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"';
    log_format gitlab_mattermost_access '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"';
    
    server_names_hash_bucket_size 64;
    
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    
    keepalive_timeout 65;
    
    gzip on;
    gzip_http_version 1.0;
    gzip_comp_level 2;
    gzip_proxied any;
    gzip_types text/plain text/css application/x-javascript text/xml application/xml application/xml+rss text/javascript application/json;
    
    include mime.types;
    
    proxy_cache_path proxy_cache keys_zone=gitlab:10m max_size=1g levels=1:2;
    proxy_cache gitlab;
    
    include /etc/nginx/conf.d/gitlab-http.conf;
    }

Копируем и вставляем содержимое в файл **gitlab-http.conf**  
  
**!!! Имя домена вводим свое !!!**  
  


Код:
    
    
    nano /media/data/nginx/conf/gitlab-http.conf

Код:
    
    
    upstream gitlab-workhorse {
    server gitlab_app:8081;
    }
    
    
    server {
    listen 443 ssl;
    keepalive_timeout 70;
    ssl_certificate /etc/nginx/gitlab.crt;
    ssl_certificate_key /etc/nginx/gitlab.key;
    
    #listen *:80;
    server_name gitlab.kubeadm.ru;
    server_tokens off; ## Don't show the nginx version number, a security best practice
    
    ## Increase this if you want to upload large attachments
    ## Or if you want to accept large git objects over http
    client_max_body_size 0;
    
    
    ## Real IP Module Config
    ## http://nginx.org/en/docs/http/ngx_http_realip_module.html
    
    ## Individual nginx logs for this GitLab vhost
    access_log /var/log/nginx/gitlab_access.log gitlab_access;
    error_log /var/log/nginx/gitlab_error.log;
    
    location / {
    ## If you use HTTPS make sure you disable gzip compression
    ## to be safe against BREACH attack.
    
    
    ## https://github.com/gitlabhq/gitlabhq/issues/694
    ## Some requests take more than 30 seconds.
    proxy_read_timeout 3600;
    proxy_connect_timeout 300;
    proxy_redirect off;
    
    proxy_http_version 1.1;
    
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    
    #proxy_set_header X-Forwarded-Proto http;
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header X-Forwarded-Ssl off;
    
    proxy_pass http://gitlab-workhorse;
    }
    }

Код:
    
    
    chown www-data:www-data -R /media/data/nginx
    chmod 755 -R /media/data/nginx

**4\. Покупаем Wildcard сертификат**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/3514)  
  
**5\. Настройка SSL сертификатов**  
  
**!!! Имя домена вводим свое !!!**  
  
Копируем содержимое из SSH консоли  
  


Код:
    
    
    nano /media/data/nginx/conf/gitlab.crt

Код:
    
    
    nano /media/data/nginx/conf/gitlab.key

Код:
    
    
    chown www-data:www-data -R /media/data/nginx/conf
    chmod 777 -R /media/data/nginx/conf

**6\. Настройка Gitlab**  
  
Копируем и вставляем в начало файла:  
  
**!!! Имя домена вводим свое !!!**  
  


Код:
    
    
    nano /media/data/gitlab/config/gitlab.rb

Код:
    
    
    external_url 'https://gitlab.kubeadm.ru'
    
    gitlab_rails['db_adapter'] = "postgresql"
    gitlab_rails['db_database'] = "gitlabhq_production"
    gitlab_rails['db_username'] = "git"
    gitlab_rails['db_password'] = "SRv5@df'2"
    gitlab_rails['db_host'] = "postgresql"
    gitlab_rails['db_port'] = 5432
    
    gitlab_rails['redis_host'] = "redis"
    gitlab_rails['redis_port'] = 6379
    gitlab_rails['redis_database'] = 0
    
    gitlab_workhorse['enable'] = true
    gitlab_workhorse['listen_network'] = "tcp"
    gitlab_workhorse['listen_addr'] = "0.0.0.0:8081"
    gitlab_workhorse['auth_backend'] = "http://localhost:8080"
    
    postgresql['enable'] = false
    redis['enable'] = false
    nginx['enable'] = false
    monitoring_role['enable'] = false
    prometheus['enable'] = false
    alertmanager['enable'] = false
    grafana['enable'] = false

Код:
    
    
    cd /root

Код:
    
    
    docker-compose up -d

**7\. Настроим PostgreSQL**  
  
Создаем пользователя git в локальной БД gitlabhq_production  
  


Код:
    
    
    docker exec -i -t postgresql /bin/bash

Код:
    
    
    su - postgres

Код:
    
    
    createuser -P git

**!!! Пароль в****консоли****не отражаются !!!**  
  


Код:
    
    
    **SRv5@df'2**

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-25 в 9.25.50.png Просмотров:	0 Размер:	10.8 Кб ID:	2203](images\\img_2203_1690266490.jpg)  
  


Код:
    
    
    createdb -O git gitlabhq_production

Код:
    
    
    echo 'CREATE EXTENSION pg_trgm;' | psql gitlabhq_production

Код:
    
    
    exit
    exit

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-25 в 9.28.45.png Просмотров:	0 Размер:	20.8 Кб ID:	2204](images\\img_2204_1690266582.jpg)  
  
Если возникнет ошибка  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-03-29 в 15.59.49.png Просмотров:	0 Размер:	18.3 Кб ID:	1386](images\\img_1386_1680094899.jpg)  
  
**!!! Игнорируем !!!**  
  


Код:
    
    
    cd /root

Код:
    
    
    docker-compose restart

**!!! Ждем пере-запуск всех контейнеров !!!**  
  


Код:
    
    
    docker exec -i -t gitlab_app /bin/bash

Код:
    
    
    gitlab-rails console -e production

**!!! Ждем 1-2 минуты !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-09-22 в 8.16.40.png Просмотров:	0 Размер:	26.7 Кб ID:	3948](images\\img_3948_1726982418.jpg)  
  
  
**!!! ​Если появилась ошибка, повотно вводим команду !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-08-19 в 8.17.24.png Просмотров:	0 Размер:	17.5 Кб ID:	2481](images\\img_2481_1692422334.jpg)  
  


Код:
    
    
    user = User.where(id: 1).first

Код:
    
    
    user.password = "Qwe+12345678"

Код:
    
    
    user.password_confirmation = "Qwe+12345678"

Код:
    
    
    user.save!

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-09-03 в 9.45.31.png Просмотров:	0 Размер:	74.9 Кб ID:	2542](images\\img_2542_1693723674.jpg)  
  


Код:
    
    
    exit
    exit

**8\. Добавим новый узел в файл host на своём ПК**  
  
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
    
    
    20.20.20.40    gitlab.kubeadm.ru

**9\. Открываем Web интерфейс**  
  


Код:
    
    
    https://gitlab.kubeadm.ru

Код:
    
    
    login: root
    pass: Qwe+12345678

После входа в веб интерфейс, сразу меняем пароль на свой.  
  
![Нажмите на изображение для увеличения.  Название:	экрана 2022-02-27 в 7.32.01.png Просмотров:	0 Размер:	14.0 Кб ID:	810](images\\img_810_1645936392.jpg)  
  
![Нажмите на изображение для увеличения.  Название:	экрана 2022-02-27 в 7.33.26.png Просмотров:	0 Размер:	80.6 Кб ID:	811](images\\img_811_1645936473.jpg)  
  
Выберем удобный для себя язык интерфейса  
  
![Нажмите на изображение для увеличения.  Название:	экрана 2022-02-27 в 7.35.06.png Просмотров:	0 Размер:	88.0 Кб ID:	812](images\\img_812_1645936613.jpg)  
  
Настроим **свой** часовой пояс  
  
![Нажмите на изображение для увеличения.  Название:	экрана 2022-02-27 в 7.46.19.png Просмотров:	0 Размер:	80.1 Кб ID:	813](images\\img_813_1645937310.jpg)  
  
  
**10\. Настроим архивацию (по требованию)**  
  


Код:
    
    
    mkdir -p /media/data/postgresql/data/backups

Код:
    
    
    chown systemd-coredump:systemd-coredump -R /media/data/postgresql/data/backups
    chmod 700 -R /media/data/postgresql/data/backups

Код:
    
    
    cd /root

Код:
    
    
    nano backup.sh

**!!! Имя домена вводим свое !!!**  
  


Код:
    
    
    #!/bin/bash
    
    mkdir -p /media/backup/gitlab.kubeadm.ru/$(date +%Y%m%d)
    
    #Backup DB PostgreSQL
    docker exec -ti postgresql /bin/bash -c 'pg_dump -U postgres -Fc gitlabhq_production > /var/lib/postgresql/data/backups/$(date +%Y%m%d)_gitlab_pg.dump'
    mv /media/data/postgresql/data/backups/$(date +%Y%m%d)_gitlab_pg.dump /media/backup/gitlab.kubeadm.ru/$(date +%Y%m%d)
    
    #Backup GitLab
    tar -cv -f /media/backup/gitlab.kubeadm.ru/$(date +%Y%m%d)/$(date +%Y%m%d)_gitlab_config.tar /media/data/gitlab/config
    
    docker exec -ti gitlab_app /bin/bash -c 'gitlab-backup create BACKUP=$(date +%Y%m%d) SKIP=db'
    mv /media/data/gitlab/data/backups/$(date +%Y%m%d)_gitlab_backup.tar /media/backup/gitlab.kubeadm.ru/$(date +%Y%m%d)

Код:
    
    
    chmod u+x backup.sh

Код:
    
    
    sh backup.sh

**11\. Добавим выполнение по расписанию (по требованию)**  
  
Каждый день в 23.00  
  
![Нажмите на изображение для увеличения.  Название:	экрана 2022-06-04 в 7.11.23.png Просмотров:	0 Размер:	78.2 Кб ID:	1032](images\\img_1032_1654316058.jpg)  
  


Код:
    
    
    nano /etc/crontab

Код:
    
    
    00 23   * * *   root    sh /root/backup.sh

Код:
    
    
    systemctl restart cron

Код:
    
    
    systemctl status cron

**!!! Забираем архивы отсюда !!!**  
  


Код:
    
    
    cd /media/backup/gitlab.kubeadm.ru

Код:
    
    
    ls

**12\. Восстановление из архива (по требованию)**  
  
**!!! Это пример !!!**  
  
Раскладываем архивы  
  


Код:
    
    
    mc

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-09-21 в 16.01.21.png Просмотров:	0 Размер:	37.7 Кб ID:	2698](images\\img_2698_1695301340.jpg)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-09-21 в 16.12.42.png Просмотров:	0 Размер:	36.3 Кб ID:	2701](images\\img_2701_1695302098.jpg)  
  
**!!! Переписываем файл !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-09-21 в 16.13.38.png Просмотров:	0 Размер:	63.8 Кб ID:	2702](images\\img_2702_1695302114.jpg)  
  
#Restore DB PostgreSQL  
  


Код:
    
    
    docker stop gitlab_app

Код:
    
    
    docker exec -ti postgresql /bin/bash

Код:
    
    
    cd /var/lib/postgresql/data/backups

Код:
    
    
    ls

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-09-21 в 16.05.16.png Просмотров:	0 Размер:	14.7 Кб ID:	2699](images\\img_2699_1695301596.jpg)  
  
**!!! Копируем и вставляем только имя архива 'pg_dump_gitlabhq_production_xxxxxxxx.dump' !!!**  
  


Код:
    
    
    pg_restore -U postgres -c -v -d gitlabhq_production XXXXXXXX_gitlab_pg.dump

**!!! Ждем завершение процесса !!!**  
  
Ошибки и предупреждения игнорируем.  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-09-21 в 16.08.32.png Просмотров:	0 Размер:	21.4 Кб ID:	2700](images\\img_2700_1695301749.jpg)  
  


Код:
    
    
    psql -U postgres gitlabhq_production

Код:
    
    
    UPDATE projects SET runners_token = null, runners_token_encrypted = null;

Код:
    
    
    UPDATE namespaces SET runners_token = null, runners_token_encrypted = null;

Код:
    
    
    UPDATE application_settings SET runners_registration_token_encrypted = null;

Код:
    
    
    UPDATE ci_runners SET token = null, token_encrypted = null;

Код:
    
    
    UPDATE ci_builds SET token = null, token_encrypted = null;

Код:
    
    
    TRUNCATE web_hooks CASCADE;

Код:
    
    
    exit
    exit

Код:
    
    
    docker start gitlab_app

#Restore GitLab  
  


Код:
    
    
    chown root:root -R /media/data/gitlab/data/backups

Код:
    
    
    chmod 777 -R /media/data/gitlab/data/backups

Код:
    
    
    docker exec -ti gitlab_app /bin/bash

Код:
    
    
    cd /var/opt/gitlab/backups

Код:
    
    
    ls

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-09-21 в 16.18.08.png Просмотров:	4 Размер:	10.5 Кб ID:	2703](images\\img_2703_1695302346.jpg)  
  
**!!! Копируем и вставляем только имя архива !!!**  
  


Код:
    
    
    gitlab-backup restore BACKUP=XXXXXXXX

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-09-21 в 16.20.04.png Просмотров:	4 Размер:	9.8 Кб ID:	2704](images\\img_2704_1695302504.jpg)  
  
![Нажмите на изображение для увеличения.  Название:	экрана 2022-07-16 в 8.08.33.png Просмотров:	0 Размер:	27.7 Кб ID:	1042](images\\img_1042_1657948206.jpg)  
  
**!!! Ждем завершение процесса !!!**  
  


Код:
    
    
    exit

Код:
    
    
    docker restart gitlab_app

Код:
    
    
    docker exec -ti gitlab_app /bin/bash

Код:
    
    
    gitlab-rake gitlab:check SANITIZE=true

**!!! Ничего не вводим !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-08-20 в 7.38.19.png Просмотров:	0 Размер:	6.5 Кб ID:	2486](images\\img_2486_1692506514.jpg)  
  
**!!! Ждем завершение процесса !!!**  
  
![Нажмите на изображение для увеличения.  Название:	image_711.png Просмотров:	4 Размер:	69.9 Кб ID:	1035](images\\img_1035_1654406563.jpg)  
  


Код:
    
    
    gitlab-ctl reconfigure

**!!! Ждем завершение процесса !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-25 в 10.27.07.png Просмотров:	0 Размер:	13.4 Кб ID:	2207](images\\img_2207_1690270090.jpg)  
  


Код:
    
    
    exit

  
**Поздравляю, настройка завершена!**


---

