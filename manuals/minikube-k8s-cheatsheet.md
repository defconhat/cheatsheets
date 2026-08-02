# ☸️ Minikube / Kubernetes (kubectl) — шпаргалка

> **Kubernetes (K8s)** — оркестратор контейнеров.
> **Minikube** — локальный кластер K8s для разработки/обучения.
> **kubectl** — CLI-клиент для управления K8s.
> Документация: https://kubernetes.io/docs · https://minikube.sigs.k8s.io

---

## 🔑 Главные понятия K8s

| Термин | Что значит |
|---|---|
| **Cluster** | Кластер (набор узлов) |
| **Node** | Узел (машина) — Master/Worker |
| **Pod** | Минимальная единица, 1+ контейнеров |
| **Deployment** | Управляет репликами Pod'ов |
| **Service** | Сетевой доступ к Pod'ам |
| **Ingress** | HTTP/HTTPS-маршрутизация |
| **ConfigMap** | Конфигурация (не секреты) |
| **Secret** | Секреты (base64) |
| **Volume** | Хранилище данных |
| **PV / PVC** | PersistentVolume / Claim |
| **Namespace** | Логическое разделение кластера |
| **Label / Selector** | Теги и выбор по ним |
| **ReplicaSet** | Гарантирует N реплик |
| **StatefulSet** | Для stateful приложений (БД) |
| **DaemonSet** | Pod на каждом узле |
| **Job / CronJob** | Разовые / по расписанию задачи |
| **Helm** | Пакетный менеджер для K8s |

---

## 🚀 Minikube — локальный кластер

### Установка
```bash
# Arch / CachyOS
sudo pacman -S minikube kubectl

# Debian/Ubuntu
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# macOS
brew install minikube kubectl
```

### Базовые команды
```bash
minikube start                      # запустить (с дефолтным драйвером)
minikube start --driver=docker      # через Docker
minikube start --driver=kvm2        # через KVM (Linux, рекомендуется)
minikube start --driver=virtualbox  # VirtualBox
minikube start --cpus=4 --memory=8g # с ресурсами
minikube start --kubernetes-version=v1.29.0

minikube status                     # статус
minikube stop                       # остановить
minikube delete                     # удалить кластер
minikube pause                      # пауза (без удаления)
minikube unpause

minikube dashboard                  # открыть Web UI в браузере
minikube ip                         # IP-адрес кластера
minikube ssh                        # SSH в ноду
minikube logs                       # логи
minikube version

minikube node list                  # список нод
minikube node add                   # добавить ноду
```

### Addons
```bash
minikube addons list                # доступные аддоны
minikube addons enable ingress      # включить Ingress controller
minikube addons enable metrics-server
minikube addons enable dashboard
minikube addons enable registry
minikube addons enable metallb      # LoadBalancer для локалки
minikube addons disable ingress     # отключить
```

### Профили (несколько кластеров)
```bash
minikube profile list
minikube profile mycluster
minikube start -p mycluster
```

### Образы и реестр
```bash
minikube image load myapp:latest    # загрузить локальный образ в minikube
minikube image ls                   # список образов
minikube image rm myapp:latest

# Использовать локальный реестр
eval $(minikube docker-env)         # использовать Docker minikube
docker build -t myapp .             # теперь образ доступен в кластере
# В deployment: imagePullPolicy: Never
```

---

## 🎯 kubectl — основные команды

### Контекст и конфигурация
```bash
kubectl config view                 # текущий конфиг (~/.kube/config)
kubectl config current-context      # текущий контекст
kubectl config get-contexts         # список контекстов
kubectl config use-context minikube # переключиться
kubectl config set-context --current --namespace=dev

kubectl version                     # версия kubectl и кластера
kubectl version --client            # только клиент
kubectl cluster-info                # инфо о кластере
kubectl api-resources               # типы ресурсов
kubectl api-versions                # версии API
```

### Просмотр ресурсов
```bash
kubectl get pods                    # все поды в текущем namespace
kubectl get pods -A                 # во ВСЕХ namespaces
kubectl get pods -o wide            # подробно (с IP, нодой)
kubectl get pods -w                 # watch (реальное время)
kubectl get pod NAME -o yaml        # в YAML
kubectl get pod NAME -o json        # в JSON
kubectl get pod NAME -o jsonpath='{.status.phase}'   # конкретное поле

kubectl get deploy                  # deployments
kubectl get svc                     # services
kubectl get ingress
kubectl get configmap
kubectl get secret
kubectl get pv,pvc                  # volumes
kubectl get nodes                   # узлы кластера
kubectl get ns                      # namespaces
kubectl get all                     # все ресурсы
kubectl get all -A                  # во всех namespaces
```

