import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import pytest
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models.enums import Especialidade, Especie, TipoServico


@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def tutor_payload():
    return {
        "nome": "João Silva",
        "cpf": "12345678901",
        "email": "joao@email.com",
        "telefone": "11999999999",
        "ativo": True,
    }


@pytest.fixture
def inactive_tutor_payload():
    return {
        "nome": "Maria Inativa",
        "cpf": "98765432100",
        "email": "maria@email.com",
        "telefone": "11888888888",
        "ativo": False,
    }


@pytest.fixture
def vet_payload():
    return {
        "nome": "Dr. Carlos",
        "crmv": "CRMV1234",
        "especialidades": [Especialidade.CLINICA_GERAL.value],
        "ativo": True,
    }


@pytest.fixture
def surgeon_vet_payload():
    return {
        "nome": "Dr. Ana Cirurgia",
        "crmv": "CRMV5678",
        "especialidades": [Especialidade.CIRURGIA.value, Especialidade.CLINICA_GERAL.value],
        "ativo": True,
    }


@pytest.fixture
def inactive_vet_payload():
    return {
        "nome": "Dr. Inativo",
        "crmv": "CRMV0000",
        "especialidades": [Especialidade.CLINICA_GERAL.value],
        "ativo": False,
    }


@pytest.fixture
def animal_payload():
    return {
        "nome": "Rex",
        "especie": Especie.CACHORRO.value,
        "raca": "Labrador",
        "peso_kg": "25.50",
        "data_nascimento": "2020-01-15",
        "ativo": True,
        "obito": False,
    }


@pytest.fixture
def deceased_animal_payload():
    return {
        "nome": "Luna",
        "especie": Especie.GATO.value,
        "raca": "Siamês",
        "peso_kg": "4.20",
        "data_nascimento": "2015-05-10",
        "ativo": False,
        "obito": True,
        "data_obito": "2024-12-01",
    }


def _future_slot(hours_offset: int = 1):
    start = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0) + timedelta(
        days=1, hours=hours_offset
    )
    end = start + timedelta(hours=1)
    return start.isoformat(), end.isoformat()


@pytest.fixture
def appointment_payload():
    start, end = _future_slot(1)
    return {
        "tipo_servico": TipoServico.CONSULTA.value,
        "data_hora_inicio": start,
        "data_hora_fim": end,
        "urgente": False,
        "valor_base": "100.00",
    }


def create_tutor(client, payload):
    response = client.post("/tutors", json=payload)
    assert response.status_code == 201
    return response.json()


def create_animal(client, tutor_id, payload):
    data = {**payload, "tutor_id": tutor_id}
    response = client.post("/animals", json=data)
    assert response.status_code == 201
    return response.json()


def create_vet(client, payload):
    response = client.post("/veterinarians", json=payload)
    assert response.status_code == 201
    return response.json()


def create_appointment(client, animal_id, vet_id, payload, **extra):
    data = {
        **payload,
        "animal_id": animal_id,
        "veterinario_id": vet_id,
        **extra,
    }
    response = client.post("/appointments", json=data)
    return response


def advance_appointment(client, appointment_id):
    client.post(f"/appointments/{appointment_id}/confirm")
    client.post(f"/appointments/{appointment_id}/start")
