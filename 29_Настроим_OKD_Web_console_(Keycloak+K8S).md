---
layout: default
title: 29_Настроим OKD Web console (Keycloak+K8S)
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Настроим OKD Web console (Keycloak+K8S) 


Источник [тут](https://habr.com/ru/articles/850864/)  
  
  
**1\. Создаем клиента Kubernetes в Keycloak**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-06 в 21.56.32.png Просмотров:	0 Размер:	39.4 Кб ID:	4539](images\\img_4539_1738868313.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-06 в 21.58.47.png Просмотров:	0 Размер:	37.1 Кб ID:	4540](images\\img_4540_1738868394.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-06 в 22.00.07.png Просмотров:	0 Размер:	36.9 Кб ID:	4541](images\\img_4541_1738868439.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-06 в 22.03.15.png Просмотров:	0 Размер:	52.0 Кб ID:	4543](images\\img_4543_1738868703.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-06 в 22.05.59.png Просмотров:	0 Размер:	35.0 Кб ID:	4544](images\\img_4544_1738868803.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-06 в 22.07.04.png Просмотров:	0 Размер:	27.6 Кб ID:	4545](images\\img_4545_1738868851.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-06 в 22.07.41.png Просмотров:	0 Размер:	44.3 Кб ID:	4546](images\\img_4546_1738868887.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-06 в 22.01.03.png Просмотров:	0 Размер:	66.4 Кб ID:	4542](images\\img_4542_1738868562.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-06 в 22.08.54.png Просмотров:	0 Размер:	54.2 Кб ID:	4548](images\\img_4548_1738869019.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-06 в 22.10.52.png Просмотров:	0 Размер:	47.3 Кб ID:	4549](images\\img_4549_1738869106.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-06 в 22.11.58.png Просмотров:	0 Размер:	40.8 Кб ID:	4550](images\\img_4550_1738869166.png)  
  
**2\. Покупаем Wildcard сертификат**  
  
Инструкция [тут](https://forum.kubeadm.ru/node/3514)  
  
**3\. Копируем содержимое сертификатов**  
  
Вводим в консоли master01  
  


Код:
    
    
    nano /etc/kubernetes/pki/keycloak-ca.crt

Код:
    
    
    nano ca.crt

Код:
    
    
    nano tls.crt

Код:
    
    
    nano tls.key

Копируем из консоли ns  
  


Код:
    
    
    cat /media/data/easy-rsa/pki/private/keycloak.kubeadm.ru.key

Код:
    
    
    kubectl create secret generic console-serving-cert \
      --from-file=tls.crt \
      --from-file=tls.key \
      --from-file=ca.crt \
      --namespace openshift-console

Проверим  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-07 в 11.51.38.png Просмотров:	0 Размер:	57.1 Кб ID:	4556](images\\img_4556_1738918346.png)  
  
**4\. Включим OIDC в Kubernetes**  
  
**!!! Соблюдаем отступы !!!**  
  


Код:
    
    
    nano /etc/kubernetes/manifests/kube-apiserver.yaml

Код:
    
    
        - --oidc-ca-file=/etc/kubernetes/pki/keycloak-ca.crt
        - --oidc-client-id=kubernetes
        - --oidc-groups-claim=groups
        - --oidc-issuer-url=https://keycloak.kubeadm.ru/realms/kubernetes
        - --oidc-username-claim=preferred_username
        - --oidc-username-prefix=-

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-07 в 11.36.24.png Просмотров:	0 Размер:	36.3 Кб ID:	4559](images\\img_4559_1738918856.png)  
  
**!!! Ждем перезапуск подов !!!**  
  


Код:
    
    
    KUBE_EDITOR="nano" kubectl edit -n kube-system configmaps kubeadm-config

Код:
    
    
          extraArgs:
            oidc-ca-file=/etc/kubernetes/pki/keycloak-ca.crt
            oidc-client-id=kubernetes
            oidc-groups-claim=groups
            oidc-issuer-url=https://keycloak.kubeadm.ru/realms/kubernetes
            oidc-username-claim=preferred_username
            oidc-username-prefix=-

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-07 в 11.58.17.png Просмотров:	0 Размер:	35.4 Кб ID:	4557](images\\img_4557_1738918754.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-07 в 11.59.32.png Просмотров:	0 Размер:	13.5 Кб ID:	4558](images\\img_4558_1738918814.png)  
  
Проверим  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-07 в 12.02.27.png Просмотров:	0 Размер:	85.7 Кб ID:	4560](images\\img_4560_1738918985.png)  
  
**5\. Сохраним образ веб консоли в Harbor**  
  


Код:
    
    
    docker pull quay.io/openshift/origin-console:4.12.0

Код:
    
    
    docker images | more

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-07 в 8.10.35.png Просмотров:	1 Размер:	8.5 Кб ID:	4555](images\\img_4555_1738907166.png)  
  