### Информация и описание
```bash
kubectl describe pod NAME           # подробная информация
kubectl describe deploy NAME
kubectl describe svc NAME
kubectl logs POD_NAME               # логи контейнера
kubectl logs POD_NAME -c CONTAINER  # конкретный контейнер
kubectl logs -f POD_NAME            # следить (tail -f)
kubectl logs --previous POD_NAME    # логи предыдущего контейнера
kubectl logs -l app=myapp           # по лейблу
kubectl top pod                     # CPU/RAM (нужен metrics-server)
kubectl top node
```

### Выполнение команд
```bash
kubectl exec -it POD_NAME -- bash           # войти в под
kubectl exec POD_NAME -- ls /app            # выполнить команду
kubectl exec POD_NAME -- env                # переменные окружения
kubectl exec POD_NAME -c CONTAINER -- sh    # конкретный контейнер
```

### Port forwarding (для локальной разработки)
```bash
kubectl port-forward svc/myservice 8080:80  # localhost:8080 → service:80
kubectl port-forward pod/mypod 8080:80
kubectl port-forward deploy/myapp 8080:80
```

### Доступ к сервису (minikube)
```bash
minikube service SERVICENAME               # открыть в браузере
minikube service SERVICENAME --url         # только URL
minikube service list                      # список сервисов
```

---

## 📝 Создание ресурсов

### Из YAML-файла
```bash
kubectl apply -f deployment.yaml    # создать/обновить
kubectl apply -f ./manifests/       # все файлы в каталоге
kubectl apply -f https://raw.githubusercontent.com/.../file.yaml
kubectl apply -k ./overlays/dev     # Kustomize
kubectl create -f file.yaml         # только создать (ошибка если есть)
```

### Императивное создание
```bash
kubectl create deployment nginx --image=nginx --replicas=3
kubectl create service clusterip my-svc --tcp=80:80
kubectl create configmap my-cm --from-literal=key=value
kubectl create secret generic my-sec --from-literal=password=secret
kubectl expose deployment nginx --port=80 --type=LoadBalancer
kubectl run tmp-pod --image=alpine --rm -it -- sh   # одноразовый под
```

### Масштабирование
```bash
kubectl scale deployment nginx --replicas=5
kubectl autoscale deployment nginx --min=2 --max=10 --cpu-percent=80
```

### Обновление
```bash
kubectl set image deployment/nginx nginx=nginx:1.25
kubectl rollout status deployment/nginx
kubectl rollout history deployment/nginx
kubectl rollout undo deployment/nginx
kubectl rollout undo deployment/nginx --to-revision=2
kubectl restart deployment/nginx
```

### Удаление
```bash
kubectl delete -f deployment.yaml
kubectl delete pod NAME
kubectl delete pod NAME --grace-period=0 --force  # принудительно
kubectl delete deployment nginx
kubectl delete svc,deploy -l app=myapp            # по лейблу
kubectl delete namespace dev                       # удалить namespace (и всё в нём)
```

---

## 🎨 Пример манифестов

### Deployment + Service
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:1.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-svc
spec:
  type: ClusterIP          # ClusterIP / NodePort / LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
```

### ConfigMap и Secret
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  config.yaml: |
    debug: true
    port: 8080
  LOG_LEVEL: info
---
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  url: cG9zdGdyZXM6Ly91c2VyOnBhc3NAZGI6NTQzMi9teWRi   # base64
# Создание из строки:
# echo -n 'postgres://user:pass@db:5432/mydb' | base64
```

### Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-svc
            port:
              number: 80
```

### PersistentVolumeClaim
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard
```

---

## 🏷️ Labels и Selectors

```bash
kubectl get pods --show-labels
kubectl get pods -l app=myapp           # фильтр по лейблу
kubectl get pods -l 'app in (myapp,web)'
kubectl get pods -l environment=prod,tier=frontend
kubectl label pod NAME env=prod         # добавить
kubectl label pod NAME env-             # удалить
kubectl annotate pod NAME description="..."
```

---

## 🌍 Namespaces

```bash
kubectl get namespaces
kubectl create namespace dev
kubectl delete namespace dev
kubectl config set-context --current --namespace=dev
kubectl get pods -n kube-system        # конкретный namespace
kubectl get pods -A                    # все namespaces
```

---

## 🛠️ Kustomize

Без шаблонизатора (встроено в kubectl):
```
project/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── replicas-patch.yaml
    └── prod/
        ├── kustomization.yaml
        └── replicas-patch.yaml
```

