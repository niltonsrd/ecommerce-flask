import base64
import io
import qrcode


PIX_KEY = "05941502567"
PIX_KEY_TYPE = "CPF"
PIX_RECEIVER_NAME = "Josenilton Santos da Cruz"
PIX_CITY = "Salvador"
PIX_DESCRIPTION = "Pagamento Loja NTDEV"


def _somente_ascii(texto: str) -> str:
    return texto.encode("ascii", "ignore").decode("ascii").strip() if texto else ""


def _format_tlv(id_campo: str, valor: str) -> str:
    tamanho = f"{len(valor):02d}"
    return f"{id_campo}{tamanho}{valor}"


def _crc16(payload: str) -> str:
    polinomio = 0x1021
    resultado = 0xFFFF

    for caractere in payload:
        resultado ^= ord(caractere) << 8
        for _ in range(8):
            if resultado & 0x8000:
                resultado = ((resultado << 1) ^ polinomio) & 0xFFFF
            else:
                resultado = (resultado << 1) & 0xFFFF

    return f"{resultado:04X}"


def gerar_pix_copia_cola(valor: float, txid: str = "NTDEVPIX") -> str:
    nome = _somente_ascii(PIX_RECEIVER_NAME.upper())[:25]
    cidade = _somente_ascii(PIX_CITY.upper())[:15]
    descricao = _somente_ascii(PIX_DESCRIPTION)[:50]
    chave = PIX_KEY.strip()

    gui = _format_tlv("00", "br.gov.bcb.pix")
    chave_tlv = _format_tlv("01", chave)

    adicionais = gui + chave_tlv

    if descricao:
        adicionais += _format_tlv("02", descricao)

    merchant_account_info = _format_tlv("26", adicionais)
    merchant_category_code = _format_tlv("52", "0000")
    transaction_currency = _format_tlv("53", "986")
    transaction_amount = _format_tlv("54", f"{float(valor):.2f}")
    country_code = _format_tlv("58", "BR")
    merchant_name = _format_tlv("59", nome)
    merchant_city = _format_tlv("60", cidade)
    txid_tlv = _format_tlv("05", txid[:25])
    additional_data_field = _format_tlv("62", txid_tlv)

    payload_sem_crc = (
        _format_tlv("00", "01")
        + merchant_account_info
        + merchant_category_code
        + transaction_currency
        + transaction_amount
        + country_code
        + merchant_name
        + merchant_city
        + additional_data_field
        + "6304"
    )

    crc = _crc16(payload_sem_crc)
    return payload_sem_crc + crc


def gerar_qr_code_base64(payload_pix: str) -> str:
    qr = qrcode.QRCode(
        version=4,
        box_size=10,
        border=2,
    )
    qr.add_data(payload_pix)
    qr.make(fit=True)

    imagem = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    imagem.save(buffer, format="PNG")
    imagem_bytes = buffer.getvalue()

    return base64.b64encode(imagem_bytes).decode("utf-8")


def gerar_dados_pix(valor: float, pedido_id: int) -> dict:
    txid = f"PEDIDO{pedido_id}"
    payload = gerar_pix_copia_cola(valor=valor, txid=txid)
    qr_code_base64 = gerar_qr_code_base64(payload)

    return {
        "payload_pix": payload,
        "qr_code_base64": qr_code_base64,
        "chave_pix": PIX_KEY,
        "tipo_chave": PIX_KEY_TYPE,
        "recebedor": PIX_RECEIVER_NAME,
        "cidade": PIX_CITY,
        "banco": "C6 Bank",
    }
