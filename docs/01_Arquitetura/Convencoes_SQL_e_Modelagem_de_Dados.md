# CentopeIA — Convenções SQL e Modelagem de Dados

## 1. Objetivo

Este documento estabelece as convenções oficiais de modelagem relacional e SQL da CentopeIA.

O objetivo é garantir:

- consistência;
- legibilidade;
- governança;
- rastreabilidade;
- facilidade de manutenção;
- compatibilidade entre código, APIs e banco de dados;
- evolução segura do schema.

Aplica-se inicialmente ao PostgreSQL da CentopeIA.

---

## 2. Idioma

Todos os objetos técnicos persistidos no banco devem usar inglês.

Exemplos:

worker
agent
persona
user
job
worker_capability

A documentação explicativa pode permanecer em português.

---

## 3. Naming convention

### 3.1 Padrão geral

Utilizar `snake_case`.

Exemplos:

worker_id
registered_at
administrative_status
last_seen_at

Não utilizar:

camelCase
PascalCase
kebab-case
espaços

---

## 4. Tabelas

Tabelas de entidades devem utilizar nomes no singular.

Exemplos:

worker
agent
persona
user
job

O nome da tabela representa a entidade persistida e não necessariamente o nome do componente de software.

Exemplo:

Componente: Worker Registry

Entidade persistida: worker

Evitar `worker_registry` quando a tabela representa apenas os Workers conhecidos pelo Registry.

---

## 5. Chaves primárias

Chaves primárias devem utilizar:

<entity>_id

Exemplos:

worker_id
agent_id
persona_id
user_id
job_id

Evitar colunas genéricas chamadas apenas `id`.

Isso facilita joins, leitura de queries e contratos entre serviços.

---

## 6. Chaves estrangeiras

Uma Foreign Key deve manter o mesmo nome da Primary Key referenciada.

Exemplo:

worker.worker_id
worker_job.worker_id

---

## 7. Datas e horários

Utilizar `TIMESTAMPTZ` para timestamps operacionais.

Convenções comuns:

created_at
updated_at
registered_at
last_seen_at
started_at
finished_at
expires_at

Evitar `TIMESTAMP` sem timezone para eventos distribuídos.

---

## 8. Booleanos

Booleanos devem possuir nomes semanticamente claros.

Prefixos preferenciais:

is_
has_
can_

Exemplos:

is_enabled
has_gpu
can_execute_local_llm

---

## 9. Status

Evitar PostgreSQL ENUM nas fases iniciais do projeto.

Utilizar TEXT com CHECK CONSTRAINT quando o conjunto de estados for controlado.

Isso facilita evolução arquitetural e migrations.

Sempre que possível, separar:

administrative_status

de:

observed_status

Valores iniciais:

administrative_status:
- enabled
- drained
- disabled

observed_status:
- unknown
- healthy
- unhealthy
- offline

O estado administrativo representa intenção do Control Plane.

O estado observado representa o estado efetivamente detectado.

---

## 10. JSONB

JSONB deve ser utilizado apenas quando:

- a estrutura é variável;
- os atributos podem evoluir independentemente;
- a normalização não agrega valor naquele estágio;
- o campo representa metadata ou capabilities flexíveis.

JSONB não deve ser utilizado apenas para evitar modelagem relacional.

---

## 11. Índices

Convenção:

idx_<table>__<column>

ou:

idx_<table>__<column1>_<column2>

Exemplos:

idx_worker__observed_status
idx_worker__last_seen_at
idx_job__worker_id_status

---

## 12. Unique Constraints

Convenção:

uq_<table>__<column>

Exemplo:

uq_user__email

---

## 13. Foreign Keys

Convenção:

fk_<table>__<referenced_table>

Quando houver múltiplas referências para a mesma tabela, complementar com a coluna.

Exemplo:

fk_worker_job__worker

---

## 14. Check Constraints

Convenção:

ck_<table>__<rule>

Exemplos:

ck_worker__port_range
ck_worker__administrative_status
ck_worker__observed_status

---

## 15. Migrations

Toda alteração estrutural do banco deve possuir migration versionada.

Formato:

NNN_<acao>_<objeto>.sql

Exemplos:

001_create_worker.sql
002_create_worker_capability.sql
003_create_job.sql
004_add_gpu_metadata_to_worker.sql

Não executar alterações estruturais permanentes apenas manualmente no PostgreSQL sem registrar a migration correspondente.

---

## 16. Regras para migrations

Uma migration deve:

- possuir responsabilidade clara;
- ser versionada;
- utilizar SQL legível;
- evitar múltiplos domínios não relacionados;
- ser executável de forma previsível;
- falhar explicitamente em caso de erro;
- ser documentada no catálogo de dados.

Quando apropriado utilizar:

CREATE TABLE IF NOT EXISTS
CREATE INDEX IF NOT EXISTS

Alterações destrutivas devem receber tratamento especial e backup prévio.

---

## 17. Campos temporais

Entidades persistentes normalmente devem considerar:

created_at
updated_at

Entidades operacionais podem também possuir:

registered_at
last_seen_at
started_at
finished_at

Nem todos são obrigatórios em todas as tabelas.

---

## 18. Identidade lógica versus infraestrutura

Identificadores persistidos devem representar identidade lógica e não detalhes temporários de infraestrutura.

Exemplo:

worker_id = cpia-dev-wkr-01

Detalhes como IP, hostname, container, GPU e runtime são atributos do Worker e podem mudar.

---

## 19. Relação com a arquitetura CentopeIA

A modelagem de dados deve preservar a separação entre:

- Control Plane;
- Data Plane;
- Worker Registry;
- Worker Router;
- Scheduler;
- Model Router;
- Model Gateway;
- Cérebro;
- Perna;
- Persona.

As tabelas representam entidades e estados.

Os componentes representam responsabilidades arquiteturais.

Uma tabela não deve ser nomeada apenas com base no nome do serviço que a utiliza.

---

## 20. Governança

Toda nova tabela deve possuir entrada correspondente no:

Catalogo_de_Dados_CentopeIA.md

A documentação mínima deve conter:

- propósito;
- domínio;
- campos;
- tipos;
- obrigatoriedade;
- Primary Key;
- Foreign Keys;
- índices;
- constraints;
- regras de negócio;
- produtor dos dados;
- consumidores dos dados;
- lifecycle, quando relevante.
