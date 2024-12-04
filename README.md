# pdris_lab5
Laboratory work on K8s

Для начала скачаем minikube и запустим его

Напишем манифесты для minikube, чтобы развернуть наше приложение

Далее развернем приложение и бд

```bash
kubectl apply -f flask-app-deployment.yml
kubectl apply -f postgres-deployment.yml
kubectl apply -f postgres-pvc.yml
```

Далее откроем соединение с нашим LoadBalancer сервисом
```bash
minikube tunnel
```

Во втором терминале получим URL-адрес для подключения к нашему сервису
```bash
minikube service flask-app-service
```

Success!!:)