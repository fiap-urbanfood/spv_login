# 💻 Projeto spv_login

Sistema de Processamento de Vídeo (Microserviço de Login)

# ###########################################################
# 💻 Arquitetura do Serviço

![ARQUITETURA](FIAP-URBAN-FOOD-FASE5.png)

# ###########################################################
# 💻 VIDEO DE APRESENTAÇÃO DO PROJETO

https://www.youtube.com/watch?v=jbnfhMVp4zo&t=6s

# ###########################################################
# 💻 Deploy via Github Actions

### Executando o CI/CD

Etapas do Pipeline via github actions:

1.1 Pull Request com sonar code quality e GitGuardian Security:
![CI/CD - PULLREQUEST](devops/CICD/CICD-SPV_LOGIN-PULLREQUEST.png)

1.2 Sonar para análise e monitoramento contínuo da qualidade do código.
![CI/CD - SONAR](devops/CICD/CICD-SPV_LOGIN-SONAR.png)

1.3 Build da Aplicação:
![CI/CD - BUILD](devops/CICD/CICD-SPV_LOGIN-BUILD.png)

1.4 Push da Imagem para o ECR.
![CI/CD - ECR](devops/CICD/CICD-SPV_LOGIN-ECR.png)

1.5 Deploy no EKS.
![CI/CD - EKS](devops/CICD/CICD-SPV_LOGIN-EKS.png)

# ###########################################################
# 💻 Deploy via DockerFile

### 1. Preparar o ambiente para gerar o pacote

1.1 Script do MySQL..
``` bash
criar_tabelas.py
```

1.2 Exemplo de como criar as Variáveis de Ambiente..
``` bash
export API_IMAGE_TAG='1.0.0'
export AWS_REGION='us-east-1'
export AWS_ACCOUNT='857378965163'
```

1.3 Docker Build na raiz do projeto..
``` bash
docker build --no-cache --progress=plain -f devops/Dockerfile -t app-login:$API_IMAGE_TAG .
docker tag app-login:$API_IMAGE_TAG $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/spv/login:$API_IMAGE_TAG
docker tag $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/spv/login:$API_IMAGE_TAG $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/spv/login:latest
```

1.4 Docker Login ECR..
``` bash
aws ecr get-login-password --region $AWS_REGION  --profile terraform-iac | docker login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com
```

1.5 Docker Push do APP..
``` bash
docker push $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/spv/login:$API_IMAGE_TAG
docker push $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/spv/login:latest
```

1.6 Rodando o container local..
``` bash
docker run -dit -p 8000:8000 --name=app-login app-login:$API_IMAGE_TAG
```

1.7 Acesso a API..
``` bash
http://localhost:8000/health
```

# ###########################################################
# 💻 Deploy no EKS

## Processo Automatizado via Github Actions

## Configuração do kubectl

2.1 Configurar o acesso ao cluster
``` bash
aws eks update-kubeconfig --region us-east-1 --name k8s-urbanfood --profile terraform-iac
```

2.2 Entramos no diretório do k8s para subir o ambiente.
``` bash
cd k8s/
kubectl apply -f aws-auth.yml
kubectl apply -f namespace.yml
```

2.3 Acessando o namespace, "Após já ter sido criado"
``` bash
kubectl config set-context --current --namespace=video-system
```

Após criar e configurar a infra executamos o github actions do projeto. 

Para documentar: 

2.4 Para subir a aplicação de forma manual:
``` bash
kubectl apply -f app/login-configmap.yaml
kubectl apply -f app/login-service.yaml
kubectl apply -f app/login-hpa.yaml
kubectl apply -f app/login-deployment.yaml
```
