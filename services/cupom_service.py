from datetime import datetime
from repositories.cupom_repository import buscar_cupom_por_codigo, incrementar_uso_cupom


def validar_cupom(codigo, total_compra=0):

    cupom = buscar_cupom_por_codigo(codigo)

    if not cupom:
        return None, "Cupom não encontrado"

    ativo = cupom[4]
    data_inicio = cupom[5]
    data_fim = cupom[6]
    valor_minimo = cupom[7]
    limite_uso = cupom[8]
    usos_atuais = cupom[9]
    agora = datetime.now()

    if not ativo:
        return None, "Cupom inativo"

    if data_inicio and agora < data_inicio:
        return None, "Cupom ainda não está válido"

    if data_fim and agora > data_fim:
        return None, "Cupom expirado"

    if valor_minimo and total_compra < valor_minimo:
        return None, f"Cupom válido apenas para compras acima de R$ {valor_minimo:.2f}"

    if limite_uso and limite_uso > 0 and usos_atuais >= limite_uso:
        return None, "Cupom atingiu o limite de uso"

    return cupom, None


def aplicar_desconto(total, cupom):

    if not cupom:
        return total

    tipo = cupom[2]
    valor = cupom[3]

    if tipo == "percentual":
        desconto = total * (valor / 100)
        total_final = total - desconto
    elif tipo == "fixo":
        total_final = total - valor
    else:
        total_final = total

    if total_final < 0:
        total_final = 0

    return total_final


def registrar_uso_cupom(cupom_id):
    incrementar_uso_cupom(cupom_id)
