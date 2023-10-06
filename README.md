# nacrITan, the project :

This project is a backend for a Tactical Interface (IT) in the game Nacridan.  
Its purpose is to parse data received from JS user scripts.  
It's done by a Python backend (Flask API) querying a (remote) MySQL DB.  

All of this inside Docker containers for portable purposes.  
These containers are powered up by Kubernetes.  

Actually, it works this way :

 - (nacritan-backend-nginx)      runs the proxy to serve the URLs, and SSL certs
 - (nacritan-backend-api)        runs the Flask app
 - (nacritan-backend-backup)     runs the DB rotating backups 24h/30d/52w/12m

### Which script does what ?

```
.
├── k8s                               |  
│   ├── deployment-*.yaml             |  Pods deployment files
│   └── service-*.yaml                |  Services deployment files
└── code                            |  
    ├── tests
    │   ├── test_00_vars.py           |  Tests for token presence
    │   ├── test_01_auth.py           |  Tests for token auth by routes
    │   └── test_02_data.py           |  Tests for data returned by routes
    └── app.py                        |  Flask main app
```

### Tech

I used mainy :

* Python v3
* nginx
* [docker/docker-ce][docker] to make it easy to maintain
* [kubernetes/kubernetes][kubernetes] to make everything smooth
* [Alpine][alpine] - probably the best/lighter base container to work with
* [pallets/flask][flask] - Python micro framework for building API
* [pytest-dev/pytest][pytest] - Python test framework

And of course GitHub to store all these shenanigans.

### Schematics

```
     +-----------------------------------------------+
     |                  LoadBalancer:443             |
     +-----------------------+-----------------------+
                             |
                    +--------v--------+
                    |    nginx:443    |
                    +--------+--------+
                             |
                    +--------v--------+
                    |    Flask:5000   |
                    |  (main app.py)  |
                    +-----------------+
```

### Installation

The core and its dependencies are meant to run in a Docker/k8s environment.  
Could work without it, but more practical to maintain this way.  

Every part is kept in a different k8s file separately for more details.  

```
$ git clone https://github.com/lordslair/nacridan-retriever-backend
$ cd nacridan-retriever-backend/k8s
$ kubectl apply -f *
```

This will create :
- The 2 pods : nginx, api (+ backup if needed)

```
$ kubectl get pods
NAME                                          READY   STATUS    RESTARTS   AGE
nacritan-backend-api-65b887758f-259gd         1/1     Running   0          17m
nacritan-backend-nginx-8f5cf6c7d-twjzw        2/2     Running   0          5h
```

- The 2 volumes : certbot-certs, certbot-www

```
$ kubectl get pvc
NAME                            STATUS  VOLUME                   CAPACITY  [...]
nacritan-backend-certbot-certs  Bound   pvc-[...]-5312025190d9   1Gi       [...]
nacritan-backend-certbot-www    Bound   pvc-[...]-d6ab9d74cf8b   1Gi       [...]
```

- The 3 services : nginx, api & loadbalancer

```
$ kubectl get services
NAME                         TYPE           CLUSTER-IP     EXTERNAL-IP  PORT(S)
nacritan-lb                  LoadBalancer   10.3.40.58     [...]        80:30985/TCP,8080:30619/TCP
nacritan-backend-api         ClusterIP      10.3.138.0     <none>       5000/TCP
nacritan-backend-nginx       ClusterIP      10.3.202.163   <none>       80/TCP,443/TCP
```

#### Disclaimer/Reminder

>The project is not mono-container, but could. Minimal setup would be one pod (Flask app without nginx).  

### Todos

 - Add a container for Discord integration

---
   [kubernetes]: <https://github.com/kubernetes/kubernetes>
   [docker]: <https://github.com/docker/docker-ce>
   [alpine]: <https://github.com/alpinelinux>
   [flask]: <https://github.com/pallets/flask>
   [pytst]: <https://github.com/pytest-dev/pytest>
