# BTG Pactual - Backend

Este proyecto es el backend del sistema de gestión de inversiones de BTG Pactual. Está construido con FastAPI y utiliza MongoDB como base de datos. A continuación, se presentan las instrucciones para correr el código localmente y desplegarlo en AWS.

## Tabla de Contenidos

- [Instalación Local](#instalación-local)
- [Despliegue en AWS](#despliegue-en-aws)
  - [Configuración de ECR](#configuración-de-ecr)
  - [Configurar AWS CodePipeline, S3, CloudFormation e IAM](#configuración-de-aws)

## Instalación Local

- Python 3.9+
- Docker (opcional para despliegue en AWS)
- AWS CLI configurado

## Correr el Código Localmente

### 1. Crear un Entorno Virtual

```sh
python -m venv .venv
source .venv/bin/activate  # En Windows usa `.venv\Scripts\activate`
```

### 2. Instalar Dependencias

```sh
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto

### 4. Ejecutar la Aplicación

```sh
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

## Despliegue en AWS

### Configuración de ECR

```sh
aws ecr create-repository --repository-name <name> --region <region>
```

### Configurar AWS CodePipeline, S3, CloudFormation e IAM

#### **Crear Roles y Políticas en IAM**

1. Crear un rol para CodePipeline con las siguientes políticas:

- AWSCodePipelineFullAccess
- AmazonS3FullAccess
- CloudFormationFullAccess
- AmazonEC2ContainerRegistryFullAccess

2. Crear un rol para CodeBuild con las siguientes políticas:

- AWSCodeBuildAdminAccess
- AmazonS3FullAccess
- AmazonEC2ContainerRegistryFullAccess

#### **Crear un Bucket en S3**

```sh
aws s3 mb s3://<name> --region <region>
```