```yaml
# kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
commonLabels:
  app: myapp
namespace: myapp-dev
images:
  - name: myapp
    newTag: 1.0.0
```

```bash
kubectl apply -k ./overlays/dev
kubectl kustomize ./overlays/dev      # показать итоговый YAML
```

---

## 📦 Helm — пакетный менеджер

```bash
helm install my-release bitnami/wordpress
helm upgrade --install my-release bitnami/wordpress -f values.yaml
helm uninstall my-release
helm list
helm search hub wordpress
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm pull bitnami/wordpress --untar      # скачать chart
helm template my-release ./wordpress     # показать итоговые манифесты
```

### Свой chart
```bash
helm create mychart
# values.yaml → что переопределить
helm install my-release ./mychart -f values.yaml
```

---

## 🐛 Дебаг и траблшутинг

### Под не запускается
```bash
kubectl describe pod NAME              # события внизу
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl logs NAME --previous           # почему упал
```

Частые причины:
- `ImagePullBackOff` — образ не существует / нет прав / нет `imagePullPolicy: Never` для локальных.
- `CrashLoopBackOff` — приложение падает. Смотрите логи.
- `Pending` — нет ресурсов / нет ноды / PVC не создан.
- `OOMKilled` — превышен memory limit.

### Не работает сеть
```bash
kubectl exec -it POD -- curl backend-service:80   # изнутри
kubectl get svc                                    # существует ли?
kubectl get endpoints SVC                          # есть ли поды за сервисом?
```

### Дебаг с ephemeral-контейнером
```bash
kubectl debug -it POD --image=busybox --target=CONTAINER
```

### Логи нескольких подов
```bash
kubectl logs -l app=myapp --tail=20
stern myapp.*           # через утилиту stern (tail -f для всех подов)
kubectl logs -f -l app=myapp --max-log-requests=10
```

### Полезные команды диагностики
```bash
kubectl get componentstatuses
kubectl get events --sort-by='.lastTimestamp'
kubectl describe node NODE_NAME
kubectl get pods -A -o wide | grep -v Running
```

---

## 🪤 Частые ошибки

1. **`imagePullPolicy: Always` для локального образа** — K8s не найдёт.
   Для minikube: `imagePullPolicy: Never` + `minikube image load`.
2. **Забыли `selector`** — Service не найдёт Pod'ы.
3. **Labels не совпадают** — Service/Deployment не подключится.
4. **Resource limits** — `requests` нужен для планирования.
5. **`latest` tag** — K8s не обновит без явного перезапуска.
6. **Secret в открытом виде** — base64 ≠ шифрование.
7. **Namespace по умолчанию** — забываете `-n`, всё в default.
8. **`kubectl apply` после `kubectl create`** — конфликт аннотаций.
9. **`replicas: 0`** — случайно масштабировали до нуля.
10. **PV не удаляется** — `reclaimPolicy: Retain` держит диск.

---

## 🔗 Полезные ссылки

- K8s документация: https://kubernetes.io/docs/home
- Minikube: https://minikube.sigs.k8s.io/docs
- kubectl Cheat Sheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet
- K8s Patterns: https://www.redhat.com/en/resources/oreilly-kubernetes-patterns-cloud-native-apps
- Awesome Kubernetes: https://github.com/ramitsurana/awesome-kubernetes
- Helm: https://helm.sh
- Lens (GUI): https://k8slens.dev
- k9s (TUI): https://github.com/derailed/k9s

---

## 💡 Полезные советы

1. **`kubectl get all`** — обзор ресурсов в namespace.
2. **`-o wide`** — больше информации (IP, нода).
3. **`-w` (watch)** — следить в реальном времени.
4. **`kubectl describe`** — лучший способ дебага (события внизу).
5. **`kubectl apply -f`** — declarative (лучше, чем `create`).
6. **`kubectl exec -it`** — войти в под (как `docker exec`).
7. **`kubectl port-forward`** — доступ к сервису локально.
8. **Minikube `image load`** — для локальных образов (без registry).
9. **Helm** — для сложных приложений (база данных, сертификаты).
10. **`k9s`** — TUI для управления (как htop для K8s).
11. **`stern`** — tail логов нескольких подов сразу.
12. **Kustomize** — для разных сред (dev/prod) без templating.
13. **`kubectl explain pod.spec.containers`** — справка по полям.
14. **Resource quotas** — лимиты на namespace.
15. **Labels everywhere** — основа для связей и выборок.

---

*Сгенерировано как шпаргалка. Kubernetes огромен —
углубляйтесь через https://kubernetes.io/docs/ и kubectl cheat sheet*
