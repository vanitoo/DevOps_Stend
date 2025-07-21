---
layout: default
title: 59_Настроим_GitLab_Runner
---
<a class="back-link" href="../index.html">⬅ Назад к списку</a>


##  Настроим GitLab Runner 


Источник [тут](https://gist.github.com/k-srkw/822b4be155cb96f51e49bfae6b8cbba0)  
  
  


Код:
    
    
    sudo oc new-project gitlab-runner

Код:
    
    
    sudo oc adm policy add-scc-to-user anyuid -z default -n gitlab-runner

Код:
    
    
    sudo oc policy add-role-to-user edit "system:serviceaccount:gitlab-runner:default"

Код:
    
    
    sudo helm repo add gitlab https://charts.gitlab.io

Код:
    
    
    sudo helm search repo -l gitlab/gitlab-runner

Код:
    
    
    sudo helm install /
    --namespace gitlab-runner /
    --version 0.64.0 gitlab-runner-01 gitlab/gitlab-runner /
    --set gitlabUrl=https://gitlab.kubeadm.ru /
    --set runnerRegistrationToken=glpat-xxxxxxxx-xxxxxxxxxxx

Код:
    
    
    sudo helm delete gitlab-runner-01 --namespace gitlab-runner

Код:
    
    
    sudo helm upgrade gitlab-runner --set gitlabUrl=https://gitlab.kubeadm.ru,runnerRegistrationToken=glpat-xxxxxxxx-xxxxxxxxxxx gitlab/gitlab-runner

**Поздравляю, настройка завершена!**  



---

