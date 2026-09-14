# Changelog

Este arquivo registra as principais mudanças da CentopeIA.

Uma versão só é considerada liberada depois de:

- implementação;
- commit;
- build;
- deploy;
- testes;
- validação;
- criação da tag correspondente.

Enquanto esse ciclo não for concluído, as mudanças permanecem em **Não lançado**.

---

# [Não lançado]

---

# [0.3.0] - 2026-09-14

## Adicionado

### Versionamento e repositório

- criação do repositório Git oficial da CentopeIA;
- definição da branch principal `main`;
- criação do repositório público no GitHub;
- configuração de acesso SSH entre o Control Plane e o GitHub;
- definição do GitHub como fonte de verdade do código;
- criação inicial do `.gitignore`;
- proteção contra versionamento de secrets, estados Terraform, logs e arquivos temporários.

### Core

- implementação inicial do serviço Core;
- API baseada em FastAPI;
- integração com PostgreSQL;
- integração com Redis;
- preparação do Worker Registry;
- endpoints para registro de Workers;
- endpoint para heartbeat;
- endpoints para listagem e consulta individual de Workers.

### Worker

- implementação do Worker 01;
- identidade lógica configurável por variável de ambiente;
- endpoint `/health`;
- endpoint `/jobs`;
- job inicial do tipo `echo`;
- execução distribuída validada;
- comunicação privada via WireGuard;
- exposição do serviço apenas pela interface privada.

### Worker Registry

- criação do modelo inicial da entidade `worker`;
- criação da migration `001_create_worker.sql`;
- persistência em PostgreSQL;
- separação entre status administrativo e status observado;
- suporte a capabilities em JSONB;
- índices iniciais;
- timestamps operacionais.

### Dados

- definição das convenções SQL;
- adoção de nomes técnicos em inglês;
- adoção de `snake_case`;
- tabelas no singular;
- padrão de primary key `<entity>_id`;
- adoção de `TIMESTAMPTZ`;
- convenções para campos booleanos;
- padrão inicial de migrations;
- criação do catálogo de dados.

### Infraestrutura

- Control Plane em VPS;
- Worker remoto independente;
- Docker;
- Docker Compose;
- PostgreSQL;
- Redis;
- redes Docker separadas;
- WireGuard;
- comunicação privada entre Control Plane e Worker;
- validação de conectividade entre os nós.

### Segurança

- autenticação SSH por chave;
- login SSH por senha desabilitado;
- login root remoto desabilitado;
- firewall;
- Fail2Ban;
- comunicação privada entre nós;
- secrets mantidos fora do Git;
- arquivos sensíveis protegidos por permissões de sistema operacional.

### Documentação

- documentação de arquitetura;
- convenções de nomenclatura;
- documentação de dados;
- ADRs arquiteturais;
- roadmap de infraestrutura;
- roadmap da Crimber Station;
- documentação da Perna;
- README público do projeto;
- CHANGELOG público do projeto.

---

## Arquitetura

### Control Plane e Worker

Foi adotada uma arquitetura distribuída baseada em Control Plane e Workers.

O Control Plane permanece como autoridade lógica da plataforma.

Os Workers representam capacidade computacional disponível para execução de workloads.

---

### Model Router

Foi definido que a seleção do modelo cognitivo será responsabilidade do **Model Router**.

O Model Router responde à pergunta:

```text
Qual modelo deve processar esta solicitação?
```

Critérios futuros poderão incluir:

- capacidade;
- custo;
- latência;
- disponibilidade;
- privacidade;
- execução local;
- modalidade;
- contexto;
- política;
- confiança.

---

### Worker Router

Foi definido que a seleção do nó físico de execução será responsabilidade do **Worker Router**.

O Worker Router responde à pergunta:

```text
Onde esta tarefa deve executar?
```

Essa separação permite evoluir modelos e infraestrutura de forma independente.

---

### Scheduler

Foi definido um Scheduler próprio da aplicação para controlar:

- jobs;
- filas;
- prioridades;
- retries;
- concorrência;
- deadlines;
- backpressure;
- tentativas;
- políticas de execução.

O Scheduler da CentopeIA permanece independente de schedulers de infraestrutura como o Kubernetes Scheduler.

---

## Perna

Foi definida a **Perna** como camada interna de inteligência da CentopeIA.

A Perna:

- não é apenas outro provider;
- participa do fluxo lógico da aplicação;
- interpreta memória e contexto;
- participa da continuidade relacional;
- aplica características de persona;
- pode decidir entre responder diretamente ou delegar;
- participa da composição final da resposta.

Na fase inicial funcionará como stub/proxy.

Contratos previstos:

- `ANSWER`;
- `DELEGATE`;
- `NEED_MEMORY`;
- `NEED_CONTEXT`.

Mesmo quando houver delegação para outra LLM, a resposta deve retornar pela Perna antes da manifestação final ao usuário.

---

## Cérebro

Foi definido que o **Cérebro** será independente da LLM utilizada.

Responsabilidades previstas incluem:

- memória persistente;
- contexto histórico;
- preferências;
- relações;
- conhecimento do usuário;
- conhecimento do ambiente;
- estado de dispositivos;
- eventos relevantes.