Код:
    
    
    docker tag b9349dc7ce6d harbor.kubeadm.ru/library/origin-console:4.12.0

Код:
    
    
    docker login -u admin -p Harbor12345 harbor.kubeadm.ru

Код:
    
    
    docker push harbor.kubeadm.ru/library/origin-console:4.12.0

**6\. Привяжем роль**  
  


Код:
    
    
    nano keycloak-user-binding.yml

Код:
    
    
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: keycloak-user-binding
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: cluster-admin
    subjects:
      - kind: User
        name: jane # The Keycloak username
        apiGroup: rbac.authorization.k8s.io

Код:
    
    
    kubectl apply -f keycloak-user-binding.yml

Добавление пользователей к роли  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-22 в 7.06.02 \(2\).png Просмотров:	1 Размер:	122.2 Кб ID:	4618](images\\img_4618_1740197333.png)  
  
* Добавляем роль cluster-admin  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-05-03 в 21.18.10.png Просмотров:	11 Размер:	95.5 Кб ID:	4784](images\\img_4784_1746296522.png)  
  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-05-03 в 21.18.22.png Просмотров:	9 Размер:	50.5 Кб ID:	4785](images\\img_4785_1746296543.png)  
  
**7\. Копируем содержимое[архива](https://galkin-vladimir.ru:5446/d/s/127VmNHZlLYGYiHCtsgtpMxSp5G4pXCp/72qkPjc0flWteODQAngufDOMbaexg6MM-Cv9APAvOCww)**  
  
**!!! Соблюдаем отступы !!!**  
  


Код:
    
    
    nano namespaces-serviceaccouns-clusterrolebindings.yml

Код:
    
    
    nano openshift_console_secret.yml

Код:
    
    
    nano openshift_console_ingress.yml

Код:
    
    
    nano openshift_console_deploy.yml

Редактируем своими параметрами  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-07 в 8.13.32.png Просмотров:	0 Размер:	30.2 Кб ID:	4553](images\\img_4553_1738905710.png)  
  
  


Код:
    
    
    kubectl apply -f namespaces-serviceaccouns-clusterrolebindings.yml

Код:
    
    
    kubectl apply -f openshift_console_secret.yml

Код:
    
    
    kubectl apply -f openshift_console_deploy.yml

Код:
    
    
    kubectl apply -f openshift_console_ingress.yml

Проверим  
  
**!!! Ждем завершение процесса !!!**  
  


Код:
    
    
    kubectl get pod -n openshift-console

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-06 в 23.02.16.png Просмотров:	0 Размер:	14.8 Кб ID:	4552](images\\img_4552_1738872207.png)  
  
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
    
    
    20.20.20.77 console.kubeadm.ru

**9\. Откроем веб консоль**  
  


Код:
    
    
    https://console.kubeadm.ru/

Код:
    
    
    login: jane
    password: foo_password

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-06 в 21.05.58.png Просмотров:	0 Размер:	62.5 Кб ID:	4538](images\\img_4538_1738865189.png)  
  
**10\. Включаем console links, ConsoleNotification, ConsoleCLIDownload**  
  


Код:
    
    
    wget https://raw.githubusercontent.com/openshift/api/refs/heads/release-4.12/console/v1/0000_10_consolelink.crd.yaml

Код:
    
    
    wget https://raw.githubusercontent.com/openshift/api/refs/heads/release-4.12/console/v1/0000_10_consoleclidownload.crd.yaml

Код:
    
    
    wget https://raw.githubusercontent.com/openshift/api/refs/heads/release-4.12/console/v1/0000_10_consolenotification.crd.yaml

Код:
    
    
    kubectl apply -f 0000_10_consolelink.crd.yaml

Код:
    
    
    kubectl apply -f 0000_10_consoleclidownload.crd.yaml

Код:
    
    
    kubectl apply -f 0000_10_consolenotification.crd.yaml

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-07 в 12.24.47.png Просмотров:	0 Размер:	33.2 Кб ID:	4561](images\\img_4561_1738920333.png)  
  
Пример  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-07 в 12.33.46.png Просмотров:	0 Размер:	49.0 Кб ID:	4562](images\\img_4562_1738921200.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-07 в 12.50.05.png Просмотров:	0 Размер:	44.8 Кб ID:	4565](images\\img_4565_1738921952.png)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-07 в 12.52.39.png Просмотров:	0 Размер:	22.0 Кб ID:	4566](images\\img_4566_1738922011.png)  
  
  
  
**Поздравляю, настройка завершена!**

Вложения 

  * [ ![Нажмите на изображение для увеличения.



Название:	Снимок экрана 2025-02-06 в 22.08.54.png

Просмотров:	56

Размер:	54.2 Кб

ID:	4547](images\\img_4547_0.png) ](filedata/fetch?id=4547)




---

