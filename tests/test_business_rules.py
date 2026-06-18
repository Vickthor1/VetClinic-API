from datetime import datetime, timedelta, timezone

from app.models.enums import Especialidade, TipoServico
from tests.conftest import (
    advance_appointment,
    create_animal,
    create_appointment,
    create_tutor,
    create_vet,
)


def test_schedule_conflict(client, tutor_payload, vet_payload, animal_payload, appointment_payload):
    tutor = create_tutor(client, tutor_payload)
    animal = create_animal(client, tutor["id"], animal_payload)
    vet = create_vet(client, vet_payload)

    first = create_appointment(client, animal["id"], vet["id"], appointment_payload)
    assert first.status_code == 201

    start = datetime.fromisoformat(appointment_payload["data_hora_inicio"])
    end = datetime.fromisoformat(appointment_payload["data_hora_fim"])
    overlapping = {
        **appointment_payload,
        "data_hora_inicio": (start + timedelta(minutes=30)).isoformat(),
        "data_hora_fim": (end + timedelta(minutes=30)).isoformat(),
    }
    second = create_appointment(client, animal["id"], vet["id"], overlapping)
    assert second.status_code == 409
    assert second.json()["error"] == "SCHEDULE_CONFLICT"


def test_inactive_vet(client, tutor_payload, inactive_vet_payload, animal_payload, appointment_payload):
    tutor = create_tutor(client, tutor_payload)
    animal = create_animal(client, tutor["id"], animal_payload)
    vet = create_vet(client, inactive_vet_payload)

    response = create_appointment(client, animal["id"], vet["id"], appointment_payload)
    assert response.status_code == 422
    assert response.json()["error"] == "VET_INACTIVE"


def test_inactive_owner(client, inactive_tutor_payload, vet_payload, animal_payload, appointment_payload):
    tutor = create_tutor(client, inactive_tutor_payload)
    animal = create_animal(client, tutor["id"], animal_payload)
    vet = create_vet(client, vet_payload)

    response = create_appointment(client, animal["id"], vet["id"], appointment_payload)
    assert response.status_code == 422
    assert response.json()["error"] == "OWNER_INACTIVE"


def test_deceased_pet(client, tutor_payload, vet_payload, deceased_animal_payload, appointment_payload):
    tutor = create_tutor(client, tutor_payload)
    animal = create_animal(client, tutor["id"], deceased_animal_payload)
    vet = create_vet(client, vet_payload)

    response = create_appointment(client, animal["id"], vet["id"], appointment_payload)
    assert response.status_code == 422
    assert response.json()["error"] == "PET_DECEASED"


def test_surgery_without_specialty(
    client, tutor_payload, vet_payload, animal_payload, appointment_payload
):
    tutor = create_tutor(client, tutor_payload)
    animal = create_animal(client, tutor["id"], animal_payload)
    vet = create_vet(client, vet_payload)

    surgery_payload = {**appointment_payload, "tipo_servico": TipoServico.CIRURGIA.value}
    response = create_appointment(client, animal["id"], vet["id"], surgery_payload)
    assert response.status_code == 422
    assert response.json()["error"] == "VET_MISSING_SPECIALTY"


def test_valid_prescription(client, tutor_payload, vet_payload, animal_payload, appointment_payload):
    tutor = create_tutor(client, tutor_payload)
    animal = create_animal(client, tutor["id"], animal_payload)
    vet = create_vet(client, vet_payload)
    appointment = create_appointment(client, animal["id"], vet["id"], appointment_payload).json()
    advance_appointment(client, appointment["id"])

    response = client.post(
        "/prescriptions",
        json={
            "consulta_id": appointment["id"],
            "medicamento": "Antibiótico",
            "dosagem": "10mg",
            "quantidade": 2,
            "frequencia": "12/12h",
            "duracao_dias": 7,
            "valor_unitario": "25.00",
        },
    )
    assert response.status_code == 201
    assert response.json()["medicamento"] == "Antibiótico"


