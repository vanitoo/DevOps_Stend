
##  Настроим свой DNS сервер (Bind) 

04-10-2021, 09:32 AM

  
vCPU = 4  
vRAM = 4 Gb  
vHDD = 40 Gb  
  
**1\. Подготовим 1 виртуальную машину**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-10-06 в 9.03.22.png Просмотров:	0 Размер:	28.1 Кб ID:	4091](images\\img_4091_1728194674.jpg)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-10-06 в 9.05.17.png Просмотров:	0 Размер:	21.4 Кб ID:	4092](images\\img_4092_1728194782.jpg)  
  


Код:
    
    
    ns

**!!! Ждем завершение процесса !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-10-06 в 9.13.29.png Просмотров:	0 Размер:	33.3 Кб ID:	4093](images\\img_4093_1728195271.jpg)  
  
**2\. Настроим имя хоста и IP адрес**  
  
Подключаемся по SSH  
  


Код:
    
    
    20.20.20.250

Заменим IP адрес  
  


Код:
    
    
    nano /etc/netplan/01-netcfg.yaml

Код:
    
    
    20.20.20.2

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-10-06 в 9.26.32.png Просмотров:	0 Размер:	18.8 Кб ID:	4094](images\\img_4094_1728196060.jpg)  
  
Заменим имя хоста  
  


Код:
    
    
    nano /etc/hostname

Код:
    
    
    ns

Код:
    
    
    rm /etc/hosts && nano /etc/hosts

Код:
    
    
    127.0.1.1 ns.kubeadm.ru ns
    127.0.0.1 localhost
    ::1     localhost

Код:
    
    
    reboot

Проверим  
  


Код:
    
    
    hostname -f

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-11 в 11.25.59.png Просмотров:	6 Размер:	4.3 Кб ID:	4351](images\\img_4351_1733905584.jpg)  
  
**3\. Установим дополнительные пакеты:**  
  


Код:
    
    
    apt-get update && apt-get install -y nano mc bind9 bind9utils bind9-doc

**4\. Редактируем named.conf**  
  
Копируем и вставляем содержимое  
  


Код:
    
    
    rm /etc/bind/named.conf && nano /etc/bind/named.conf

Код:
    
    
    include "/etc/bind/named.conf.options";
    include "/etc/bind/named.conf.local";
    include "/etc/bind/named.conf.default-zones";
    include "/etc/bind/rndc.key";

**5\. Редактируем named.conf.options**  
  
Копируем и вставляем содержимое  
  


Код:
    
    
    rm /etc/bind/named.conf.options && nano /etc/bind/named.conf.options

Код:
    
    
    acl our_net {
       20.20.20.0/24;
       127.0.0.0/8;
    };
    
    controls {
       inet 127.0.0.1 allow { localhost; } keys { "rndc-key"; };
    };
    
    logging {
       category lame-servers { null; };
    };
    
    options {
       directory "/var/cache/bind";
    
       forwarders {
       1.1.1.1;
       1.1.2.2;
       };
    
       #listen-on { any; };
       listen-on {
       20.20.20.0/24;
       127.0.0.0/8;
       };
    
       allow-query {
       our_net;
       };
    
       #dnssec-enable yes;
       dnssec-validation auto;
       auth-nxdomain no; # conform to RFC1035
       listen-on-v6 { none; };
       allow-recursion { our_net; };
    };

**6\. Редактируем named.conf.default-zones**  
  
Копируем и вставляем содержимое  
  


Код:
    
    
    nano /etc/bind/named.conf.default-zones

**!!! Добавляем в конец файла !!!**  
  
**!!! Имя домена вводим свое !!!**  
  


Код:
    
    
    zone "kubeadm.ru" {
    type master;
    file "/etc/bind/kubeadm.ru";
    };
    
    zone "20.20.20.in-addr.arpa" {
    type master;
    file "/etc/bind/20.20.20.in-addr.arpa";
    };

  
**7\. Прямая зона:**  
  
**!!! Serial - увеличиваем на 1 единицу, при каждом изменении настроек !!!**  
  
**!!! Имя домена вводим свое !!!**  
  
Копируем и вставляем содержимое  
  


Код:
    
    
    nano /etc/bind/kubeadm.ru

