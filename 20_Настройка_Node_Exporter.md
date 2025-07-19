---
layout: default
title: 20_Настройка Node Exporter
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Настройка Node Exporter 

04-29-2021, 11:08 PM

Источник: [Node Exporter](https://prometheus.io/docs/guides/node-exporter/)  
  
Настроим сбор метрик с узлов  
  
**Пример:**  
  
Выбираем узел  
  


Код:
    
    
    20.20.20.41 runner01

**1\. Установка**  
  
Для установки Node Exporter выбираем узлы откуда нужно собрать метрики.  
  


Код:
    
    
    cd /root

Код:
    
    
    wget github.com/prometheus/node_exporter/releases/download/v1.1.2/node_exporter-1.1.2.linux-amd64.tar.gz

Код:
    
    
    tar -xvf node_exporter-1.1.2.linux-amd64.tar.gz -C /usr/local/bin/ --strip-components=1

Код:
    
    
    useradd -rs /bin/false node_exporter

Код:
    
    
    chown -R node_exporter:node_exporter /usr/local/bin/node_exporter

**2\. Настройка сервиса**  
  


Код:
    
    
    nano /etc/systemd/system/node_exporter.service

Код:
    
    
    [Unit]
    Description=Node Exporter
    After=network.target
    
    [Service]
    User=node_exporter
    Group=node_exporter
    Type=simple
    ExecStart=/usr/local/bin/node_exporter --web.listen-address=":9191"
    
    [Install]
    WantedBy=multi-user.target

Код:
    
    
    systemctl daemon-reload

Код:
    
    
    systemctl enable node_exporter

Код:
    
    
    systemctl start node_exporter

Код:
    
    
    systemctl status node_exporter

Проверим наличие метрик  
  


Код:
    
    
    http://20.20.20.41:9191/metrics

Пример:  
  
![Нажмите на изображение для увеличения.  Название:	экрана 2022-03-08 в 11.43.40.png Просмотров:	0 Размер:	92.5 Кб ID:	860](images\\img_860_1646729071.png)  
  
**3\. Добавляем свои таргеты в Prometeus:**  
  
В водим в консоли prometeus  
  


Код:
    
    
    docker-compose stop

Дописываем в конец файла свои таргеты  
  
**!!! Соблюдаем отступы !!!**  
  


Код:
    
    
    nano /media/data/docker/volumes/root_prometheus-data/_data/prometheus.yml

Код:
    
    
    - job_name: "runner01"
      static_configs:
      - targets: ["20.20.20.41:9191"]

![Нажмите на изображение для увеличения.



Название:	Снимок экрана 2024-11-12 в 8.50.44.png

Просмотров:	18

Размер:	29.9 Кб

ID:	4151](images\\img_4151_1731390704.png)  
  
  


Код:
    
    
    docker-compose up -d

Проверим  
  
![Нажмите на изображение для увеличения.



Название:	Снимок экрана 2024-11-12 в 8.52.21.png

Просмотров:	17

Размер:	43.3 Кб

ID:	4152](images\\img_4152_1731390834.png)  
  
Проверим в Grafana  
  
![Нажмите на изображение для увеличения.



Название:	Снимок экрана 2024-11-12 в 8.54.48.png

Просмотров:	17

Размер:	97.5 Кб

ID:	4153](images\\img_4153_1731390938.png)  
  
  
**Поздравляю! настройка завершена.**

Вложения 

  * [ ![Нажмите на изображение для увеличения.



Название:	1.png

Просмотров:	221

Размер:	78.6 Кб

ID:	829](images\\img_829_0.png) ](filedata/fetch?id=829)




---

