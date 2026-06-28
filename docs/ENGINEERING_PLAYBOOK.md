# Project Horizon Engineering Playbook

Version 1.0

Status: Living Document

## Nossa Filosofia

Horizon não é um software.
Horizon é uma plataforma de inteligência para ativos conectados.
Toda decisão de engenharia deve fortalecer essa visão.
Nunca escrevemos código apenas para fazer funcionar.
Escrevemos código para permanecer correto durante anos.
Velocidade sem arquitetura gera dívida.
Arquitetura sem entrega gera desperdício.
Nosso objetivo é equilíbrio.

## Engineering First Principles

Toda decisão deve respeitar os princípios abaixo.

O domínio é soberano.
Nenhuma tecnologia influencia o domínio.
Nunca.

Eventos representam a verdade.
Estados são apenas projeções.
Nunca armazenamos "verdades".
Armazenamos acontecimentos.

O Digital Twin é o principal ativo da empresa.
Nenhum módulo pode modificar diretamente o estado do Twin.
Toda evolução acontece através de eventos.

IA nunca interpreta sensores.
A IA interpreta conhecimento.
Quem interpreta sensores é o domínio.

Toda decisão deve ser explicável.
Não aceitamos lógica impossível de justificar.
Toda recomendação precisa apresentar evidências.

## Organização do Repositório

O projeto utiliza Monorepo.
Nenhum serviço poderá existir fora dele.

Estrutura obrigatória:

```text
/apps
/services
/packages
/docs
/infra
/tools
/examples
```

## Arquitetura

Todo código deve respeitar DDD.
Todo domínio possui autonomia.
Todo serviço possui responsabilidade única.
Toda comunicação ocorre por contratos.
Nunca por implementação.

## Eventos

Todo comportamento importante gera um evento.
Eventos são imutáveis.
Eventos nunca são editados.
Eventos nunca são removidos.

Todo evento possui:

- ID
- Timestamp
- Aggregate ID
- Version
- Correlation ID
- Causation ID
- Metadata

## Value Objects

Sempre que um conceito possuir significado próprio ele deverá ser representado por um Value Object.

Exemplos:

- HealthScore
- Temperature
- FuelLevel
- RPM
- Voltage
- Confidence
- AssetId
- JourneyId
- EventId

Nunca utilizar tipos primitivos quando existir significado de negócio.

## Aggregate Roots

Toda entidade importante possui apenas um Aggregate Root.

Exemplos:

- Asset
- Journey
- DigitalTwin
- Maintenance
- Driver

Nunca acessar entidades internas diretamente.

## APIs

Toda funcionalidade nasce como API.
Interfaces gráficas são apenas consumidores.
Nunca implementar lógica de negócio em Controllers.
Nunca.

## Banco de Dados

Banco representa persistência.
Nunca conhecimento.
Nunca inteligência.
Nunca regras de negócio.

## Inteligência Artificial

A IA nunca possui acesso direto:

- ao banco.
- a sensores.
- à infraestrutura.

Ela conversa apenas com:

- Knowledge Engine
- Digital Twin
- Context Engine

## Testes

Todo comportamento importante deve possuir testes.
Preferimos testes de domínio.
Depois integração.
Depois infraestrutura.
Nunca escrever testes presos à implementação.

## Observabilidade

Todo evento relevante deve ser rastreável.
Todo erro deve possuir contexto.
Todo processamento deve possuir correlação.
Nada acontece de forma invisível.

## Logging

Nunca registrar informação sem contexto.

Todo log deverá responder:

- Quem?
- Quando?
- Onde?
- Por quê?
- Qual Correlation ID?

## Versionamento

Seguimos Semantic Versioning.

- MAJOR
- MINOR
- PATCH

Nunca quebrar contratos públicos sem aumento de versão major.

## Commits

Seguimos Conventional Commits.

- feat:
- fix:
- refactor:
- docs:
- test:
- perf:
- build:
- ci:

Nunca utilizar mensagens genéricas.

Exemplo incorreto:

```text
update
```

Exemplo correto:

```text
feat(asset): add Asset aggregate root
```

## Pull Requests

Toda PR deve responder:

- Qual problema resolve?
- Qual RFC implementa?
- Qual ADR utiliza?
- Quais testes foram adicionados?
- Existe breaking change?

## ADRs

Toda decisão arquitetural relevante gera um ADR.
Nunca discutir arquitetura apenas em chats.
Arquitetura pertence ao repositório.

## RFCs

Toda grande funcionalidade nasce como RFC.
O código nunca precede a arquitetura.

## Definition of Done

Uma funcionalidade só é considerada pronta quando possuir:

- Código
- Testes
- Documentação
- Observabilidade
- ADR atualizado quando necessário
- RFC atendida
- Cobertura mínima definida
- Revisão aprovada

## Papel da IA

IA é membro da equipe.
Nunca autoridade.
IA propõe.
Humanos decidem.
Toda contribuição da IA deve ser revisada.
Sempre.

## Papel do Codex

O Codex é responsável por implementação.
Nunca define arquitetura.
Nunca altera RFCs.
Nunca altera ADRs.
Nunca altera princípios.
Sempre segue a documentação oficial.

## Papel do ChatGPT

O ChatGPT atua como Chief Software Architect.

Responsável por:

- Arquitetura
- RFCs
- ADRs
- Product Thinking
- Domain Model
- Revisões Arquiteturais
- Evolução da Plataforma

## Papel do CTO

O CTO possui decisão final.
Toda arquitetura existe para atender o negócio.
Nunca o contrário.

## Cultura

Preferimos:

- clareza
- simplicidade
- evolução contínua
- consistência
- qualidade

a velocidade.

## Regra Suprema

Antes de escrever qualquer linha de código responda:

```text
Esta implementação fortalece ou enfraquece a visão do Horizon?
```

Se enfraquecer.
Não implemente.

## Nosso Compromisso

Não estamos construindo apenas um software.
Estamos construindo uma plataforma que poderá acompanhar milhões de ativos durante décadas.
Cada linha de código deve ser escrita como se fosse permanecer no projeto pelos próximos dez anos.

## Engineering Motto

Build for decades.
Think in events.
Learn continuously.
Explain everything.
Trust is our product.
