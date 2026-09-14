# CentopeIA

A **CentopeIA** é um laboratório pessoal de Engenharia de IA desenvolvido dentro da **CrimberLabs**.

O projeto tem como objetivo explorar, de forma prática e incremental, a construção de uma plataforma de inteligência artificial distribuída, persistente, model-agnostic, orientada a contexto e capaz de evoluir para uma assistente residencial inteligente com múltiplas personas.

Mais do que construir uma interface conversacional, a CentopeIA busca estudar e implementar as diferentes camadas que compõem uma plataforma moderna de IA:

- arquitetura de aplicações de IA;
- orquestração de LLMs;
- memória persistente;
- contexto de usuário;
- personas;
- agentes;
- ferramentas;
- execução distribuída;
- observabilidade;
- LLMOps;
- infraestrutura como código;
- computação local e edge;
- automação residencial;
- privacidade;
- segurança;
- governança.

O projeto também funciona como ambiente prático de aprendizado e como portfólio técnico da CrimberLabs.

---

# Visão

A CentopeIA parte de um princípio central:

> **A inteligência do sistema não deve depender de uma única LLM.**

Modelos de linguagem são tratados como motores cognitivos substituíveis.

A identidade, a memória, o histórico, o conhecimento sobre o usuário, as relações, as personas e a lógica da aplicação pertencem à própria CentopeIA.

Isso permite utilizar diferentes modelos conforme o contexto, incluindo:

- modelos locais;
- modelos open source;
- Ollama;
- OpenAI;
- Gemini;
- DeepSeek;
- outros provedores futuros.

A arquitetura deve permitir trocar ou combinar modelos sem perder a continuidade da experiência.

---

# Conceito central

A arquitetura separa responsabilidades que frequentemente ficam acopladas em aplicações de IA mais simples.

Três conceitos são especialmente importantes:

## Cérebro

O **Cérebro** é responsável pela memória persistente e pelo conhecimento acumulado pela CentopeIA.

Pode armazenar, por exemplo:

- informações declaradas pelo usuário;
- preferências;
- eventos;
- histórico relevante;
- relações;
- contexto do ambiente;
- fatos aprendidos;
- inferências;
- estado de dispositivos;
- informações temporais.

A memória deve permanecer independente da LLM utilizada.

Isso permite:

- portabilidade entre modelos;
- auditoria;
- exclusão de informações;
- governança;
- rastreabilidade;
- privacidade;
- continuidade de contexto.

---

## Perna

A **Perna** é a camada de inteligência interna da CentopeIA.

Ela será responsável progressivamente por interpretar:

- memória;
- contexto;
- relações;
- comportamento;
- sinais emocionais;
- necessidades relacionais;
- personalidade;
- continuidade de interação.

A Perna não deve ser tratada apenas como mais um modelo externo.

Ela é uma camada lógica interna que participa do fluxo de decisão mesmo quando utiliza uma LLM externa ou local para gerar parte da resposta.

Em sua fase inicial, a Perna funcionará como um **stub/proxy**.

Ela poderá decidir semanticamente entre ações como:

- `ANSWER`;
- `DELEGATE`;
- `NEED_MEMORY`;
- `NEED_CONTEXT`.

Quando não possuir capacidade própria suficiente, delegará a solicitação ao Model Router.

Mesmo quando houver delegação, a resposta retornará pela Perna antes de ser apresentada ao usuário.

Com a evolução do projeto, a Perna deverá incorporar progressivamente capacidades próprias de interpretação contextual, memória, persona e inteligência relacional.

---

## Persona

A **Persona** representa a manifestação da CentopeIA para o usuário.

Ela controla características como:

- identidade;
- estilo;
- tom;
- comportamento;
- vocabulário;
- nível de formalidade;
- forma de interação;
- características relacionais.

A Persona pertence à CentopeIA e não ao modelo utilizado.

Um mesmo usuário poderá utilizar diferentes personas sem perder memória ou continuidade.

---

# Princípio conceitual

> **O Cérebro lembra.  
> A Perna entende.  
> A Persona se manifesta.**

---

# Arquitetura lógica

