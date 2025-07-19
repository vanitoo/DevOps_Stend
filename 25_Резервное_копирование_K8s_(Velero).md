---
layout: default
title: 25_Резервное копирование K8s (Velero)
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Резервное копирование K8s (Velero) 

11-17-2023, 08:51 AM

Источник [тут](https://habr.com/ru/articles/671706/)  
  
  
**1\. Установка клиента**  
  
Проверим актуальную версию  
  


Код:
    
    
    https://github.com/vmware-tanzu/velero/releases

**Для Linux**  
  
Вводим в консоли master01  
  


Код:
    
    
    wget https://github.com/vmware-tanzu/velero/releases/download/v1.12.1/velero-v1.12.1-linux-amd64.tar.gz

Код:
    
    
    tar -xvf velero-v1.12.1-linux-amd64.tar.gz -C ./ --strip-components=1

Код:
    
    
    mv velero /usr/local/bin/

Код:
    
    
    chmod +x /usr/local/bin/velero

Код:
    
    
    velero version

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-15 в 8.06.44.png Просмотров:	0 Размер:	21.7 Кб ID:	4387](images\\img_4387_1734239245.jpg)  
  
**2\. Создаем Bucket в CEPH S3 API**  
  


Код:
    
    
    https://ceph01:8443

Код:
    
    
    velero

  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-11-17 в 10.05.18.png Просмотров:	0 Размер:	45.9 Кб ID:	2871](images\\img_2871_1700204828.jpg)  
  
**3\. Настройка клиента**  
  
Заходим в консоль ceph01  
  


Код:
    
    
    cd /root

Код:
    
    
    cat access_key
    cat secret_key

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-11-17 в 9.16.32.png Просмотров:	0 Размер:	17.8 Кб ID:	2869](images\\img_2869_1700201854.jpg)  


Код:
    
    
    nano credentials-velero

Код:
    
    
    [default]    
    aws_access_key_id = <key>
    aws_secret_access_key = <secret>

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2023-11-17 в 9.18.06.png Просмотров:	0 Размер:	17.1 Кб ID:	2870](images\\img_2870_1700201918.jpg)  
  
**4\. Установка**  
  
**!!! Имя домена вводим свое !!!**  
  


Код:
    
    
    velero install \
    --provider aws \
    --plugins velero/velero-plugin-for-aws:v1.8.1 \
    --bucket velero \
    --secret-file ./credentials-velero \
    --use-volume-snapshots=false \
    --backup-location-config region="eu-central-1",s3ForcePathStyle="true",s3Url=http://s3.kubeadm.ru:8000 \
    --features=EnableCSI \
    --plugins velero/velero-plugin-for-aws:v1.8.1,velero/velero-plugin-for-csi:v0.2.0

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-12-15 в 8.16.59.png Просмотров:	0 Размер:	21.0 Кб ID:	4388](images\\img_4388_1734239857.jpg)  
  
**5\. Выполним первую архивацию**  
  
Для теста выполним архивацию namespaces "landing-page"  
  


Код:
    
    
    sudo velero backup create landing-page --include-namespaces landing-page --include-cluster-resources=true

Проверим  
  


Код:
    
    
    sudo velero backup describe landing-page

  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2024-11-14 в 8.43.22.png Просмотров:	0 Размер:	22.1 Кб ID:	4178](images\\img_4178_1731563107.jpg)  
  
  
**6\. Восстановление**  
  


Код:
    
    
    sudo velero restore create --from-backup landing-page --namespace-mappings landing-page:landing-page-restore

**7\. Удалить архивы (по желанию)**  
  


Код:
    
    
    sudo velero backup delete landing-page

  
**Поздравляю, восстановление завершено!**


---

