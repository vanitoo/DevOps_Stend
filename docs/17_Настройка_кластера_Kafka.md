---
layout: default
title: 17_Настройка кластера Kafka
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Настройка кластера Kafka 


**1\. Подготовим 3 виртуальных машины**  
  
Клонируем шаблон k8s-UbuntuTemplate  
  
3 - kafka ноды  
  
vCPU = 4  
vRAM = 4 Gb  
vHDD = 40 Gb  
  
Меняем IP и имена хостов на каждом узле  
  


Код:
    
    
    rm /etc/resolv.conf && nano /etc/resolv.conf

Код:
    
    
    nameserver 20.20.20.2

Код:
    
    
    nano /etc/netplan/01-netcfg.yaml

Код:
    
    
    20.20.20.35

Код:
    
    
    nano /etc/hostname

Код:
    
    
    kafka01

Код:
    
    
    reboot

**!!! kafka02 и kafka03 настраиваем аналогично !!!**  
  
**2\. Добавим имена хостов на все ноды**  
  


Код:
    
    
    rm /etc/hosts && nano /etc/hosts

Код:
    
    
    127.0.0.1       localhost
    ::1     localhost
    #
    20.20.20.35 kafka01
    20.20.20.36 kafka02
    20.20.20.37 kafka03
    #

**3\. Установим дополнительные пакеты на все ноды**  
  


Код:
    
    
    apt-get update && apt-get install -y curl mc openjdk-8-jre

Проверим  
  


Код:
    
    
    java -version

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-04 в 9.08.46.png Просмотров:	0 Размер:	21.3 Кб ID:	4139](..\images\\img_4139_1730700581.png)  
  
**4\. Скачаем и распаковываем архив на все ноды**  
  


Код:
    
    
    cd

Проверим актуальную версию  
  


Код:
    
    
    http://mirror.linux-ia64.org/apache/kafka/

Код:
    
    
    wget http://mirror.linux-ia64.org/apache/kafka/3.7.1/kafka_2.12-3.7.1.tgz

Код:
    
    
    mkdir -p /media/data/kafka

Код:
    
    
    tar -xvzf kafka_2.12-3.7.1.tgz -C /media/data/kafka --strip-components=1

**5\. Настроим параметры на всех нодах**  
  
Привести в соответствие с скриншотом  
  


Код:
    
    
    nano /media/data/kafka/config/server.properties

Настройка для kafka01  
  
![Нажмите на изображение для увеличения.  Название:	60.png Просмотров:	0 Размер:	178.4 Кб ID:	2487](..\images\\img_2487_1692688895.png)  
  
По аналогии настраиваем kafka02 kafka03  
  
**6\. Настроим параметры Zookeeper на все ноды**  
  


Код:
    
    
    mkdir -p /media/data/zookeeper

Код:
    
    
    nano /media/data/kafka/config/zookeeper.properties

Код:
    
    
    /media/data/zookeeper

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-04 в 9.20.23.png Просмотров:	0 Размер:	9.5 Кб ID:	4140](..\images\\img_4140_1730701281.png)  
  
Добавляем в конец файла  
  


Код:
    
    
    tickTime=2000
    initLimit=5
    syncLimit=2
    server.1=kafka01:2888:3888
    server.2=kafka02:2888:3888
    server.3=kafka03:2888:3888

![Нажмите на изображение для увеличения.  Название:	61.png Просмотров:	0 Размер:	164.8 Кб ID:	2488](..\images\\img_2488_1692689037.png)  
  
В консоли **kafka01**  
  


Код:
    
    
    echo "1" >> /media/data/zookeeper/myid

В консоли **kafka02**  
  


Код:
    
    
    echo "2" >> /media/data/zookeeper/myid

В консоли **kafka03**  
  


Код:
    
    
    echo "3" >> /media/data/zookeeper/myid

**7\. Создадим сервис Zookeeper на все ноды**  
  


Код:
    
    
    chmod +x /media/data/kafka/bin/zookeeper-server-start.sh

Код:
    
    
    nano /etc/systemd/system/zookeeper.service

Код:
    
    
    [Unit]
    Requires=network.target remote-fs.target
    After=network.target remote-fs.target
    
    [Service]
    Type=simple
    ExecStart=/media/data/kafka/bin/zookeeper-server-start.sh /media/data/kafka/config/zookeeper.properties
    ExecStop=/media/data/kafka/bin/zookeeper-server-stop.sh
    Restart=on-abnormal
    
    [Install]
    WantedBy=multi-user.target

Код:
    
    
    systemctl enable zookeeper.service

Код:
    
    
    systemctl daemon-reload

Код:
    
    
    systemctl start zookeeper

Код:
    
    
    systemctl status zookeeper

[Ctrl]+[C]  
  
**8\. Создадим сервис Kafka****на все ноды**  
  


Код:
    
    
    chmod +x /media/data/kafka/bin/kafka-server-start.sh

Код:
    
    
    nano /etc/systemd/system/kafka.service