Fluxo conceitual simplificado:

```text
Interface
    ↓
Gateway
    ↓
Identity / Auth
    ↓
User Context
    ↓
Core
    ↓
Perna
    ↓
Cérebro / Persona / Contexto
    ↓
Capability Check
    ├── ANSWER
    ├── NEED_MEMORY
    ├── NEED_CONTEXT
    └── DELEGATE
            ↓
       Model Router
            ↓
       Model Gateway
            ↓
       LLM / Provider
            ↓
          Perna
            ↓
       Persona Rendering
            ↓
         Resposta
```

Essa separação evita que identidade, memória e lógica da aplicação fiquem acopladas ao provedor de IA.

---

# Core

O **Core** é responsável pela coordenação principal da aplicação.

Entre suas responsabilidades atuais e futuras estão:

- receber solicitações internas;
- coordenar componentes;
- acessar serviços de dados;
- gerenciar Workers;
- integrar Scheduler;
- integrar Worker Router;
- integrar Perna;
- controlar fluxos de execução;
- expor APIs internas.

O Core não deve concentrar todas as responsabilidades da plataforma. A arquitetura procura manter componentes com papéis bem definidos.

---

# Gateway

O Gateway é o ponto oficial de entrada da plataforma.

Ele será responsável progressivamente por funções como:

- roteamento;
- autenticação;
- autorização;
- controle de acesso;
- rate limiting;
- versionamento de APIs;
- correlation IDs;
- observabilidade de entrada;
- aplicação de políticas.

O Gateway não deve se transformar no orquestrador principal da aplicação.

---

# Arquitetura distribuída

A CentopeIA também possui uma arquitetura de execução distribuída.

Uma decisão importante é separar:

1. **qual modelo cognitivo deve processar uma solicitação**;
2. **qual máquina ou nó deve executar determinado workload**.

Essas duas decisões pertencem a componentes diferentes.

---

# Model Router

O **Model Router** será responsável por selecionar o modelo de IA mais adequado para uma determinada necessidade.

Critérios futuros podem incluir:

- capacidade;
- custo;
- latência;
- disponibilidade;
- privacidade;
- execução local;
- modalidade;
- política;
- confiança;
- tamanho do contexto;
- tipo de tarefa.

Exemplo:

```text
Solicitação
    ↓
Model Router
    ↓
Ollama / OpenAI / Gemini / outro provider
```

---

# Model Gateway

O **Model Gateway** funcionará como camada de abstração entre a CentopeIA e os diferentes provedores/modelos.

O objetivo é evitar que a lógica da aplicação dependa diretamente das APIs de um único fornecedor.

Essa camada poderá padronizar:

- requests;
- responses;
- autenticação;
- erros;
- métricas;
- tokens;
- custos;
- timeout;
- fallback;
- contratos entre modelos.

---

# Worker Router

O **Worker Router** é responsável por determinar onde uma tarefa deve executar fisicamente.

Exemplos de destinos futuros:

- Worker em VPS;
- workstation local;
- GPU Worker;
- notebook;
- Raspberry Pi;
- edge device.

Exemplo:

```text
Job
    ↓
Worker Router
    ↓
Worker compatível
```

---

# Scheduler

O **Scheduler da CentopeIA** será responsável pelo controle operacional dos jobs da aplicação.

Entre suas responsabilidades previstas:

- admission control;
- filas;
- prioridades;
- concorrência;
- retries;
- deadlines;
- backpressure;
- tentativas;
- políticas de execução;
- controle de capacidade.

O Scheduler da CentopeIA é diferente de um scheduler de infraestrutura.

Por exemplo, futuramente:

```text
CentopeIA Scheduler
    ↓
decide qual job deve executar

Kubernetes Scheduler
    ↓
decide em qual Node um Pod executará
```

Essas responsabilidades não devem ser misturadas.

---

# Fluxo de execução distribuída

Fluxo conceitual:

```text
Core
    ↓
Scheduler
    ↓
Worker Router
    ↓
Worker Protocol
    ↓
Worker selecionado
    ↓
Execução
    ↓
Resultado
```

