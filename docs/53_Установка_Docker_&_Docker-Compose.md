---
layout: default
title: 53_Установка_Docker_&_Docker-Compose
---
<a class="back-link" href="../index.html">⬅ Назад к списку</a>


##  Установка Docker & Docker-Compose 

  
**1\. Ставим Docker**  
  


Код:
    
    
    apt-get update && apt-get install -y docker.io

Код:
    
    
    mkdir -p /media/data/docker

Код:
    
    
    nano /etc/docker/daemon.json

Код:
    
    
    {
    "data-root":"/media/data/docker",
    "dns":["20.20.20.2"],
    "log-driver": "json-file",
    "log-opts": {"max-size": "10m", "max-file": "3"}
    }

Код:
    
    
    systemctl daemon-reload

Код:
    
    
    systemctl restart docker && systemctl status docker

[Ctrl]+[C]  
  
Проверим  
  


Код:
    
    
    docker info | grep Root

**2\. Ставим Docker-Compose**  
  


Код:
    
    
    curl -L https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose

Код:
    
    
    chown root:root -R /usr/local/bin/docker-compose
    chmod 755 -R /usr/local/bin/docker-compose

**3\. Покупаем Wildcard сертификат**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/3514)  
  
**4\. Обновляем сертификаты**  
  


Код:
    
    
    mkdir -p /etc/docker/certs.d/harbor.kubeadm.ru

Копируем содержимое сертификатов  
  


Код:
    
    
    nano /etc/docker/certs.d/harbor.kubeadm.ru/ca.crt

Код:
    
    
    cp /etc/docker/certs.d/harbor.kubeadm.ru/ca.crt /usr/local/share/ca-certificates/ca.crt

Код:
    
    
    update-ca-certificates --fresh

**Поздравляю, настройка завершена!**


---

