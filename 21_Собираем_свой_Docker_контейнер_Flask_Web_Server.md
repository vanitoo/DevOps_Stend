---
layout: default
title: 21_Собираем свой Docker контейнер Flask Web Server
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Собираем свой Docker контейнер Flask Web Server 

vCPU = 4  
vRAM = 4 Gb  
vHDD1 = 40 Gb  
  
**1\. Подготовим 1 виртуальную машину**  
  
Клонируем шаблон k8s-UbuntuTemplate  
  
Меняем IP и имена хостов на каждом узле  
  


Код:
    
    
    rm /etc/resolv.conf && nano /etc/resolv.conf

Код:
    
    
    nameserver 20.20.20.2

Код:
    
    
    nano /etc/netplan/01-netcfg.yaml

Код:
    
    
    20.20.20.50

Код:
    
    
    nano /etc/hostname

Код:
    
    
    work

Код:
    
    
    reboot

**2\. Установка Docker & Docker-Compose**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/398)  
  
**3.** **Установка Kubectl:**  
  
Add the Kubernetes repository  
  


Код:
    
    
    mkdir -p /etc/apt/keyrings

Код:
    
    
    curl -fsSL https://pkgs.k8s.io/core:/stable:/**v1.30** /deb/Release.key |gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

Код:
    
    
    echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/**v1.30** /deb/ /" |tee /etc/apt/sources.list.d/kubernetes.list

Код:
    
    
    apt-get update && apt-get install -y kubectl

Проверим:  
  


Код:
    
    
    kubectl version --client

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 14.43.32.png Просмотров:	0 Размер:	11.7 Кб ID:	4191](images\\img_4191_1732016677.png)  
  


Код:
    
    
    mkdir -p /root/.kube/ && nano /root/.kube/config

Копируем содержимое из консоли master01  
  


Код:
    
    
    cat .kube/config

Проверим  
  
Получим список нод  
  


Код:
    
    
    kubectl get nodes

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 14.53.57.png Просмотров:	0 Размер:	14.6 Кб ID:	4192](images\\img_4192_1732017269.png)  
  
Получим список всех namespace  
  


Код:
    
    
    kubectl get namespace

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 14.54.44.png Просмотров:	0 Размер:	19.9 Кб ID:	4193](images\\img_4193_1732017309.png)  
  
**4\. Ставим Helm**  
  


Код:
    
    
    wget https://get.helm.sh/helm-v3.12.1-linux-amd64.tar.gz

Код:
    
    
    tar -xvzf helm-v3.12.1-linux-amd64.tar.gz -C /usr/local/bin --strip-components=1

Проверим  
  


Код:
    
    
    helm version

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 14.56.39.png Просмотров:	0 Размер:	10.2 Кб ID:	4194](images\\img_4194_1732017436.png)  
  
**5\. Создаем наше приложение**  
  


Код:
    
    
    cd /root

Код:
    
    
    mkdir App && cd App

**!!! Соблюдаем отступы !!!**  
  


Код:
    
    
    nano app.py

Код:
    
    
    from flask import Flask
    
    app = Flask(__name__)
    
    
    @app.route('/')
    def hello_world():
          return 'Привет Мир!'
    
    
    if __name__ == '__main__':
         app.run(debug=True,host='0.0.0.0')

Код:
    
    
    nano requirements.txt

Код:
    
    
    Flask==2.2.2
    Werkzeug==2.3.7

**6\. Собираем наш контейнер**  
  


Код:
    
    
    cd ..

**!!! Имя домена у вас свое !!!**  
  


Код:
    
    
    nano Dockerfile

Код:
    
    
    FROM harbor.kubeadm.ru/mirror.docker.hub/library/python:3.10
    RUN python3 -m pip install --user --upgrade pip
    COPY ["App","App"]
    WORKDIR /App
    RUN python3 -m pip install -r requirements.txt
    EXPOSE 5000
    ENTRYPOINT ["python3", "app.py"]

**!!! Точка в конце строки обязательна !!!**  
  


Код:
    
    
    docker build --no-cache -t harbor.kubeadm.ru/myproject/my-flaskproject:latest **.**

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 15.07.34.png Просмотров:	0 Размер:	10.6 Кб ID:	4195](images\\img_4195_1732018116.png)  
  
Проверим  
  


Код:
    
    
    docker images

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 15.08.56.png Просмотров:	0 Размер:	23.0 Кб ID:	4196](images\\img_4196_1732018185.png)  
  
**7\. Запустим наш контейнер**  
  


Код:
    
    
    docker run --name flask-project -d -p 5000:5000 harbor.kubeadm.ru/myproject/my-flaskproject:latest

Проверим  
  


Код:
    
    
    docker ps -a

Откроем веб интерфейс  
  


Код:
    
    
    http://20.20.20.50:5000

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 15.13.13.png Просмотров:	0 Размер:	6.8 Кб ID:	4198](images\\img_4198_1732018435.png)  
  
**8\. Загрузим наш проект в Harbor (Docker Registry)**  
  
Открываем в браузере  
  


Код:
    
    
    https://harbor.kubeadm.ru

В водим логин и пароль  
  


Код:
    
    
    admin
    Harbor12345

![Нажмите на изображение для увеличения.  Название:	image_1084.png Просмотров:	0 Размер:	11.1 Кб ID:	2711](images\\img_2711_1683106253.png)  
  
Добавляем наш проект  
  


Код:
    
    
    myproject

![Нажмите на изображение для увеличения.  Название:	image_1341.png Просмотров:	0 Размер:	8.8 Кб ID:	2712](images\\img_2712_1685177789.png)  
  
![Нажмите на изображение для увеличения.  Название:	image_1342.png Просмотров:	0 Размер:	20.8 Кб ID:	2713](images\\img_2713_1685177867.png)  
  
**9\. Сохраним наш образ в репозиторий Harbor**  
  


Код:
    
    
    docker login -u admin -p Harbor12345 harbor.kubeadm.ru

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 15.17.28.png Просмотров:	0 Размер:	29.3 Кб ID:	4199](images\\img_4199_1732018715.png)  
  


Код:
    
    
    docker push "harbor.kubeadm.ru/myproject/my-flaskproject:latest"

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 15.18.51.png Просмотров:	0 Размер:	63.4 Кб ID:	4200](images\\img_4200_1732018780.png)  
  
Проверим  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-07-25 в 19.23.56.png Просмотров:	0 Размер:	22.2 Кб ID:	2242](images\\img_2242_1690302288.png)  
  
**10\. Загружаем наше приложение в Kubernetes**  
  
Создадим структуру каталогов  
  


Код:
    
    
    cd /root

Код:
    
    
    helm create myapp

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 15.20.44.png Просмотров:	0 Размер:	10.4 Кб ID:	4201](images\\img_4201_1732018886.png)  
  
Редактируем файл с параметрами по умолчанию  
  


Код:
    
    
    nano /root/myapp/values.yaml

**!!! Соблюдаем отступы !!!**  
  
**!!! Имя домена у вас свое !!!**  
  


Код:
    
    
    repository: harbor.kubeadm.ru/myproject/my-flaskproject
    pullPolicy: Always
    tag: "latest"

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 15.24.48.png Просмотров:	0 Размер:	31.6 Кб ID:	4202](images\\img_4202_1732019146.png)  
  
**!!! Ниже по тексту !!!**  
  


Код:
    
    
    type: LoadBalancer
    port: 5000
    enabled: true
    className: "nginx"
    host: hello-world.info

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 16.20.50.png Просмотров:	0 Размер:	27.8 Кб ID:	4215](images\\img_4215_1732022635.png)  
  
**11\. Добавим новый namespace в Kubernetes**  
  


Код:
    
    
    kubectl create namespace myproject

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 15.35.28.png Просмотров:	0 Размер:	7.0 Кб ID:	4204](images\\img_4204_1732019775.png)  
  
Перейдем в новый namespace  
  


Код:
    
    
    kubectl config set-context --current --namespace=myproject

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 15.36.58.png Просмотров:	0 Размер:	11.1 Кб ID:	4205](images\\img_4205_1732019855.png)  
  
Получим текущий список подов  
  


Код:
    
    
    kubectl get pod

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 15.37.51.png Просмотров:	0 Размер:	7.5 Кб ID:	4206](images\\img_4206_1732019943.png)  
  
**12\. Установим приложение в Kubernetes**  
  


Код:
    
    
    helm install myapp --namespace myproject myapp

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 16.17.33.png Просмотров:	0 Размер:	37.9 Кб ID:	4213](images\\img_4213_1732022324.png)  
  
Проверим  
  


Код:
    
    
    kubectl get pod

**!!! Ждём запуска pod !!!**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 15.42.00.png Просмотров:	0 Размер:	13.1 Кб ID:	4208](images\\img_4208_1732020202.png)  
  
**13\. Добавляем запись в файл на своем ПК**  
  
Для OSX  
  


Код:
    
    
    sudo nano /private/etc/hosts

Для Windows  
  


Код:
    
    
    C:\Windows\System32\drivers\etc\hosts

Код:
    
    
    20.20.20.77 hello-world.local

Откроем браузер  
  


Код:
    
    
    http://hello-world.local

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 16.19.19.png Просмотров:	0 Размер:	6.1 Кб ID:	4214](images\\img_4214_1732022399.png)  
  
**15\. Удалим приложение из Rancher**  
  
**!!! Все манипуляции с приложениями проводим только через HELM во избежание не согласованности статусов !!!**  
  


Код:
    
    
    helm list

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 15.59.21.png Просмотров:	0 Размер:	11.9 Кб ID:	4210](images\\img_4210_1732021229.png)  
  


Код:
    
    
    helm uninstall myapp

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 16.00.42.png Просмотров:	0 Размер:	10.3 Кб ID:	4211](images\\img_4211_1732021291.png)  
  
Проверим  
  


Код:
    
    
    kubectl get pod

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-19 в 16.01.44.png Просмотров:	0 Размер:	7.4 Кб ID:	4212](images\\img_4212_1732021392.png)  
  
**Поздравляю, настройка завершена!**

Вложения 

  * [ ![Нажмите на изображение для увеличения.



Название:	Снимок экрана 2023-05-24 в 17.37.19.png

Просмотров:	252

Размер:	15.8 Кб

ID:	1732](images\\img_1732_0.png) ](filedata/fetch?id=1732)




---