Код:
    
    
    [Unit]
    Requires=network.target remote-fs.target
    After=network.target remote-fs.target
    
    [Service]
    Type=simple
    ExecStart=/media/data/kafka/bin/kafka-server-start.sh /media/data/kafka/config/server.properties
    ExecStop=/media/data/kafka/bin/kafka-server-stop.sh
    Restart=on-abnormal
    
    [Install]
    WantedBy=multi-user.target

Код:
    
    
    systemctl enable kafka.service

Код:
    
    
    systemctl daemon-reload

Код:
    
    
    systemctl start kafka

Код:
    
    
    systemctl status kafka

[Ctrl]+[C]  
  
**9\. Перегружаем все узлы**  
  


Код:
    
    
    reboot

**!!! После перезагрузки узлов, возможно понадобится перезапуск Kafka !!!**  
  
**!!! Перегружаем сервисы на всех узлах !!!**  
  


Код:
    
    
    systemctl restart zookeeper

Код:
    
    
    systemctl status zookeeper

[Ctrl] + [C]  
  


Код:
    
    
    systemctl restart kafka

Код:
    
    
    systemctl status kafka

[Ctrl] + [C]  
  
**10\. Создадим топики**  
  
Заходим в консоль **kafka01**  
  
Для примера имя топика  
  


Код:
    
    
    my-test-topic

Код:
    
    
    /media/data/kafka/bin/kafka-topics.sh --create \
    --bootstrap-server kafka01:9092,kafka02:9092,kafka03:9092 \
    --replication-factor 3 \
    --partitions 3 \
    --topic my-test-topic

![Нажмите на изображение для увеличения.  Название:	62.png Просмотров:	0 Размер:	37.0 Кб ID:	2489](..\images\\img_2489_1692689401.png)  
  
Получим список топиков  
  


Код:
    
    
    /media/data/kafka/bin/kafka-topics.sh --list \
    --bootstrap-server localhost:9092

![Нажмите на изображение для увеличения.  Название:	63.png Просмотров:	0 Размер:	21.3 Кб ID:	2490](..\images\\img_2490_1692689524.png)  
  
Дополнительная информация  
  


Код:
    
    
    /media/data/kafka/bin/kafka-topics.sh --describe \
    --topic my-test-topic \
    --bootstrap-server localhost:9092

![Нажмите на изображение для увеличения.  Название:	64.png Просмотров:	0 Размер:	67.5 Кб ID:	2491](..\images\\img_2491_1692689622.png)  
  
**11\. Добавим имена хостов на свой ПК**  
  
**для MacOS**  
  
В терминале вводим  
  


Код:
    
    
    sudo nano /private/etc/hosts

**для Windows**  
  


Код:
    
    
    C:\Windows\System32\drivers\etc\hosts

Код:
    
    
    #KAFKA
    20.20.20.35 kafka01
    20.20.20.36 kafka02
    20.20.20.37 kafka03

**12\. Проверим работу кластера**  
  
На **kafka01** мы будем создавать сообщения  
  


Код:
    
    
    /media/data/kafka/bin/kafka-console-producer.sh --topic my-test-topic \
    --bootstrap-server localhost:9092

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-04 в 10.27.04.png Просмотров:	0 Размер:	8.6 Кб ID:	4141](..\images\\img_4141_1730705280.png)  
  


Код:
    
    
    Приветик!

Код:
    
    
    тест пройден?

Код:
    
    
    Ура =)

Код:
    
    
    Привет мир!!!

  
![Нажмите на изображение для увеличения.  Название:	65.png Просмотров:	0 Размер:	28.3 Кб ID:	2492](..\images\\img_2492_1692690654.png)  
  
[Ctrl]+[C]  
  
На **kafka02** и **kafka03** мы будем читаем наши сообщения  
  


Код:
    
    
    /media/data/kafka/bin/kafka-console-consumer.sh --topic my-test-topic \
    --from-beginning \
    --bootstrap-server localhost:9092

**!!! Ждем появление сообщений !!!**  
  
![Нажмите на изображение для увеличения.  Название:	66.png Просмотров:	0 Размер:	30.2 Кб ID:	2493](..\images\\img_2493_1692690727.png)  
  
Выход из консоли: [Ctrl] + [C]  
  
**13\. Устанавливаем на свой ПК утилиту**[**Offset Explorer**](https://kafkatool.com/download.html)  
  


Код:
    
    
    my-test

Код:
    
    
    kafka01,kafka02,kafka03

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-12 в 16.48.36.png Просмотров:	5 Размер:	45.8 Кб ID:	4166](..\images\\img_4166_1731419404.png)  
  
Настроим  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-12 в 16.50.48.png Просмотров:	5 Размер:	55.8 Кб ID:	4167](..\images\\img_4167_1731419502.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-12 в 16.52.01.png Просмотров:	5 Размер:	50.8 Кб ID:	4168](..\images\\img_4168_1731419590.png)  
  
  
  
**Поздравляю, настройка завершена!**


---

