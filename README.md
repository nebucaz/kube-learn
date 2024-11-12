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

### Run a local repository 
```bash
minikube addons enable registry 
```
> Note: Minikube will generate a port and request you use that port when enabling registry. That instruction is not related to this guide.

When enabled, the registry addon exposes its port 5000 on the minikube’s virtual machine.
In order to make docker accept pushing images to this registry, we have to redirect port 5000 on the docker virtual machine over to port 5000 on the minikube machine. We can (ab)use docker’s network configuration to instantiate a container on the docker’s host, and run socat there:

```bash
docker run --rm -it --network=host alpine ash -c "apk add socat && socat TCP-LISTEN:5000,reuseaddr,fork TCP:$(minikube ip):5000"
```
Once socat is running it’s possible to push images to the minikube registry:
```bash
docker tag my/image localhost:5000/myimage
docker push localhost:5000/myimage
```
After the image is pushed, refer to it by `localhost:5000/{name}` in kubectl specs.

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