Conforme a arquitetura evoluir, filas e execução assíncrona poderão ser incorporadas a esse fluxo.

---

# Control Plane e Workers

A arquitetura atual utiliza um modelo de **Control Plane + Workers**.

## Control Plane

O Control Plane concentra componentes centrais da plataforma.

Entre eles:

- Gateway;
- Core;
- PostgreSQL;
- Redis;
- Worker Registry;
- futuramente Worker Router;
- futuramente Scheduler;
- observabilidade;
- controle administrativo.

O Control Plane permanece como autoridade lógica da CentopeIA.

---

## Worker

Um Worker representa capacidade computacional disponível para executar workloads.

Um Worker pode possuir diferentes capacidades, por exemplo:

- CPU;
- GPU;
- execução Python;
- inferência de modelos;
- visão computacional;
- automação residencial;
- processamento multimodal;
- edge computing.

Workers não representam agentes.

Um **Agent** é uma entidade lógica especializada.

Um **Worker** é um recurso físico ou computacional utilizado para executar tarefas.

---

# Worker Registry

O **Worker Registry** mantém o catálogo dos nós disponíveis para execução.

Entre as informações previstas estão:

- identidade lógica;
- endereço;
- porta;
- versão;
- status administrativo;
- status observado;
- capacidades;
- timestamps;
- heartbeat;
- metadados.

A arquitetura separa dois tipos de status:

### Status administrativo

Representa a intenção operacional:

- `enabled`;
- `drained`;
- `disabled`.

### Status observado

Representa o estado técnico percebido:

- `unknown`;
- `healthy`;
- `unhealthy`;
- `offline`.

Essa separação evita misturar decisões administrativas com condições observadas automaticamente.

O Worker não acessa diretamente o PostgreSQL do Control Plane.

A comunicação é intermediada pelo Core.

---

# Estado atual do projeto

A base inicial da arquitetura distribuída já foi implementada e validada.

Atualmente o projeto possui:

- Control Plane em VPS;
- Worker remoto em VPS independente;
- comunicação privada entre os nós;
- WireGuard;
- Docker;
- Docker Compose;
- Gateway;
- Core;
- PostgreSQL;
- Redis;
- Worker API;
- health checks;
- execução remota de jobs;
- estrutura inicial do Worker Registry;
- primeira migration SQL do Worker Registry;
- persistência de metadados;
- convenções SQL;
- catálogo de dados;
- versionamento Git;
- repositório público no GitHub.

O primeiro Worker já foi validado executando jobs remotamente através da rede privada.

---

# Infraestrutura atual

Arquitetura simplificada:

```text
Internet
   ↓
Gateway
   ↓
Control Plane
   ├── Core
   ├── PostgreSQL
   ├── Redis
   ├── Worker Registry
   │
   └── Scheduler / Worker Router
            ↓
        WireGuard
            ↓
          Worker
```

Alguns componentes apresentados acima ainda estão em evolução e fazem parte do roadmap.

---

# Segurança

Desde as primeiras versões, o projeto adota princípios básicos de segurança.

Entre eles:

- autenticação SSH por chave;
- login por senha desabilitado;
- login root remoto desabilitado;
- firewall;
- Fail2Ban;
- redes Docker separadas;
- serviços internos não expostos publicamente quando não necessário;
- comunicação privada entre Workers;
- secrets fora do Git;
- variáveis sensíveis armazenadas em arquivos protegidos;
- princípio de mínimo acesso sempre que possível.

Nenhuma credencial, token, chave privada ou senha deve ser versionada neste repositório.

---

# Dados

A CentopeIA possui convenções próprias para modelagem e governança de dados.

Entre as convenções atuais:

- nomes técnicos em inglês;
- `snake_case`;
- tabelas no singular;
- primary keys no padrão `<entity>_id`;
- timestamps em `TIMESTAMPTZ`;
- booleans prefixados por `is_`, `has_` ou `can_`;
- `TEXT + CHECK` inicialmente em vez de PostgreSQL ENUM;
- JSONB apenas para estruturas flexíveis;
- migrations versionadas;
- catálogo de dados atualizado junto das mudanças de schema.

Padrão de migrations:

