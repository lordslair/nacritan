# nacridan-retriever-backend, the project :

This project is mainly a backend for a Tactical Interface (IT) for the game Nacridan.  
Its purpose is to parse data received from JS user scripts.  
It's done by a Python backend to query a SQLite DB.  
And a Python-Flask API, to return JSON if requested.  

All of this inside Docker containers for portable purposes.  
These containers are powered up by Kubernetes.  

Actually, it works this way :

 - (nacritan-python)     runs the Flask app
 - (nacritan-sqlite-web) runs the SQLite WebUI

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
    │   └── test_02_data.py           |  Tests for data returned by routes
    ├── app.py                        |  Flask main app
    ├── functions.py                  |  library to handle common f()
    ├── variables.py                  |  library to handle global variables
    └── queries.py                    |  library to handle SQL layer
```

### Tech

I used mainy :

* Python v3
* SQLite v3
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
      +-+-------------------------------------------+-+
        |                                           |
+-------v-------+                           +-------v-------+
|  Flask:5000   |                           |  Flask:5001   |
| (main app.py) |                           |  (sqlite-web) |
+-------+-------+                           +-------+-------+
        |            +-----------------+            |
        +----------->+      SQLite     +<-----------+
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
- The 2 pods : python, sqlite-web

```
$ kubectl get pods
NAME                                     READY   STATUS    RESTARTS   AGE
nacritan-python-767d8cd58d-qnrxx         1/1     Running   0          22h
nacritan-sqlite-web-58d569d6c5-ncpch     1/1     Running   0          21h
```

- The 2 volumes : code-python, sqlite-db

```
$ kubectl get pvc
NAME                     STATUS   VOLUME                   CAPACITY   [...]
nacritan-code-python     Bound    pvc-[...]-da539ff1fafe   1Gi        [...]
nacritan-sqlite-db       Bound    pvc-[...]-418ac586b236   1Gi        [...]
```

- The 3 services : python, sqlite-web & loadbalancer

```
$ kubectl get services
NAME                         TYPE           CLUSTER-IP     EXTERNAL-IP  PORT(S)     
nacritan-lb                  LoadBalancer   10.3.40.58     [...]        80:30985/TCP,8080:30619/TCP
nacritan-python              ClusterIP      10.3.51.95     <none>       5000/TCP    
nacritan-sqlite-web          ClusterIP      10.3.98.218    <none>       5001/TCP         
```

#### Disclaimer/Reminder

>The project is not mono-container, but could. Minimal setup would be one pod (Flask app) + one volume with code+db.  
>The SQLite DB engine should be upgraded to MariaDB/whatever to handle big workloads.  
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