A memória não deve ficar armazenada exclusivamente nos pesos de um modelo.

Isso permite:

- exclusão;
- auditoria;
- governança;
- portabilidade;
- rastreabilidade;
- continuidade entre diferentes modelos.

---

## Persona

Foi definida a **Persona** como camada independente do modelo de linguagem.

Responsabilidades:

- identidade;
- estilo;
- tom;
- comportamento;
- vocabulário;
- manifestação final da resposta.

A troca de modelo não deve alterar automaticamente a identidade da Persona.

---

## Memória

Foi definida a necessidade de proveniência explícita das informações.

Categorias iniciais previstas:

- `USER_DECLARED`;
- `OBSERVED`;
- `INFERRED`;
- `SYSTEM_GENERATED`.

Inferências não devem ser tratadas automaticamente como fatos.

Também deverão existir mecanismos futuros para:

- confiança;
- validade temporal;
- retenção;
- confirmação;
- atualização;
- exclusão.

---

## Inteligência relacional

Foi definido o conceito futuro de **Companion Intelligence**.

A proposta combina:

- Memory Intelligence;
- Contextual Intelligence;
- Persona Intelligence;
- Emotional Intelligence;
- Relational Intelligence.

Estados emocionais inferidos deverão ser tratados probabilisticamente, com contexto e confiança, e não como fatos absolutos.

---

## Infraestrutura como código

Foi decidido introduzir Terraform de forma incremental.

Princípios:

- evitar recriação desnecessária da infraestrutura atual;
- importar recursos existentes quando suportado;
- versionar definições de infraestrutura;
- manter secrets fora do Git;
- separar infraestrutura de aplicação da lógica de negócio.

---

## Kubernetes

Foi decidido não utilizar Kubernetes no runtime principal da V1.

A V1 seguirá inicialmente com:

- Docker;
- Docker Compose;
- WireGuard.

k3s/Kubernetes será introduzido futuramente como trilha de laboratório quando houver necessidade real de:

- múltiplos workloads;
- múltiplos Workers;
- GPU nodes;
- scheduling avançado;
- resiliência;
- autoscaling;
- service discovery mais complexo.

O Scheduler da CentopeIA continuará existindo mesmo com a adoção futura de Kubernetes.

---

## Observabilidade

Foi definido que cada solicitação deverá futuramente ser rastreável de ponta a ponta.

Fluxo conceitual:

```text
request_id
    ↓
persona
    ↓
Perna
    ↓
contexto
    ↓
memória
    ↓
decisão
    ↓
delegação
    ↓
Model Router
    ↓
modelo
    ↓
Perna
    ↓
resposta
```

Entre as métricas previstas estão:

- latência;
- tokens;
- custo;
- erros;
- fallback;
- delegações;
- qualidade da recuperação de memória;
- falsas memórias;
- consistência de persona;
- continuidade relacional;
- decisões da Perna;
- utilização dos Workers.

---

## Segurança

Foram definidos princípios iniciais de segurança e isolamento:

- autenticação SSH por chave;
- proibição de secrets no Git;
- uso de rede privada entre nós;
- redução de exposição pública;
- proteção de arquivos sensíveis;
- separação de responsabilidades;
- princípio de mínimo privilégio quando aplicável.

---

# Histórico inicial

## Baseline do repositório

Commit inicial:

```text
c0592fe chore: establish CentopeIA repository baseline
```

Incluiu:

- estrutura inicial do repositório;
- Core;
- primeira migration;
- infraestrutura Docker;
- documentação SQL;
- catálogo de dados;
- `.gitignore`.

---

## Worker 01

Commit:

```text
8f4e59f feat: add Worker 01 implementation
```

Incluiu:

- implementação do Worker;
- Dockerfile;
- requirements;
- Docker Compose do Worker;
- estrutura necessária para execução distribuída.

---

# Próxima versão planejada

## Core 0.3.0

Objetivos previstos:

- disponibilizar Worker Registry operacional;
- registrar Worker via API;
- receber heartbeat;
- listar Workers;
- consultar Worker individual;
- validar persistência PostgreSQL;
- validar integração com Worker 01;
- build da imagem `centopeia-core:0.3.0`;
- deploy;
- testes funcionais;
- validação;
- criação da tag `v0.3.0`.

A versão `v0.3.0` somente será criada após o ciclo completo de build, deploy e validação.

---

# Próximas evoluções arquiteturais

Entre os próximos blocos previstos estão:

- Worker Router;
- Scheduler;
- filas de jobs;
- capability matching;
- Model Gateway;
- Model Router;
- integração com Ollama;
- Perna stub;
- contexto;
- memória persistente;
- personas;
- agentes;
- ferramentas;
- observabilidade;
- Terraform;
- Crimber Station;
- GPU Workers;
- edge computing;
- automação residencial;
- voz;
- visão computacional.

---

# Convenção

Este CHANGELOG registra mudanças relevantes de produto, arquitetura, infraestrutura e plataforma.

Pequenos ajustes internos que não alterem comportamento, arquitetura ou operação podem permanecer registrados apenas no histórico Git.
