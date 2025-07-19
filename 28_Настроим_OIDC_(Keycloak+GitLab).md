---
layout: default
title: 28_Настроим OIDC (Keycloak+GitLab)
---
<a class="back-link" href="index.html">⬅ Назад к списку</a>


##  Настроим OIDC (Keycloak+GitLab) 

02-01-2025, 11:27 PM

Источник [тут](https://vk.com/wall-226121191_212?ysclid=m6mn2pgq6t863888093)  
Источник [тут](https://bytegoblin.io/blog/kubernetes-authentication-with-keycloak-oidc.mdx)  
Источник [тут](https://www.0xbbeer.ru/posts/config-sso-for-gitlab/)  
  
  
**1\. Создаем клиента Gitlab в Keycloak**  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-04 в 8.04.03.png Просмотров:	0 Размер:	36.9 Кб ID:	4501](images\\img_4501_1738650077.jpg)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-04 в 8.04.29.png Просмотров:	0 Размер:	52.5 Кб ID:	4502](images\\img_4502_1738650091.jpg)  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-04 в 12.32.29.png Просмотров:	0 Размер:	24.9 Кб ID:	4505](images\\img_4505_1738661718.jpg)  
  
**2\. Добавляем настройку в начало файла**  
  
Вводим в консоли [**gitlab**](https://forum.kubeadm.ru/node/771)  
  
**!!! Соблюдаем отступы !!!**  
  


Код:
    
    
    nano /media/data/gitlab/config/gitlab.rb

Код:
    
    
    #
    gitlab_rails['env'] = {
      SSL_CERT_FILE: "/etc/gitlab/trusted-certs/ca.crt"
    }
    #
    gitlab_rails['omniauth_enabled'] = true
    gitlab_rails['omniauth_allow_single_sign_on'] = true
    gitlab_rails['omniauth_sync_email_from_provider'] = 'openid_connect'
    gitlab_rails['omniauth_block_auto_created_users'] = false
    gitlab_rails['omniauth_auto_link_ldap_user'] = false
    gitlab_rails['omniauth_auto_link_user'] = ["openid_connect"]
    #
    gitlab_rails['omniauth_providers'] = [
      {
        "name" => "keycloak",
        "label" => "Keycloak SSO",
        "args" => {
          "name" => "openid_connect",
          "scope" => ["openid", "profile", "email"],
          "response_type" => "code",
          "issuer" => "https://keycloak.kubeadm.ru/realms/kubernetes",
          "client_auth_method" => "query",
          "uid_field" => "preferred_username",
          "discovery" => true,
          "client_options" => {
            "identifier" => "gitlab",
            "secret" => "**< ACCESS_TOKEN>**",
            "redirect_uri" => "https://gitlab.kubeadm.ru/users/auth/openid_connect/callback"
          }
        }
      }
    ]
    #

Заменим <ACCESS_TOKEN> своим токеном  
  
  
![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-04 в 13.56.50.png Просмотров:	0 Размер:	43.7 Кб ID:	4509](images\\img_4509_1738666744.jpg)  
  
**3\. Добавим корневой сертификат**  
  
Вводим в консоли [**gitlab**](https://forum.kubeadm.ru/node/771)  
  


Код:
    
    
    nano /media/data/gitlab/config/trusted-certs/ca.crt

Копируем содержимое консоли [**ns**](https://forum.kubeadm.ru/node/239)  
  


Код:
    
    
    20.20.20.2

Код:
    
    
    cat /media/data/easy-rsa/pki/ca.crt

Применим  
  


Код:
    
    
    docker-compose restart

Проверим  
  


Код:
    
    
    https://gitlab.kubeadm.ru

Код:
    
    
    login: jane
    password: foo_password

![Нажмите на изображение для увеличения.  Название:	Снимок экрана 2025-02-04 в 12.36.23.png Просмотров:	1 Размер:	7.2 Кб ID:	4506](images\\img_4506_1738661823.jpg)  
  
  
  
**Поздравляю, настройка завершена!**


---

