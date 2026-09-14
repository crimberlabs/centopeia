# CentopeIA — Catálogo de Dados

## 1. Objetivo

Este documento representa o catálogo oficial das estruturas persistentes utilizadas pela CentopeIA.

O catálogo deve evoluir junto com as migrations do banco de dados.

---

# Domínio: Infrastructure / Worker Registry

## Tabela: worker

### Objetivo

Representar os Workers conhecidos pelo Control Plane da CentopeIA.

Um Worker é um nó capaz de executar workloads do Data Plane.

Exemplos:

- cpia-dev-wkr-01
- cpia-dev-wkr-02
- cpia-lab-gpu-01
- cpia-lab-edge-01

O Worker Registry é o componente responsável por gerenciar essas entidades.

A tabela representa a entidade Worker, e não o componente Worker Registry.

---

## Campos

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---:|---|
| worker_id | TEXT | Sim | Identidade lógica estável do Worker |
| address | INET | Sim | Endereço privado utilizado pelo Control Plane |
| port | INTEGER | Sim | Porta do Worker Protocol |
| version | TEXT | Sim | Versão do runtime CentopeIA Worker |
| administrative_status | TEXT | Sim | Estado administrativo definido pelo Control Plane |
| observed_status | TEXT | Sim | Estado operacional observado |
| capabilities | JSONB | Sim | Capacidades anunciadas pelo Worker |
| registered_at | TIMESTAMPTZ | Sim | Momento do primeiro registro do Worker |
| last_seen_at | TIMESTAMPTZ | Sim | Último contato válido recebido |
| created_at | TIMESTAMPTZ | Sim | Momento de criação do registro |
| updated_at | TIMESTAMPTZ | Sim | Última alteração do registro |

---

## Primary Key

`worker_id`

A identidade lógica do Worker deve permanecer estável durante sua existência no Registry.

Exemplo:

cpia-dev-wkr-01

---

## Status administrativo

Valores iniciais:

- enabled
- drained
- disabled

### enabled

Worker autorizado a receber novos workloads.

### drained

Worker permanece registrado, mas não deve receber novos workloads.

Pode concluir workloads existentes.

### disabled

Worker administrativamente indisponível.

---

## Status observado

Valores iniciais:

- unknown
- healthy
- unhealthy
- offline

### unknown

Ainda não existem evidências suficientes para determinar o estado.

### healthy

Worker respondeu corretamente às verificações.

### unhealthy

Worker foi alcançado, porém apresenta falha operacional.

### offline

Worker deixou de responder dentro do limite definido pelo Control Plane.

---

## Capabilities

Inicialmente armazenadas como JSONB.

Exemplo:

[
  "echo"
]

Evoluções possíveis:

- llm_inference
- embeddings
- vision
- audio
- gpu
- home_automation
- document_processing

No futuro, capacidades poderão ser normalizadas em uma tabela própria `worker_capability` quando o domínio justificar.

---

## Regras

A porta deve estar entre 1 e 65535.

`worker_id` não deve depender de:

- IP;
- container_id;
- hostname Docker;
- hardware específico.

O endereço pode mudar sem alterar `worker_id`.

---

## Índices iniciais

- idx_worker__administrative_status
- idx_worker__observed_status
- idx_worker__last_seen_at

---

## Produtor

CentopeIA Core / Worker Registry.

Futuramente o Worker Protocol enviará eventos ou operações como:

- REGISTER
- HEARTBEAT
- HEALTH

---

## Consumidores

- Worker Registry
- Worker Router
- Scheduler
- Control Center
- Observability

---

## Evolução prevista

Campos futuros podem incluir:

- node_class
- location
- cpu_count
- memory_total_mb
- memory_available_mb
- gpu_vendor
- gpu_model
- gpu_count
- vram_total_mb
- vram_available_mb
- cuda_version
- runtime
- runtime_version
- max_concurrency
- privacy_class
- data_locality
- models_available

Esses campos somente serão adicionados quando houver necessidade operacional concreta.

---

## Relação arquitetural

Worker não é Agent.

Worker representa:

onde executar

Agent representa:

o que sabe executar

Model Router decide:

qual motor cognitivo utilizar

Worker Router decide:

onde executar o workload

Scheduler decide:

quando e sob quais condições o workload será admitido e executado
