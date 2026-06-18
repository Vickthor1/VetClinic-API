class AppException(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        status_code: int = 400,
        details: dict | None = None,
    ) -> None:
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, resource: str, resource_id: int | str) -> None:
        super().__init__(
            error_code="NOT_FOUND",
            message=f"{resource} com id {resource_id} não encontrado.",
            status_code=404,
            details={"resource": resource, "id": resource_id},
        )


class ScheduleConflictException(AppException):
    def __init__(self, details: dict | None = None) -> None:
        super().__init__(
            error_code="SCHEDULE_CONFLICT",
            message="Conflito de agenda: veterinário já possui consulta neste horário.",
            status_code=409,
            details=details or {},
        )


class VetInactiveException(AppException):
    def __init__(self) -> None:
        super().__init__(
            error_code="VET_INACTIVE",
            message="Veterinário inativo não pode receber consultas.",
            status_code=422,
        )


class OwnerInactiveException(AppException):
    def __init__(self) -> None:
        super().__init__(
            error_code="OWNER_INACTIVE",
            message="Tutor inativo bloqueia agendamentos.",
            status_code=422,
        )


class PetDeceasedException(AppException):
    def __init__(self) -> None:
        super().__init__(
            error_code="PET_DECEASED",
            message="Animal com óbito registrado não pode receber consultas.",
            status_code=422,
        )


class VetMissingSpecialtyException(AppException):
    def __init__(self) -> None:
        super().__init__(
            error_code="VET_MISSING_SPECIALTY",
            message="Cirurgias exigem veterinário com especialidade CIRURGIA.",
            status_code=422,
        )


class CancellationReasonRequiredException(AppException):
    def __init__(self) -> None:
        super().__init__(
            error_code="CANCELLATION_REASON_REQUIRED",
            message="Cancelamento exige motivo_cancelamento.",
            status_code=422,
        )


class AppointmentNotInProgressException(AppException):
    def __init__(self) -> None:
        super().__init__(
            error_code="APPOINTMENT_NOT_IN_PROGRESS",
            message="Prescrições só podem ser criadas quando a consulta estiver EM_ATENDIMENTO.",
            status_code=409,
        )


class InvalidTransitionException(AppException):
    def __init__(self, old_status: str, new_status: str) -> None:
        super().__init__(
            error_code="INVALID_TRANSITION",
            message=f"Transição inválida de {old_status} para {new_status}.",
            status_code=409,
            details={"old_status": old_status, "new_status": new_status},
        )
