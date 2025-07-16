# Go Gin API – Implantação com Kubernetes e Helm

Este projeto tem como objetivo aplicar os conceitos de orquestração de contêineres utilizando **Kubernetes** com **Minikube**, a partir de uma aplicação previamente conteinerizada com Docker Compose.

A aplicação é uma **API simples em Go (Gin)** para cadastro e listagem de usuários, com suporte a balanceamento de carga, descoberta de serviços e interface gráfica via navegador.

## Autores

- Carolina Martins Emilio – 811508  
- Ivan Capeli Navas – 802286

---

## 💡 Ideia

- Aplicação minimalista, centrada no cadastro de usuários.
- Cada usuário possui apenas um nome e um ID.
- O frontend envia apenas o nome para cadastro.
- O balanceador de carga opera com dois algoritmos:  
  - `roundrobin` (padrão): acessa os serviços em ordem sequencial A → B → C → A...  
  - `random`: escolhe uma instância aleatoriamente.

---

## 🧱 Arquitetura Kubernetes

A aplicação foi adaptada para rodar em **Minikube**, utilizando os seguintes recursos Kubernetes:

| Tipo        | Descrição                                                      |
|-------------|----------------------------------------------------------------|
| Deployment  | Define os Pods e réplicas para frontend, load balancer, etc.   |
| StatefulSet | Usado para o backend (`go-gin-api`) com descoberta estável.    |
| Service     | Comunicação entre os componentes (alguns headless).            |
| Ingress     | Expõe o frontend publicamente via `http://k8s.local`.          |
| ConfigMap   | Armazena variáveis de ambiente não sensíveis.                  |


---

## 🌐 Acesso via Ingress

O controlador de entrada (Ingress Controller) expõe as portas `80` e `443` e roteia todas as requisições ao frontend:

```text
http://k8s.local
```

---

## 🚀 Helm Chart

A implantação foi automatizada com **Helm**, utilizando uma estrutura multigráfico:

```
go-chart/
├── charts/
│   ├── api/
│   ├── front/
│   └── lb/
├── Chart.yaml
└── values.yaml
```

Cada gráfico Helm é independente por componente, facilitando reutilização e versionamento.

### Estratégias Adotadas

- Uso de `values.yaml` global compartilhado.
- Templates Helm para Deployment, Services e variáveis de ambiente.
- `StatefulSet` e `headless service` para descoberta estável no backend.
- Balanceador com variável `SERVICE_REGISTRY_URL` dinâmica.
- Mapeamento consistente de portas entre serviços.

---

## 📦 Containers e Serviços

### 🖥️ frontend
- Interface gráfica feita em Python (NiceGUI).
- Porta exposta: `5000` (via Service mapeada para `80`).
- Variáveis:  
  `API_URL=http://load-balancer:8080`

### ⚙️ go-gin-api (backend)
- Framework: Go (Gin).
- Executado como `StatefulSet` com 3 réplicas.
- Usa serviço `headless` para descoberta.
- Acesso ao banco via env:
  ```yaml
  DB_HOST: postgres
  DB_PORT: 5432
  DB_USER: postgres
  DB_PASSWORD: pass
  DB_NAME: mydb
  ```

### 🔍 service-discovery
- Serviço de descoberta onde as instâncias da API se registram.
- Comunicação via `POST /register` e `GET /services`.

### ⚖️ load-balancer
- Recebe requisições do frontend e encaminha para o backend.
- Balanceamento `roundrobin` ou `random`.
- Usa:
  ```yaml
  SERVICE_REGISTRY_URL=http://service-discovery:3000/services
  ```

### 🛢️ db (PostgreSQL)
- Armazena dados persistentes.
- Inicialização com `initdb.sql`.
- Monitorado com `healthcheck`.

---


## 📌 Conclusão

O projeto Go Gin API demonstra de forma prática a implantação de microsserviços com Kubernetes, utilizando boas práticas como descoberta de serviços, balanceamento de carga e uso de Ingress para exposição segura. A abordagem modular e automatizada facilita escalabilidade, manutenção e portabilidade para ambientes reais de produção.
