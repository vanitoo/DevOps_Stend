---
layout: default
title: 07_Настройка DHCP Server
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Настройка DHCP Server 

02-06-2023, 11:41 PM

Настроим получения IP адресов для диапазона  
  


Код:
    
    
    **#DHCP Server**
    20.20.20.90
    -//-
    20.20.20.99

**1\. Заходим в консоль[ ns](https://forum.kubeadm.ru/node/239)**  
  


Код:
    
    
    apt-get update && apt-get install -y isc-dhcp-server

**2\. Смотрим интерфейс локалькой сети**  
  


Код:
    
    
    ip -br a

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-03-03 в 16.04.50.png Просмотров:	0 Размер:	8.8 Кб ID:	4636](images\\img_4636_1741007150.jpg)  
  


Код:
    
    
    nano /etc/default/isc-dhcp-server

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-03-03 в 16.06.38.png Просмотров:	0 Размер:	9.2 Кб ID:	4637](images\\img_4637_1741007271.jpg)  
  
**Вводим свое имя домена!**  
  


Код:
    
    
    nano /etc/dhcp/dhcpd.conf

Код:
    
    
    option domain-name "kubeadm.ru";
    option domain-name-servers ns.kubeadm.ru;

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-03-03 в 16.09.08.png Просмотров:	0 Размер:	10.3 Кб ID:	4638](images\\img_4638_1741007375.jpg)  
  
**3\. Добавляем в конц файла**  
  


Код:
    
    
    subnet 20.20.20.0 netmask 255.255.255.0 {
    range 20.20.20.90 20.20.20.99;
    option domain-name-servers 20.20.20.2;
    option domain-name "kubeadm.ru";
    option ntp-servers 20.20.20.2;
    option subnet-mask 255.255.255.0;
    option routers 20.20.20.1;
    option broadcast-address 20.20.20.255;
    default-lease-time 600;
    max-lease-time 7200;
    }

Код:
    
    
    systemctl restart isc-dhcp-server

Код:
    
    
    systemctl status isc-dhcp-server

**4\. Проверим (по требованию)**  
  
**Это пример!**  
  


Код:
    
    
    cat /var/lib/dhcp/dhcpd.leases

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-03-03 в 16.13.20.png Просмотров:	0 Размер:	47.8 Кб ID:	4640](images\\img_4640_1741007652.jpg)  
  
  
**5\. Закрепим IP адрес за MAC (по требованию)**  
  


Код:
    
    
    nano /etc/dhcp/dhcpd.conf

Добавляем в конц файла  
  


Код:
    
    
    host mynas {
    hardware ethernet 00:0c:29:51:26:76;
    fixed-address 20.20.20.xx;
    }

Код:
    
    
    systemctl restart isc-dhcp-server

Код:
    
    
    systemctl status isc-dhcp-server

**Поздравляю, настройка завершена!**


---

