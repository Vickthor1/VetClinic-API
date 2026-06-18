import enum


class Especie(str, enum.Enum):
    CACHORRO = "CACHORRO"
    GATO = "GATO"
    AVE = "AVE"
    REPTIL = "REPTIL"
    OUTRO = "OUTRO"


class TipoServico(str, enum.Enum):
    CONSULTA = "CONSULTA"
    RETORNO = "RETORNO"
    CIRURGIA = "CIRURGIA"
    EXAME = "EXAME"
    VACINA = "VACINA"


class ConsultaStatus(str, enum.Enum):
    AGENDADO = "AGENDADO"
    CONFIRMADO = "CONFIRMADO"
    EM_ATENDIMENTO = "EM_ATENDIMENTO"
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"
    NAO_COMPARECEU = "NAO_COMPARECEU"


class Especialidade(str, enum.Enum):
    CLINICA_GERAL = "CLINICA_GERAL"
    CIRURGIA = "CIRURGIA"
    DERMATOLOGIA = "DERMATOLOGIA"
    CARDIOLOGIA = "CARDIOLOGIA"
    ONCOLOGIA = "ONCOLOGIA"