```text
NNN_<acao>_<objeto>.sql
```

Exemplo:

```text
001_create_worker.sql
```

---

# Tecnologias

## Utilizadas atualmente

- Linux;
- Python;
- FastAPI;
- PostgreSQL;
- Redis;
- Docker;
- Docker Compose;
- WireGuard;
- Git;
- GitHub.

## Previstas ou em avaliação

- Ollama;
- pgvector;
- embeddings;
- RAG;
- GraphRAG;
- LangChain;
- LangGraph;
- MCP;
- Terraform;
- OpenTelemetry;
- tracing distribuído;
- métricas;
- LLMOps;
- vector databases;
- Kubernetes;
- k3s;
- GPU inference;
- computer vision;
- speech recognition;
- voice synthesis;
- edge computing.

A presença de uma tecnologia nesta lista não significa necessariamente que ela será adotada. Parte do objetivo do projeto é avaliar trade-offs antes da incorporação definitiva.

---

# Terraform

Terraform será introduzido de forma incremental.

O objetivo é tornar a infraestrutura reproduzível, auditável e versionada sem recriar recursos existentes desnecessariamente.

Princípios definidos:

- importar recursos existentes quando suportado;
- não destruir infraestrutura funcional apenas para adotar IaC;
- manter secrets fora do Git;
- separar infraestrutura do código da aplicação;
- documentar ownership de cada recurso.

---

# Kubernetes / k3s

Kubernetes não faz parte do runtime principal da V1.

A primeira fase continuará utilizando:

- Docker;
- Docker Compose;
- WireGuard.

Kubernetes/k3s será introduzido posteriormente como uma trilha de laboratório quando houver necessidade concreta relacionada a:

- múltiplos Workers;
- múltiplos workloads;
- GPU nodes;
- scheduling avançado;
- autoscaling;
- resiliência;
- service discovery;
- gerenciamento de workloads distribuídos.

A adoção deve acontecer por necessidade arquitetural ou aprendizado explícito, e não apenas pela presença da tecnologia no mercado.

---

# Model Router x Worker Router

Uma decisão arquitetural importante da CentopeIA é manter essas responsabilidades separadas.

```text
Model Router
    ↓
Qual modelo deve pensar?

Worker Router
    ↓
Onde a tarefa deve executar?
```

Exemplo:

```text
Modelo escolhido:
Llama local

Destino de execução:
GPU Worker da Crimber Station
```

Essa separação permite evoluir modelos e infraestrutura de forma independente.

---

# Estratégia local-first

Sempre que apropriado, a CentopeIA prioriza execução local.

Objetivos:

- reduzir custo;
- reduzir dependência de terceiros;
- aumentar privacidade;
- permitir experimentação;
- possibilitar funcionamento parcial offline;
- aproveitar recursos computacionais próprios.

Ollama está previsto como principal ambiente inicial para experimentação com modelos locais.

Provedores externos continuarão disponíveis quando apresentarem vantagem de capacidade, custo ou funcionalidade.

---

# Memória e contexto

A memória será tratada como camada independente dos modelos de linguagem.

Tipos de informação poderão possuir proveniência explícita.

Categorias iniciais previstas:

- `USER_DECLARED`;
- `OBSERVED`;
- `INFERRED`;
- `SYSTEM_GENERATED`.

Inferências não devem ser tratadas automaticamente como fatos.

Além do valor armazenado, uma memória poderá possuir informações como:

- origem;
- confiança;
- validade temporal;
- data de criação;
- última confirmação;
- usuário relacionado;
- contexto;
- política de retenção.

Esse desenho permitirá maior controle sobre memória, privacidade e comportamento do sistema.

---

# Inteligência relacional

Uma evolução futura da Perna envolve o conceito de **Companion Intelligence**.

Ela combina:

- Memory Intelligence;
- Contextual Intelligence;
- Persona Intelligence;
- Emotional Intelligence;
- Relational Intelligence.

O objetivo não é declarar estados emocionais do usuário como fatos.

Sinais emocionais e relacionais deverão ser tratados como inferências probabilísticas, com contexto e confiança.

---

