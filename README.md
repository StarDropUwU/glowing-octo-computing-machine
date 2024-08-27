
# Documentação do Aplicativo Flask

## Visão Geral

Este aplicativo é uma API RESTful desenvolvida com Flask para gerenciar operações financeiras e registrar o histórico de transações. Ele oferece funcionalidades de CRUD (Criar, Ler, Atualizar e Deletar) para operações financeiras, bem como a capacidade de processar operações em lote. A API é protegida por autenticação JWT.

### Funcionalidades

1. **Gerenciamento de Operações Financeiras**
   - Criar operações financeiras.
   - Obter uma lista de operações financeiras com filtros e paginação.
   - Obter, atualizar e deletar uma operação financeira específica.
   - Processar operações financeiras em lote.

2. **Histórico de Transações**
   - Registro de mudanças para operações financeiras.

### Autenticação

Todos os endpoints são protegidos por autenticação JWT. O decorator `@token_required` deve ser aplicado para garantir que o usuário esteja autenticado.

## Endpoints

### 1. **Health Check**

- **URL:** `/health`
- **Método:** `GET`
- **Descrição:** Verifica se o servidor está funcionando.
- **Autenticação:** Requer token JWT.
- **Resposta de Sucesso:**
  ```html
  <h1>Surprise, it Works!<h1>
  ```

### 2. **Criar Operação**

- **URL:** `/operations`
- **Método:** `POST`
- **Descrição:** Cria uma nova operação financeira.
- **Autenticação:** Requer token JWT.
- **Corpo da Requisição:**
  ```json
  {
    "tipo_operacao": "tipo",
    "valor": 100.00,
    "descricao": "Descrição da operação",
    "data": "2024-08-27T00:00:00"
  }
  ```
- **Resposta de Sucesso:**
  ```json
  {
    "id": 1,
    "tipo_operacao": "tipo",
    "valor": 100.00,
    "data": "2024-08-27T00:00:00",
    "descricao": "Descrição da operação"
  }
  ```
- **Resposta de Erro:**
  ```json
  {
    "error": "Invalid data"
  }
  ```

### 3. **Obter Operações**

- **URL:** `/operations`
- **Método:** `GET`
- **Descrição:** Obtém uma lista de operações financeiras com filtros e paginação.
- **Autenticação:** Requer token JWT.
- **Parâmetros de Consulta:**
  - `page`: Número da página (padrão: 1).
  - `per_page`: Número de itens por página (padrão: 10).
- **Corpo da Requisição:**
  ```json
  {
    "tipo_operacao": "tipo",
    "valor": 100.00,
    "descricao": "Descrição da operação",
    "data": "2024-08-27T00:00:00"
  }
  ```
- **Resposta de Sucesso:**
  ```json
  [
    {
      "id": 1,
      "tipo_operacao": "tipo",
      "valor": 100.00,
      "data": "2024-08-27T00:00:00",
      "descricao": "Descrição da operação"
    }
  ]
  ```

### 4. **Obter Operação por ID**

- **URL:** `/operations/<int:id>`
- **Método:** `GET`
- **Descrição:** Obtém uma operação financeira específica pelo ID.
- **Autenticação:** Requer token JWT.
- **Resposta de Sucesso:**
  ```json
  {
    "id": 1,
    "tipo_operacao": "tipo",
    "valor": 100.00,
    "data": "2024-08-27T00:00:00",
    "descricao": "Descrição da operação"
  }
  ```
- **Resposta de Erro:**
  ```json
  {
    "error": "Nenhuma operacao encontrada"
  }
  ```

### 5. **Atualizar Operação**

- **URL:** `/operations/<int:id>`
- **Método:** `PUT`
- **Descrição:** Atualiza uma operação financeira existente.
- **Autenticação:** Requer token JWT.
- **Corpo da Requisição:**
  ```json
  {
    "tipo_operacao": "novo tipo",
    "valor": 200.00,
    "descricao": "Nova descrição",
    "data": "2024-08-28T00:00:00"
  }
  ```
- **Resposta de Sucesso:**
  ```json
  {
    "id": 1,
    "tipo_operacao": "novo tipo",
    "valor": 200.00,
    "data": "2024-08-28T00:00:00",
    "descricao": "Nova descrição"
  }
  ```
- **Resposta de Erro:**
  ```json
  {
    "error": "Invalid data"
  }
  ```

### 6. **Deletar Operação**

- **URL:** `/operations/<int:id>`
- **Método:** `DELETE`
- **Descrição:** Deleta uma operação financeira existente.
- **Autenticação:** Requer token JWT.
- **Resposta de Sucesso:**
  ```json
  {
    "success": "Operação de id 1 deletada com sucesso"
  }
  ```
- **Resposta de Erro:**
  ```json
  {
    "error": "Operação não encontrada"
  }
  ```

### 7. **Criar Operações em Lote**

- **URL:** `/operations/bulk`
- **Método:** `POST`
- **Descrição:** Cria várias operações financeiras de uma vez.
- **Autenticação:** Requer token JWT.
- **Corpo da Requisição:**
  ```json
  [
    {
      "tipo_operacao": "tipo1",
      "valor": 100.00,
      "descricao": "Descrição 1",
      "data": "2024-08-27T00:00:00"
    },
    {
      "tipo_operacao": "tipo2",
      "valor": 200.00,
      "descricao": "Descrição 2",
      "data": "2024-08-28T00:00:00"
    }
  ]
  ```
- **Resposta de Sucesso:**
  ```json
  {
    "success": "Operations [<lista de operações válidas>] added, could not add [<lista de operações inválidas>] due to bad data"
  }
  ```
- **Resposta de Erro:**
  ```json
  {
    "error": "Invalid data: no items in List"
  }
  ```

## Banco de Dados

### Modelos

1. **FinancialOperation**

   - **Tabela:** `financialOperations`
   - **Campos:**
     - `id`: ID da operação (chave primária).
     - `tipo_operacao`: Tipo da operação.
     - `valor`: Valor da operação.
     - `data`: Data da operação.
     - `descricao`: Descrição da operação.

   - **Métodos:**
     - `create_exportable()`: Retorna um dicionário representando a operação.

2. **TransactionHistory**

   - **Tabela:** `transactionHistory`
   - **Campos:**
     - `id`: ID do histórico (chave primária).
     - `operation_id`: ID da operação associada.
     - `timestamp`: Data e hora da mudança.
     - `mudancas`: Descrição da mudança.

### Configuração do Banco de Dados

- **URI do Banco de Dados:** Configurado em `Config.SQLALCHEMY_DATABASE_URI`.

### Inicialização do Banco de Dados

- As tabelas são criadas usando `Base.metadata.create_all(db)`.

## Validações

- As operações financeiras são validadas usando a função `validate_operation_data` antes de serem criadas ou atualizadas.

## Considerações Finais

Este aplicativo proporciona uma API completa para o gerenciamento de operações financeiras, com suporte para autenticação, validação e histórico de transações. Certifique-se de proteger adequadamente os tokens JWT e de validar todos os dados recebidos nas requisições.