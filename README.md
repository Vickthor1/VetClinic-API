# VetClinic API

API REST para **Gestão de Clínica Veterinária**, desenvolvida com FastAPI, SQLAlchemy 2.x, PostgreSQL e Alembic, seguindo arquitetura em camadas.

## Domínio

O sistema gerencia o ciclo completo de atendimento veterinário:

- **Tutores** — responsáveis pelos animais
- **Animais** — pacientes vinculados a tutores
- **Veterinários** — profissionais com especialidades
- **Consultas (Appointments)** — agendamentos com máquina de estados
- **Prescrições** — medicamentos prescritos durante atendimento
- **Histórico de Status** — auditoria de transições de consulta

## Arquitetura

```
app/
├── main.py              # Entry point FastAPI
├── core/                # Config, DB, exceptions, handlers
├── models/              # SQLAlchemy ORM
├── schemas/             # Pydantic v2 (Create/Update/Response)
├── repositories/        # Acesso a dados (queries, filtros, paginação)
├── services/            # Regras de negócio RN-001 a RN-008
└── routers/             # Endpoints HTTP (sem regra de negócio)
```

**Fluxo:** Router → Service → Repository → Database

## Diagrama ER (ASCII)

```
┌─────────────┐       ┌─────────────┐
│   TUTORES   │       │ VETERINARIOS│
│─────────────│       │─────────────│
│ id (PK)     │       │ id (PK)     │
│ nome        │       │ nome        │
│ cpf         │       │ crmv        │
│ email       │       │ especialid. │
│ telefone    │       │ ativo       │
│ ativo       │       └──────┬──────┘
└──────┬──────┘              │
       │ 1:N                 │ 1:N
       ▼                     ▼
┌─────────────┐       ┌─────────────────────────┐
│   ANIMAIS   │       │       CONSULTAS           │
│─────────────│       │─────────────────────────│
│ id (PK)     │───N:1─│ id (PK)                 │
│ tutor_id(FK)│       │ animal_id (FK)            │
│ nome        │       │ veterinario_id (FK)       │
│ especie     │       │ tipo_servico, status      │
│ raca        │       │ data_hora_inicio/fim      │
│ peso_kg     │       │ urgente, valor_base/total │
│ obito       │       └───────────┬───────────────┘
└─────────────┘                   │ 1:N
                                  ▼
                    ┌─────────────────────────────┐
                    │ PRESCRICOES                 │
                    │─────────────────────────────│
                    │ id (PK), consulta_id (FK)   │
                    │ medicamento, dosagem, etc.  │
                    └─────────────────────────────┘

                    ┌─────────────────────────────┐
                    │ APPOINTMENT_STATUS_HISTORY  │
                    │─────────────────────────────│
                    │ appointment_id (FK)         │
                    │ old_status, new_status      │
                    │ changed_at, changed_by      │
                    └─────────────────────────────┘
```

## Máquina de Estados (Consultas)

```
AGENDADO
   ↓ confirm
CONFIRMADO
   ↓ start
EM_ATENDIMENTO
   ↓ complete
CONCLUIDO (terminal)

AGENDADO ──cancel──→ CANCELADO (terminal)
CONFIRMADO ──cancel──→ CANCELADO (terminal)
CONFIRMADO ──no-show──→ NAO_COMPARECEU (terminal)
```

Transições inválidas retornam `409 INVALID_TRANSITION`.

## Regras de Negócio

| Código | Regra | HTTP | Error Code |
|--------|-------|------|------------|
| RN-001 | Sem sobreposição de agenda (SELECT FOR UPDATE) | 409 | SCHEDULE_CONFLICT |
| RN-002 | Veterinário inativo não recebe consultas | 422 | VET_INACTIVE |
| RN-003 | Tutor inativo bloqueia agendamentos | 422 | OWNER_INACTIVE |
| RN-004 | Animal falecido não recebe consultas | 422 | PET_DECEASED |
| RN-005 | Cirurgia exige especialidade CIRURGIA | 422 | VET_MISSING_SPECIALTY |
| RN-006 | Cálculo de valor_total ao concluir | — | — |
| RN-007 | Cancelamento exige motivo | 422 | CANCELLATION_REASON_REQUIRED |
| RN-008 | Prescrição só em EM_ATENDIMENTO | 409 | APPOINTMENT_NOT_IN_PROGRESS |

**RN-006 — Fórmula:**

```
valor_total = valor_base
            + Σ(prescricao.valor_unitario × quantidade)
            + (30% × valor_base, se urgente=True)
```

## Casos de Borda

- Consultas canceladas e no-show não entram em conflito de agenda
- Animal com `obito=True` exige `data_obito`
- Atualização de consulta em estado terminal é bloqueada
- Prescrições criadas fora de `EM_ATENDIMENTO` são rejeitadas
- Cirurgia com veterinário sem especialidade `CIRURGIA` é rejeitada
- Constraint DB: `data_hora_fim > data_hora_inicio`

## Endpoints

### Tutores — `/tutors`
`POST`, `GET`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}`

### Animais — `/animals`
`POST`, `GET`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}`

### Veterinários — `/veterinarians`
`POST`, `GET`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}`

### Consultas — `/appointments`
`POST`, `GET`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}`

**Filtros GET /appointments:** `status`, `animal_id`, `veterinario_id`, `tipo_servico`, `data_inicio`, `data_fim`, `limit`, `offset`

**Transições:**
- `POST /appointments/{id}/confirm`
- `POST /appointments/{id}/start`
- `POST /appointments/{id}/complete`
- `POST /appointments/{id}/cancel`
- `POST /appointments/{id}/no-show`

### Prescrições — `/prescriptions`
`POST`, `GET`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}`, `GET /by-appointment/{consulta_id}`

### Health — `/health`

## Formato de Erro

```json
{
  "error": "ERROR_CODE",
  "message": "Mensagem amigável",
  "details": {}
}
```

## Como Executar

### Docker (recomendado)

```bash
cp .env.example .env
docker compose up --build
```

Serviços:
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **PostgreSQL:** localhost:5432
- **pgAdmin:** http://localhost:5050

### Local (desenvolvimento)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Ajuste DATABASE_URL para PostgreSQL local
uvicorn app.main:app --reload
```

## Migrations

```bash
# Aplicar todas
alembic upgrade head

# Reverter última
alembic downgrade -1

# Histórico
alembic history
```

**Migrations:**
1. `001_initial_structure` — tabelas base
2. `002_add_urgente_valor_total` — urgente, valor_total, constraint de datas
3. `003_appointment_status_history` — auditoria de status

## Testes

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Banco isolado em memória (SQLite) por fixture. **11 testes** cobrindo todas as regras de negócio.

## Stack

- Python 3.12+
- FastAPI 0.115
- SQLAlchemy 2.x
- PostgreSQL 16
- Alembic
- Pydantic v2
- Pytest
- Docker & Docker Compose
