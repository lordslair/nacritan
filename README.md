# nacrITan, the project :

This project is a backend for a Tactical Interface (IT) in the game Nacridan.  
Its purpose is to parse data received from JS user scripts.  
It's done by a Python backend (Flask API) querying a MongoDB.  

All of this inside Docker containers for portable purposes.  
These containers are powered up by Kubernetes.  

Actually, it works this way :

 - (nacritan-nginx)      runs the proxy to serve the URLs, and SSL certs
 - (nacritan-api)        runs the Flask app

 Optionnal:
 - (nacritan-backup)     runs the DB rotating backups 24h/30d/52w/12m

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

* [docker/docker-ce][docker] to make it easy to maintain
* [kubernetes/kubernetes][kubernetes] to make everything smooth
* [Alpine][alpine] - probably the best/lighter base container to work with
* [pallets/flask][flask] - Python micro framework for building API
* [pytest-dev/pytest][pytest] - Python test framework

And of course GitHub to store all these shenanigans.

### Schematics

```
     +-----------------------------------------------+
     |                  NodePort:30443               |
     +-----------------------+-----------------------+
                             |
                    +--------v--------+
                    |    nginx:443    |
                    +--------+--------+
                             |
                    +--------v--------+
                    |    Flask:5000   |
                    |     (app.py)    |
                    +--------+--------+
                             |
                    +--------v--------+
                    |  Ext.  MongoDB  |
                    +-----------------+
```

### Installation

The core and its dependencies are meant to run in a Docker/k8s environment.  
Could work without it, but more practical to maintain this way.  

Every part is kept in a different k8s file separately for more details.  

```
$ git clone https://github.com/lordslair/nacritan
$ cd nacritan/k8s
$ kubectl apply -f *
```

This will create :
- The pods : nginx, api (+ backup if needed)

```
$ kubectl get pods
NAME                       READY   STATUS    RESTARTS       AGE
api-769b969d98-rgmk4       1/1     Running   0              95d
backup-cdddf5787-5742g     1/1     Running   0              95d
nginx-5cc68db8d7-rchxb     2/2     Running   0              33m
```

- The 2 volumes : certbot-certs, certbot-www

```
$ kubectl get pvc
NAME               STATUS  VOLUME                   CAPACITY  [...]
certbot-certs-pvc  Bound   pvc-[...]-5312025190d9   1Gi       [...]
certbot-www-pvc    Bound   pvc-[...]-d6ab9d74cf8b   1Gi       [...]
```

- The 3 services : nginx, api

```
$ kubectl get services
NAME          TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
api-svc       ClusterIP   10.3.223.39    <none>        5000/TCP                     155d
nginx-svc     NodePort    10.3.140.182   <none>        80:30080/TCP,443:30443/TCP   31m
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
   [pytest]: <https://github.com/pytest-dev/pytest>
