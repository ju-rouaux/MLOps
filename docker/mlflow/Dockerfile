FROM ghcr.io/mlflow/mlflow:latest

EXPOSE 8080

CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "8080", "--backend-store-uri", "/mlflow/backend", "--default-artifact-root", "/mlflow/artifacts"]