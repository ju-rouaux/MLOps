## Installation
1. ``cd`` on this directory
```
cd docker/mlflow/
```
2. Create image
```
docker build -t mlops-mlflow:latest .
```
3. Create Volume and change ``<LOCATION>`` to your preferred storage location
```
docker volume create --driver local --opt type=none --opt device=<LOCATION> --opt o=bind mlflow_volume
```
4. Run container
```
docker run -d -p 8015:8080 --mount type=volume,src=mlflow_volume,dst=/mlflow mlops-mlflow
```
5. Open in a browser
```
http://localhost:8015
```
