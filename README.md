# kube-learn
Learning Kubernetes

## Links
- [Tutorial](https://kubernetes.io/docs/tutorials/)
- [Docs](https://kubernetes.io/docs/)

## Create deployment
```bash
kubectl apply -f example-backend-deployment.yaml
```

### Get Pods
```bash
kubectl get pods
```

### Get Logs <pod>
```bash
kubectl logs <pod-name> 
```

### Get Logs of container within pod
```bash
kubectl logs <pod-name> -c <container-name>
```

### Get replica Sets
```bash
kubectl get rs
```

### Get Services
```bash
kubectl get services
```

### Get Deployments
```bash
kubectl get deployments
```

### Get Service
Create a proxy to access the service ports
```bash
minikube service example-backend-service --url
```

## Rolling Update

### Create a new image
```bash
docker build -t localhost:5000/kubelearn:1.1 .
```
Update the server image (new endpoint to get status of the task). Problem: If replica set > 1 example-backend-service loadbalancer may connect to the wrong replica set and the task will not be found
- Do not forget to push image after building: `docker push localhost:5000/kubelearn:1.1'
```bash
kubectl set image deployments/example-backend server=localhost:5000/kubelearn:1.1
```

### Rollback
```bash
kubectl rollout undo deployments/example-backend 
```