# Observabilidade

A CentopeIA deverá permitir reconstruir o caminho completo de uma solicitação.

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

Entre as métricas previstas:

- latência;
- tokens;
- custo;
- erros;
- fallbacks;
- delegações;
- qualidade de recuperação de memória;
- falsas memórias;
- consistência de persona;
- continuidade relacional;
- decisões da Perna;
- utilização dos Workers.

No futuro, logs, métricas e traces deverão permitir correlação ponta a ponta.

---

# Estrutura do repositório

Estrutura inicial:

```text
centopeia/
├── services/
│   ├── core/
│   └── worker/
│
├── infra/
│   ├── docker/
│   └── terraform/
│
├── docs/
│   ├── 01_Arquitetura/
│   └── 05_Dados/
│
├── README.md
├── CHANGELOG.md
└── .gitignore
```

A estrutura será expandida conforme o projeto evoluir.

---

# Estratégia de desenvolvimento

A CentopeIA é construída de forma incremental.

Princípios:

1. definir;
2. implementar;
3. validar;
4. observar;
5. documentar;
6. versionar;
7. evoluir.

O objetivo é evitar complexidade prematura.

Cada nova camada deve responder a uma necessidade concreta ou a um objetivo explícito de aprendizado.

---

# Git e fluxo de desenvolvimento

O GitHub é a fonte de verdade do código.

Fluxo esperado:

```text
GitHub
   ↓
clone / pull
   ↓
desenvolvimento
   ↓
commit
   ↓
push
   ↓
build
   ↓
deploy
   ↓
validação
```

Diretórios operacionais dos servidores não devem funcionar como fonte principal do código.

Mudanças devem ser feitas no repositório e posteriormente promovidas para os ambientes de execução.

---

# Versionamento

Uma versão só é considerada liberada depois que:

- o código foi versionado;
- a imagem foi construída;
- o deploy foi realizado;
- os health checks passaram;
- os testes funcionais foram executados;
- a versão foi validada.

Somente então uma tag Git deve ser criada.

Fluxo:

```text
Git commit
   ↓
Docker image
   ↓
Deploy
   ↓
Validação
   ↓
Git tag
   ↓
Release
```

---

# Roadmap

## Fundação

- [x] Control Plane;
- [x] Worker remoto;
- [x] Docker;
- [x] PostgreSQL;
- [x] Redis;
- [x] WireGuard;
- [x] health checks;
- [x] execução remota de job;
- [x] Git;
- [x] GitHub;
- [x] convenções SQL;
- [x] primeira migration do Worker Registry.

## Orquestração distribuída

- [ ] Worker Registry operacional;
- [ ] heartbeat;
- [ ] Worker Router;
- [ ] Scheduler;
- [ ] fila de jobs;
- [ ] retries;
- [ ] backpressure;
- [ ] prioridades;
- [ ] capability matching;
- [ ] controle de concorrência;
- [ ] deadlines.

## Model Layer

- [ ] Model Gateway;
- [ ] Model Router;
- [ ] integração Ollama;
- [ ] provedores externos;
- [ ] fallback entre modelos;
- [ ] políticas de seleção;
- [ ] controle de custo;
- [ ] métricas de uso;
- [ ] contratos comuns de modelo.

## Perna

- [ ] contrato inicial;
- [ ] stub operacional;
- [ ] Context Engine;
- [ ] Memory Intelligence;
- [ ] Persona Intelligence;
- [ ] Emotional Intelligence;
- [ ] Relational Intelligence;
- [ ] Companion Intelligence;
- [ ] Personal Core.

## Memória

- [ ] memória episódica;
- [ ] memória semântica;
- [ ] memória relacional;
- [ ] embeddings;
- [ ] recuperação contextual;
- [ ] pgvector;
- [ ] RAG;
- [ ] GraphRAG;
- [ ] políticas de retenção;
- [ ] proveniência;
- [ ] confiança;
- [ ] expiração de informação.

## Personas

- [ ] identidade;
- [ ] tom;
- [ ] comportamento;
- [ ] estilo;
- [ ] preferências;
- [ ] múltiplas personas;
- [ ] troca dinâmica;
- [ ] consistência de persona.

