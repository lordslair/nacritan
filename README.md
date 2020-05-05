# nacridan-retriever-backend, the project :

This project is a backend for a Tactical Interface (IT) in the game Nacridan.  
Its purpose is to parse data received from JS user scripts.  
It's done by a Python backend to query a SQLite DB.  
And a Python-Flask API, to return JSON if requested.  

All of this inside Docker containers for portable purposes.  
These containers are powered up by Kubernetes.  

Actually, it works this way :

 - (nacritan-backend-nginx)      runs the proxy to serve the URLs, and SSL certs
 - (nacritan-backend-api)        runs the Flask app
 - (nacritan-backend-sqlite-web) runs the SQLite WebUI
 - (nacritan-backend-redis)      runs the Redis server

### Which script does what ?

```
.
├── k8s                               |  
│   ├── deployment-*.yaml             |  Pods deployment files
│   ├── service-*.yaml                |  Services deployment files
│   └── volume-*.yaml                 |  Volumes deployment files
└── python                            |  
    ├── data
    │   └── initDB.SQL                |  Init SQL script for the DB
    ├── tests
    │   ├── test_00_vars.py           |  Tests for token presence
    │   ├── test_01_auth.py           |  Tests for token auth by routes
    │   ├── test_02_data.py           |  Tests for data returned by routes
    │   └── test_03_redis.py          |  Tests for redis
    ├── app.py                        |  Flask main app
    ├── functions.py                  |  library to handle common f()
    ├── variables.py                  |  library to handle global variables
    └── queries.py                    |  library to handle SQL layer
```

### Tech

I used mainy :

* Python v3
* SQLite v3
* nginx
* redis
* [docker/docker-ce][docker] to make it easy to maintain
* [kubernetes/kubernetes][kubernetes] to make everything smooth
* [Alpine][alpine] - probably the best/lighter base container to work with
* [pallets/flask][flask] - Python micro framework for building API
* [pytest-dev/pytest][pytest] - Python test framework

And of course GitHub to store all these shenanigans.

### Schematics

```
      +-----------------------------------------------+
      |                  LoadBalancer                 |
      +-----------------------+-----------------------+
                              |
                     +--------v--------+
        +----------->+      nginx      +<-----------+
        |            +-----------------+            |
        |                                           |
+-------v-------+                           +-------v-------+
|  Flask:5000   |                           |  Flask:5001   |
| (main app.py) |                           |  (sqlite-web) |
+-------+-------+                           +-------+-------+
        |            +-----------------+            |
        +----------->+      SQLite     +<-----------+
        |            +-----------------+
        |
        |            +-----------------+
        +----------->+      Redis      |
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
- The 3 pods : nginx, api, sqlite-web, redis

```
$ kubectl get pods
NAME                                          READY   STATUS    RESTARTS   AGE
nacritan-backend-api-65b887758f-259gd         1/1     Running   0          17m
nacritan-backend-nginx-8f5cf6c7d-twjzw        2/2     Running   0          5h
nacritan-backend-sqlite-web-6f5567f64f-bk8mk  1/1     Running   0          8m42s
nacritan-backend-redis-6f5bdccf84-dw9tm       1/1     Running   0          2d15h
```

- The 4 volumes : api, sqlite-db, certbot-certs, certbot-www

```
$ kubectl get pvc
NAME                            STATUS  VOLUME                   CAPACITY  [...]
nacritan-backend-code-api       Bound   pvc-[...]-da539ff1fafe   1Gi       [...]
nacritan-sqlite-db              Bound   pvc-[...]-418ac586b236   1Gi       [...]
nacritan-backend-certbot-certs  Bound   pvc-[...]-5312025190d9   1Gi       [...]
nacritan-backend-certbot-www    Bound   pvc-[...]-d6ab9d74cf8b   1Gi       [...]
```

- The 5 services : nginx, api, sqlite-web, redis & loadbalancer

```
$ kubectl get services
NAME                         TYPE           CLUSTER-IP     EXTERNAL-IP  PORT(S)
nacritan-lb                  LoadBalancer   10.3.40.58     [...]        80:30985/TCP,8080:30619/TCP
nacritan-backend-api         ClusterIP      10.3.138.0     <none>       5000/TCP
nacritan-backend-nginx       ClusterIP      10.3.202.163   <none>       80/TCP,443/TCP
nacritan-backend-sqlite-web  ClusterIP      10.3.89.229    <none>       5001/TCP
nacritan-backend-redis-svc   ClusterIP      10.3.179.197   <none>       6379/TCP
```

#### Disclaimer/Reminder

>The project is not mono-container, but could. Minimal setup would be one pod (Flask app) + one volume with code+db.  
>The SQLite DB engine should be upgraded to MariaDB/whatever to handle big workloads.  
>A Redis server caches /tiles and /minimap JSON as they need up to 6sec of compute time to generate
>Flask pod needs to be scaled up to handle more load (and maybe MariaDB clusterized at some point).  

### Todos

 - Add a container for backups
 - Add a container for Discord integration

---
   [kubernetes]: <https://github.com/kubernetes/kubernetes>
   [docker]: <https://github.com/docker/docker-ce>
   [alpine]: <https://github.com/alpinelinux>
   [flask]: <https://github.com/pallets/flask>
   [pytst]: <https://github.com/pytest-dev/pytest>
