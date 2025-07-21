---
layout: default
title: 23_Развёртывание Django Web Server в Интенет
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Развёртывание Django Web Server в Интенет 

Источник [тут](https://github.com/Williano/Landing-Page/tree/master)  
  
**1\. Добавляем наш проект в Harbor**  
  


Код:
    
    
    https://harbor.kubeadm.ru

Код:
    
    
    landing-page

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-20 в 16.14.05.png Просмотров:	0 Размер:	20.7 Кб ID:	4237](images\\img_4237_1732108477.png)  
  
**2\. Добавляем новый проект "landing-page" в Kubernetes**  
  
Вводим в консоли work  
  


Код:
    
    
    kubectl create namespace landing-page

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-20 в 10.04.51.png Просмотров:	0 Размер:	5.3 Кб ID:	4227](images\\img_4227_1732086324.png)  
  


Код:
    
    
    kubectl config set-context --current --namespace=landing-page

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-20 в 10.05.30.png Просмотров:	0 Размер:	10.7 Кб ID:	4228](images\\img_4228_1732086364.png)  
  
**3\. Покупаем Wildcard сертификат**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/3514)  
  
**4\. Добавим свои коммерческие SSL сертификаты**  
  
Вводим в консоли work  
  


Код:
    
    
    mkdir certs && cd certs

Копируем содержимое ваших сертификатов  
  
**!!! Имя домена у вас свое !!!**  
  


Код:
    
    
    nano kubeadm.ru.crt

Код:
    
    
    nano kubeadm.ru.key

Код:
    
    
    kubectl create secret tls kubeadm-tls --cert=kubeadm.ru.crt --key=kubeadm.ru.key

Проверим  
  


Код:
    
    
    kubectl get secret

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-20 в 15.35.54.png Просмотров:	0 Размер:	10.4 Кб ID:	4229](images\\img_4229_1732106210.png)  
  


Код:
    
    
    kubectl get secret kubeadm-tls -o yaml

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-20 в 15.37.15.png Просмотров:	0 Размер:	30.6 Кб ID:	4230](images\\img_4230_1732106269.png)  
  
**5\. Создаем пустой проект в Gitlab**  
  


Код:
    
    
    landing-page

**6\. Загружаем наш проект из GitLab в IDE**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-20 в 15.40.07.png Просмотров:	0 Размер:	37.0 Кб ID:	4231](images\\img_4231_1732106438.png)  
  
**7\. Выбираем IDE**  
  
Настройка _**[PyCharm](https://forum.kubeadm.ru/node/4791)**_  
  
ниже _**[Visual Studio Code](https://code.visualstudio.com/download)**_  
  
Клонируем репозиторий  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-20 в 15.41.59.png Просмотров:	0 Размер:	33.9 Кб ID:	4232](images\\img_4232_1732106608.png)  
  
**8\. Скачиваем[архив](https://galkin-vladimir.ru:5446/d/s/13dCk63bU1BtZL9x5aZKDMYVmfYDvbLY/xmuIhTgSjcWomVBtZ0CCF3A3081cz2X5-mrrgAHl7VAw)**  
  
Копируем содержимое архива в проект  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-20 в 15.44.40.png Просмотров:	0 Размер:	30.1 Кб ID:	4233](images\\img_4233_1732106763.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-20 в 15.44.52.png Просмотров:	0 Размер:	17.0 Кб ID:	4234](images\\img_4234_1732106805.png)  
  
**9\. Включаем SSL**  
  
**!!! Имя домена у вас свое !!!**  
  
Открываем файл проекта  
  


Код:
    
    
    values.yaml

Код:
    
    
    kubeadm-tls

Код:
    
    
    landing-page.kubeadm.ru

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-20 в 16.17.04.png Просмотров:	0 Размер:	32.3 Кб ID:	4238](images\\img_4238_1732108670.png)  
  
**!!! Переименуем файл !!!**  
  
Спереди ставим точку  
  


Код:
    
    
    **.** gitlab-ci.yml

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-20 в 15.52.38.png Просмотров:	0 Размер:	24.4 Кб ID:	4235](images\\img_4235_1732107213.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-20 в 15.53.53.png Просмотров:	0 Размер:	17.9 Кб ID:	4236](images\\img_4236_1732107292.png)  
  
**10\. Добавляем запись в файл на своем ПК**  
  
Для OSX  
  


Код:
    
    
    sudo nano /private/etc/hosts

Для Windows  
  


Код:
    
    
    C:\Windows\System32\drivers\etc\hosts

Код:
    
    
    20.20.20.77 landing-page.kubeadm.ru

Проверим  
  


Код:
    
    
    https://landing-page.kubeadm.ru

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-20 в 16.44.23.png Просмотров:	0 Размер:	48.1 Кб ID:	4239](images\\img_4239_1732110305.png)  
  
**11\. Проверяем**  
  
Откроем браузер на мобильном или другом ПК подключенным к интернету  
  


Код:
    
    
    https://landing-page.kubeadm.ru

**12\. Обновление SSL сертификата (по требованию)**  
  


Код:
    
    
    kubectl config set-context --current --namespace=landing-page

Код:
    
    
    kubectl delete secret kubeadm-tls --ignore-not-found

Код:
    
    
    kubectl create secret tls kubeadm-tls --cert=kubeadm.ru.crt --key=kubeadm.ru.key

**Поздравляю, настройка завершена!**


---