## Agentes e ferramentas

- [ ] Agent Registry;
- [ ] Tool Registry;
- [ ] agentes especializados;
- [ ] execução de ferramentas;
- [ ] MCP;
- [ ] workflows multi-step;
- [ ] políticas de autorização.

## Observabilidade

- [ ] logs estruturados;
- [ ] correlation IDs;
- [ ] tracing distribuído;
- [ ] métricas;
- [ ] dashboards;
- [ ] custo por requisição;
- [ ] métricas de LLM;
- [ ] métricas da Perna;
- [ ] auditoria de decisões.

## Infraestrutura

- [ ] Terraform;
- [ ] import da infraestrutura existente;
- [ ] workstation local;
- [ ] GPU Worker;
- [ ] notebook Worker;
- [ ] Raspberry Pi Workers;
- [ ] edge computing;
- [ ] k3s;
- [ ] Kubernetes lab.

## Casa inteligente

- [ ] Device Registry;
- [ ] World State;
- [ ] sensores;
- [ ] TVs;
- [ ] câmeras;
- [ ] dispositivos de rede;
- [ ] automação local;
- [ ] presença;
- [ ] reconhecimento de voz;
- [ ] localização dentro da residência;
- [ ] visão computacional;
- [ ] detecção de pessoas não autorizadas.

## Interfaces

- [ ] interface web;
- [ ] autenticação de usuários;
- [ ] criação de conta;
- [ ] texto;
- [ ] voz;
- [ ] mobile;
- [ ] dashboards;
- [ ] painel administrativo.

---

# Crimber Station

A **Crimber Station** será a futura infraestrutura local de computação da CentopeIA.

Ela poderá atuar como:

- GPU Worker;
- ambiente de inferência local;
- laboratório de modelos;
- infraestrutura para visão computacional;
- processamento multimodal;
- ambiente Kubernetes/k3s;
- plataforma de experimentação.

Mesmo com a expansão da infraestrutura local, o Control Plane continuará sendo a autoridade lógica da plataforma.

---

# Edge computing

A arquitetura futura também prevê dispositivos de menor capacidade próximos ao ambiente físico.

Exemplos:

- Raspberry Pi;
- sensores;
- gateways locais;
- dispositivos especializados.

Esses componentes poderão funcionar como Edge Workers para tarefas como:

- coleta de dados;
- monitoramento;
- automação;
- processamento local;
- integração com dispositivos residenciais.

---

# Objetivo técnico

A CentopeIA é utilizada como laboratório prático para aprofundar conhecimentos em:

- AI Engineering;
- Data Engineering;
- Data Architecture;
- distributed systems;
- APIs;
- Linux;
- networking;
- segurança;
- cloud;
- containers;
- Infrastructure as Code;
- observabilidade;
- LLMOps;
- MLOps;
- edge computing;
- arquitetura de software.

---

# Objetivo de portfólio

A CentopeIA também é um projeto de portfólio técnico.

O objetivo é demonstrar não apenas utilização de ferramentas, mas principalmente:

- decisões arquiteturais;
- trade-offs;
- evolução incremental;
- documentação;
- implementação;
- validação;
- operação;
- troubleshooting;
- governança;
- aprendizado contínuo.

---

# Filosofia do projeto

A CentopeIA não busca começar como uma plataforma excessivamente complexa.

A proposta é construir uma base simples, observável e funcional e aumentar a sofisticação progressivamente.

Tecnologias são incorporadas quando apresentam:

1. necessidade funcional;
2. ganho arquitetural;
3. valor operacional;
4. oportunidade relevante de aprendizado.

A arquitetura deve crescer acompanhando o problema, e não antecipando complexidade sem necessidade.

---

# CrimberLabs

A **CrimberLabs** é um laboratório pessoal de tecnologia, dados e inteligência artificial.

A CentopeIA é seu principal projeto de experimentação e desenvolvimento.

---

# Status

**Experimental / Desenvolvimento ativo**

A arquitetura, APIs, protocolos e componentes ainda podem sofrer alterações significativas durante a evolução do projeto.