def test_invalid_prescription_not_in_progress(
    client, tutor_payload, vet_payload, animal_payload, appointment_payload
):
    tutor = create_tutor(client, tutor_payload)
    animal = create_animal(client, tutor["id"], animal_payload)
    vet = create_vet(client, vet_payload)
    appointment = create_appointment(client, animal["id"], vet["id"], appointment_payload).json()

    response = client.post(
        "/prescriptions",
        json={
            "consulta_id": appointment["id"],
            "medicamento": "Antibiótico",
            "dosagem": "10mg",
            "quantidade": 1,
            "frequencia": "12/12h",
            "duracao_dias": 5,
            "valor_unitario": "15.00",
        },
    )
    assert response.status_code == 409
    assert response.json()["error"] == "APPOINTMENT_NOT_IN_PROGRESS"


def test_cancel_without_reason(client, tutor_payload, vet_payload, animal_payload, appointment_payload):
    tutor = create_tutor(client, tutor_payload)
    animal = create_animal(client, tutor["id"], animal_payload)
    vet = create_vet(client, vet_payload)
    appointment = create_appointment(client, animal["id"], vet["id"], appointment_payload).json()

    response = client.post(f"/appointments/{appointment['id']}/cancel", json={})
    assert response.status_code == 422
    body = response.json()
    assert body["error"] in ("CANCELLATION_REASON_REQUIRED", "VALIDATION_ERROR")


def test_total_value_calculation(
    client, tutor_payload, vet_payload, animal_payload, appointment_payload
):
    tutor = create_tutor(client, tutor_payload)
    animal = create_animal(client, tutor["id"], animal_payload)
    vet = create_vet(client, vet_payload)

    urgent_payload = {**appointment_payload, "urgente": True, "valor_base": "200.00"}
    appointment = create_appointment(client, animal["id"], vet["id"], urgent_payload).json()
    advance_appointment(client, appointment["id"])

    client.post(
        "/prescriptions",
        json={
            "consulta_id": appointment["id"],
            "medicamento": "Medicamento A",
            "dosagem": "5mg",
            "quantidade": 3,
            "frequencia": "8/8h",
            "duracao_dias": 10,
            "valor_unitario": "10.00",
        },
    )
    client.post(
        "/prescriptions",
        json={
            "consulta_id": appointment["id"],
            "medicamento": "Medicamento B",
            "dosagem": "2mg",
            "quantidade": 1,
            "frequencia": "24/24h",
            "duracao_dias": 5,
            "valor_unitario": "20.00",
        },
    )

    complete = client.post(f"/appointments/{appointment['id']}/complete")
    assert complete.status_code == 200
    # valor_total = 200 + (10*3 + 20*1) + 30% de 200 = 200 + 50 + 60 = 310
    assert complete.json()["valor_total"] == "310.00"


def test_invalid_transition(client, tutor_payload, vet_payload, animal_payload, appointment_payload):
    tutor = create_tutor(client, tutor_payload)
    animal = create_animal(client, tutor["id"], animal_payload)
    vet = create_vet(client, vet_payload)
    appointment = create_appointment(client, animal["id"], vet["id"], appointment_payload).json()

    response = client.post(f"/appointments/{appointment['id']}/complete")
    assert response.status_code == 409
    assert response.json()["error"] == "INVALID_TRANSITION"


def test_surgery_with_specialty(
    client, tutor_payload, surgeon_vet_payload, animal_payload, appointment_payload
):
    tutor = create_tutor(client, tutor_payload)
    animal = create_animal(client, tutor["id"], animal_payload)
    vet = create_vet(client, surgeon_vet_payload)

    surgery_payload = {**appointment_payload, "tipo_servico": TipoServico.CIRURGIA.value}
    response = create_appointment(client, animal["id"], vet["id"], surgery_payload)
    assert response.status_code == 201