Код:
    
    
    $TTL      604800
    @           IN            SOA       ns.kubeadm.ru.        root.kubeadm.ru. (
                                                 00000001 ; Serial
                                                 604800 ; Refresh
                                                 86400 ; Retry
                                                 2419200 ; Expire
                                                 604800 ; Negative Cache TTL
    )
                   IN        NS      ns.kubeadm.ru.
                   IN        MX 10   mx.kubeadm.ru.
    ;
    @              IN        A       20.20.20.2
    localhost      IN        A       127.0.0.1
    ns             IN        A       20.20.20.2
    mx             IN        A       20.20.20.2
    ldap           IN        A       20.20.20.3
    keycloak       IN        A       20.20.20.4
    ;
    gitlab         IN        A       20.20.20.40
    harbor         IN        A       20.20.20.55
    kafka01        IN        A       20.20.20.35
    kafka02        IN        A       20.20.20.36
    kafka03        IN        A       20.20.20.37
    opensearch     IN        A       20.20.20.60
    rancher        IN        A       20.20.20.10
    k8s            IN        A       20.20.20.11
    ;k8s            IN        A       20.20.20.12
    ;k8s            IN        A       20.20.20.13
    master01       IN        A       20.20.20.11
    ;master02       IN        A       20.20.20.12
    ;master03       IN        A       20.20.20.13
    worker01       IN        A       20.20.20.14
    worker02       IN        A       20.20.20.15
    worker03       IN        A       20.20.20.16
    ceph01         IN        A       20.20.20.20
    ceph02         IN        A       20.20.20.21
    ceph03         IN        A       20.20.20.22
    s3             IN        A       20.20.20.20
    s3             IN        A       20.20.20.21
    s3             IN        A       20.20.20.22
    pg             IN        A       20.20.20.23
    api            IN        A       20.20.20.251

  
**8\. Обратная зона:**  
  
**!!! Serial - увеличиваем на 1 единицу, при каждом изменении настроек !!!**  
  
**!!! Имя домена вводим свое !!!**  
  
Копируем и вставляем содержимое  
  


Код:
    
    
    nano /etc/bind/20.20.20.in-addr.arpa

Код:
    
    
    $TTL        604800
    @             IN           SOA      ns.kubeadm.ru.       root.kubeadm.ru. (
                                                00000001 ; Serial
                                                604800 ; Refresh
                                                86400 ; Retry
                                                2419200 ; Expire
                                                604800 ) ; Negative Cache TTL
    @             IN         NS        ns.kubeadm.ru.
    2             IN         PTR       ns.kubeadm.ru.
    3             IN         PTR       ldap.kubeadm.ru.
    4             IN         PTR       keycloak.kubeadm.ru.
    ;
    40            IN         PTR       gitlab.kubeadm.ru.
    55            IN         PTR       harbor.kubeadm.ru.
    35            IN         PTR       kafka01.kubeadm.ru.
    36            IN         PTR       kafka02.kubeadm.ru.
    37            IN         PTR       kafka03.kubeadm.ru.
    10            IN         PTR       rancher.kubeadm.ru.
    11            IN         PTR       k8s.kubeadm.ru.
    ;12            IN         PTR       k8s.kubeadm.ru.
    ;13            IN         PTR       k8s.kubeadm.ru.
    11            IN         PTR       master01.kubeadm.ru.
    ;12            IN         PTR       master02.kubeadm.ru.
    ;13            IN         PTR       master03.kubeadm.ru.
    14            IN         PTR       worker01.kubeadm.ru.
    15            IN         PTR       worker02.kubeadm.ru.
    16            IN         PTR       worker03.kubeadm.ru.
    20            IN         PTR       ceph01.kubeadm.ru.
    21            IN         PTR       ceph02.kubeadm.ru.
    22            IN         PTR       ceph03.kubeadm.ru.
    251           IN         PTR       api.kubeadm.ru.

  
**9\. Редактируем resolv.conf**  
  
Копируем и вставляем содержимое  
  


Код:
    
    
    rm /etc/resolv.conf && nano /etc/resolv.conf

Код:
    
    
    nameserver 127.0.0.1

Код:
    
    
    systemctl restart bind9

Код:
    
    
    systemctl status bind9

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-09-22 в 10.13.26.png Просмотров:	0 Размер:	54.0 Кб ID:	3955](images\\img_3955_1726989437.jpg)  
  
  
**10\. Проверка:**  
  


Код:
    
    
    nslookup mail.ru

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-22 в 15.09.32.png Просмотров:	0 Размер:	29.1 Кб ID:	2109](images\\img_2109_1690027857.jpg)  
  
Проверим прямую зону  
  
**!! Имя домена вводим свое !!!**  
  


Код:
    
    
    nslookup gitlab.kubeadm.ru

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-10-06 в 9.44.08.png Просмотров:	0 Размер:	13.4 Кб ID:	4095](images\\img_4095_1728197087.jpg)  
  
Проверим обратную зону  
  


Код:
    
    
    nslookup 20.20.20.55

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-10-06 в 9.45.04.png Просмотров:	0 Размер:	8.5 Кб ID:	4096](images\\img_4096_1728197149.jpg)  
  
  
**Поздравляю, настройка завершена!**


---

