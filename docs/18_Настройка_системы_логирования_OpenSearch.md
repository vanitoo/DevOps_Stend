---
layout: default
title: 18_Настройка системы логирования OpenSearch
---
<a class="back-link" href="../index.html">⬅ Назад к списку</a>


##  Настройка системы логирования OpenSearch 


vCPU = 8  
vRAM = 16 Gb  
vHDD1 = 40 Gb  
vHDD2 = 100 Gb  
  
**1\. Подготовим 1 виртуальную машину**  
  
Клонируем шаблон k8s-UbuntuTemplate  
  
**!!! Добавляем количество ядер, оперативной памяти и дисков !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-06-14 в 07.09.38.png Просмотров:	2 Размер:	66.8 Кб ID:	4827](..\images\\img_4827_1749874318.png)  
  
Меняем IP и имена хостов на каждом узле  
  


Код:
    
    
    rm /etc/resolv.conf && nano /etc/resolv.conf

Код:
    
    
    nameserver 20.20.20.2

Код:
    
    
    nano /etc/netplan/01-netcfg.yaml

Код:
    
    
    20.20.20.60

Код:
    
    
    nano /etc/hostname

Код:
    
    
    opensearch

Код:
    
    
    reboot

**2\. Подключим новый диск**  
  
Убедимся в его наличии  
  


Код:
    
    
    lsblk

Код:
    
    
    fdisk /dev/sdb

![Нажмите на изображение для увеличения.  Название:	image_3356.png Просмотров:	0 Размер:	91.9 Кб ID:	4826](..\images\\img_4826_1749873972.png)  
  


Код:
    
    
    mkfs.ext4 /dev/sdb1

Код:
    
    
    mount /dev/sdb1 /media/data

Код:
    
    
    blkid

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-06-14 в 07.01.38.png Просмотров:	0 Размер:	29.3 Кб ID:	4824](..\images\\img_4824_1749873750.png)  
  


Код:
    
    
    nano /etc/fstab

Код:
    
    
    UUID=xxxxxxxx /media/data ext4 rw 0 1

Код:
    
    
    reboot

Проверим  
  


Код:
    
    
    lsblk

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-06-14 в 06.58.36.png Просмотров:	0 Размер:	18.2 Кб ID:	4825](..\images\\img_4825_1749873663.png)  
  
**3\. Установка Docker & Docker-Compose**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/398)  
  
**4\. Добавим параметр виртуальной памяти**  
  
В конец файла  
  


Код:
    
    
    nano /etc/sysctl.conf

Код:
    
    
    vm.max_map_count=262144

Код:
    
    
    sysctl -p

**5\. Скачиваем и распаковываем[архив](https://galkin-vladimir.ru:5446/d/s/13lHaajTCNwpSKmwWMQF8mtTmilYQSzS/wstR2QkLeN3cwwv80Z0HjoBdLAi0RpZd-9rOgrKi_Wgw)**  
  
Копируем и вставляем содержимое в файл **docker-compose.yml**  
  


Код:
    
    
    nano docker-compose.yml

Код:
    
    
    docker-compose up -d

**!!! Ждем завершение процесса !!!**  
  
**6\. Проверка**  
  
Откроем браузер  
  


Код:
    
    
    http://20.20.20.60:5601

Код:
    
    
    login: admin
    pass: admin

**7\. Настроим отправку событий в Opensearch**  
  


Код:
    
    
    rm /media/data/docker/volumes/root_logstash-data/_data/pipeline/logstash.conf

Код:
    
    
    nano /media/data/docker/volumes/root_logstash-data/_data/pipeline/logstash.conf

Код:
    
    
    input {
       tcp {
          port => 5044
       }
    }
    
    output {
       opensearch {
       hosts => ["https://20.20.20.60:9200"]
       index => "opensearch-logstash-%{+YYYY.MM.dd}"
       user => admin
       password => admin
       ssl => true
       ssl_certificate_verification => false
       }
    }

Код:
    
    
    docker-compose restart

**8\. Установим Filebeat для сбора событий**  
  
**Пример:**  
  
Выбираем 3 узла K8s  
  


Код:
    
    
    #
    20.20.20.14 worker01
    20.20.20.15 worker02
    20.20.20.16 worker03
    #

Код:
    
    
    wget https://mirror.yandex.ru/mirrors/elastic/7/pool/main/f/filebeat/filebeat-7.12.1-amd64.deb

Код:
    
    
    dpkg -i filebeat-7.12.1-amd64.deb

Код:
    
    
    nano /etc/filebeat/filebeat.yml

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-06 в 11.34.23.png Просмотров:	0 Размер:	59.2 Кб ID:	4144](..\images\\img_4144_1730882190.png)  
  
Список всех доступных модулей  
  


Код:
    
    
    filebeat modules list

Выбираем нужные  
  


Код:
    
    
    filebeat modules enable system

Код:
    
    
    systemctl enable filebeat

Код:
    
    
    systemctl start filebeat

Код:
    
    
    systemctl status filebeat

[Ctrl]+[C]  
  
  
**9\. Создадим индекс**  
  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-25 в 7.11.51.png Просмотров:	0 Размер:	26.6 Кб ID:	2189](..\images\\img_2189_1690258383.png)  
  
**!!! Ждём 5-10 минут появления данных !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-25 в 7.13.16.png Просмотров:	0 Размер:	27.5 Кб ID:	2190](..\images\\img_2190_1690258435.png)  
  


Код:
    
    
    opensearch-logstash-*

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-29 в 5.21.11.png Просмотров:	0 Размер:	70.4 Кб ID:	2304](..\images\\img_2304_1690597395.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-25 в 7.16.00.png Просмотров:	0 Размер:	66.0 Кб ID:	2192](..\images\\img_2192_1690258609.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-25 в 7.11.51.png Просмотров:	0 Размер:	26.6 Кб ID:	2193](..\images\\img_2193_1690258383.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-06 в 11.47.46.png Просмотров:	4 Размер:	161.3 Кб ID:	4145](..\images\\img_4145_1730882974.png)  
  
  
**10\. Ограничим размер индекса**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-29 в 4.59.49.png Просмотров:	0 Размер:	66.5 Кб ID:	2297](..\images\\img_2297_1690596049.png)  
  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-06-07 в 07.36.46.png Просмотров:	0 Размер:	31.2 Кб ID:	4822](..\images\\img_4822_1749271069.png)  
  
Вставляем содержимое файла policies.json из архива  
  
  
**Поздравляю, настройка завершена!**

Вложения 

  * [ ![Нажмите на изображение для увеличения.



Название:	image_1724.png

Просмотров:	227

Размер:	15.5 Кб

ID:	2162](..\images\\img_2162_0.png) ](filedata/fetch?id=2162)




---

