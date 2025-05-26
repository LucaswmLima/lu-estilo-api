# Lu Estilo API

API RESTful construída com FastAPI para gerenciar clientes, produtos, pedidos e autenticação via JWT. Inclui integração com WhatsApp (sandbox Twilio).

---

## Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/lu-estilo-api.git
cd lu-estilo-api
```

### 2. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e preencha com suas credenciais:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=lu_estilo
POSTGRES_HOST=db
POSTGRES_PORT=5432
SENTRY_DSN=<seu_sentry_dns>
JWT_SECRET=seu_segredo_aqui
TWILIO_ACCOUNT_SID=seu_sid_twilio
TWILIO_AUTH_TOKEN=seu_token_twilio
TWILIO_WHATSAPP_SANDBOX_NUMBER=+14155238886
```

### 3. Suba os containers com Docker Compose

```bash
docker-compose up --build
```

A API estará disponível em `http://localhost:8000`.

---

## Funcionalidades principais

- Autenticação (registro, login, refresh token, logout)
- Gerenciamento de clientes (CRUD)
- Gerenciamento de produtos (CRUD)
- Gerenciamento de pedidos (CRUD)
- Integração com WhatsApp via API sandbox Twilio
- Controle de acesso por níveis (usuário comum e administrador)
- Comando para alternar status de administrador de um usuário (toggle admin)

---

## Endpoints principais

### Auth

| Método | Rota             | Descrição                  | Acesso        |
|--------|------------------|----------------------------|---------------|
| POST   | `/auth/register` | Registrar novo usuário     | Público       |
| POST   | `/auth/login`    | Login e obtenção de token  | Público       |
| POST   | `/auth/refresh`  | Refresh token              | Token válido  |
| POST   | `/auth/logout`   | Logout                     | Token válido  |

---

### Clientes

| Método | Rota            | Descrição                 | Acesso           |
|--------|-----------------|---------------------------|------------------|
| GET    | `/clients`      | Listar clientes           | Usuário/Admin    |
| POST   | `/clients`      | Criar cliente             | Usuário/Admin    |
| GET    | `/clients/{id}` | Detalhes cliente          | Usuário/Admin    |
| PUT    | `/clients/{id}` | Atualizar cliente         | Usuário/Admin    |
| DELETE | `/clients/{id}` | Deletar cliente           | Admin somente    |

---

### Produtos

| Método | Rota             | Descrição                 | Acesso           |
|--------|------------------|---------------------------|------------------|
| GET    | `/products`      | Listar produtos           | Usuário/Admin    |
| POST   | `/products`      | Criar produto             | Admin somente    |
| GET    | `/products/{id}` | Detalhes produto          | Usuário/Admin    |
| PUT    | `/products/{id}` | Atualizar produto         | Admin somente    |
| DELETE | `/products/{id}` | Deletar produto           | Admin somente    |

---

### Pedidos

| Método | Rota            | Descrição                  | Acesso           |
|--------|-----------------|----------------------------|------------------|
| GET    | `/orders`       | Listar pedidos             | Usuário/Admin    |
| POST   | `/orders`       | Criar pedido               | Usuário/Admin    |
| GET    | `/orders/{id}`  | Detalhes do pedido         | Usuário/Admin    |
| PUT    | `/orders/{id}`  | Atualizar pedido           | Usuário/Admin    |
| DELETE | `/orders/{id}`  | Deletar pedido             | Admin somente    |

---

## Integração WhatsApp - Sandbox Twilio

Para testar a integração com o WhatsApp no ambiente sandbox do Twilio:

- Use o link para entrar no sandbox:

```
https://api.whatsapp.com/send/?phone=%2B14155238886&text=join+circle-continent&type=phone_number&app_absent=0
```

- Após entrar, você poderá receber mensagens da API em seu WhatsApp.

---

## Integração com Sentry – Monitoramento de Erros

Para monitorar erros automaticamente com o Sentry:

- Defina a variável `SENTRY_DSN` no arquivo `.env` com sua chave DSN.
- A integração é feita automaticamente ao iniciar a aplicação.
- Erros não tratados (como exceções) são enviados para o painel do Sentry.

## Alternar status de administrador

Durante os testes, é permitido definir se um usuário é administrador (`is_admin`) diretamente na chamada de registro (`POST /register`), usando `is_admin: 1` para admin e `is_admin: 0` (ou omitido) para um usuário comum.

> ⚠️ Em produção, essa prática **não deve ser mantida** por questões de segurança. O campo `is_admin` deve ser controlado exclusivamente por usuários autorizados.

Caso queira alterar o status de administrador de um usuário **já criado**, você pode:

### ✅ Opção 1: Usar o script `toggle_admin.py`

1. Liste os containers Docker em execução:

```bash
docker ps
```

2. Localize o nome do container que está rodando a aplicação (coluna **NAMES**).

3. Acesse o terminal do container:

```bash
docker exec -it NOME_DO_CONTAINER bash
```

4. Dentro do container, execute o script com o e-mail do usuário:

```bash
python app/utils/toggle_admin.py usuario@example.com
```

Esse comando irá alternar o campo `is_admin`: se o usuário for admin, vira comum; se for comum, vira admin.

## Observações

- As rotas que precisam de autenticação exigem o token JWT no header `Authorization: Bearer <token>`.
- Usuários comuns podem ver e modificar seus próprios clientes e pedidos.
- Somente administradores podem criar/deletar produtos e deletar clientes e pedidos.
- O banco de dados roda dentro do container Postgres, mapeado para a porta 5432 no host.
- Use PgAdmin ou outro cliente para acessar o banco via `localhost` na porta `5433` com usuário e senha do `.env`.

---