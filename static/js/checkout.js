document.addEventListener("DOMContentLoaded", function () {

    const checkoutContainer = document.querySelector(".checkout-container");
    const cidadeLoja = (checkoutContainer?.dataset?.cidadeLoja || "").trim().toLowerCase();

    const enderecoRadios = document.querySelectorAll(".checkout-address-radio");
    const modalidadeRadios = document.querySelectorAll(".checkout-modalidade-radio");
    const modalidadeCards = document.querySelectorAll(".checkout-modalidade-card");
    const pagamentoRadios = document.querySelectorAll('input[name="forma_pagamento"]');

    const subtotalElement = document.getElementById("checkout-subtotal");
    const freteElement = document.getElementById("checkout-frete");
    const totalElement = document.getElementById("checkout-total-geral");
    const modalidadeNomeElement = document.getElementById("checkout-modalidade-nome");
    const prazoElement = document.getElementById("checkout-prazo");
    const descontoElement = document.getElementById("checkout-desconto-valor");
    const finalizarBtn = document.querySelector(".checkout-btn-finalizar");

    const cupomInput = document.getElementById("cupom_codigo");
    const aplicarCupomBtn = document.getElementById("checkout-aplicar-cupom");
    const cupomStatus = document.getElementById("checkout-cupom-status");

    const modalidadeStatus = document.getElementById("checkout-modalidade-status");

    let descontoAtual = 0;

    // ==============================
    // Utils
    // ==============================

    function parseCurrency(value) {
        if (!value) return 0;
        return Number(String(value).replace(",", "."));
    }

    function formatCurrency(value) {
        return value.toLocaleString("pt-BR", {
            style: "currency",
            currency: "BRL"
        });
    }

    function getSubtotal() {
        const raw = subtotalElement?.dataset?.subtotal || "0";
        return parseCurrency(raw);
    }

    function getCidadeAtual() {
        const enderecoSelecionado = document.querySelector(".checkout-address-radio:checked");

        if (enderecoSelecionado) {
            return (enderecoSelecionado.dataset.cidade || "").trim().toLowerCase();
        }

        return "";
    }

    // ==============================
    // Entrega
    // ==============================

    function filtrarModalidadesPorCidade() {
        const cidadeAtual = getCidadeAtual();

        let tiposPermitidos = ["NACIONAL"];

        if (cidadeAtual && cidadeLoja && cidadeAtual === cidadeLoja) {
            tiposPermitidos = ["RETIRADA", "LOCAL", "MOTOBOY_CLIENTE"];

            if (modalidadeStatus) {
                modalidadeStatus.textContent = "Cliente na mesma cidade da loja.";
            }
        } else if (cidadeAtual) {
            tiposPermitidos = ["NACIONAL"];

            if (modalidadeStatus) {
                modalidadeStatus.textContent = "Entrega nacional disponível.";
            }
        } else {
            if (modalidadeStatus) {
                modalidadeStatus.textContent = "Selecione um endereço.";
            }
        }

        modalidadeCards.forEach((card) => {
            const radio = card.querySelector(".checkout-modalidade-radio");
            const tipo = (radio?.dataset?.tipo || "").toUpperCase();

            if (tiposPermitidos.includes(tipo)) {
                card.classList.remove("hidden");
            } else {
                card.classList.add("hidden");
                if (radio) radio.checked = false;
            }
        });

        updateResumoEntrega();
        validarCheckout();
    }

    function updateResumoEntrega() {
        const selected = document.querySelector(".checkout-modalidade-radio:checked");
        const subtotal = getSubtotal();

        if (!selected) {
            freteElement.textContent = "R$ 0,00";
            modalidadeNomeElement.textContent = "Selecione uma modalidade";
            prazoElement.textContent = "-";
            totalElement.textContent = formatCurrency(subtotal - descontoAtual);
            return;
        }

        const valor = parseCurrency(selected.dataset.valor);
        const nome = selected.dataset.nome;
        const prazo = selected.dataset.prazo;
        const tipo = (selected.dataset.tipo || "").toUpperCase();

        const frete = tipo === "RETIRADA" ? 0 : valor;
        const total = subtotal - descontoAtual + frete;

        freteElement.textContent = formatCurrency(frete);
        modalidadeNomeElement.textContent = nome;
        prazoElement.textContent = prazo;
        totalElement.textContent = formatCurrency(total);
    }

    // ==============================
    // Validação
    // ==============================

    function validarCheckout() {
        const endereco = document.querySelector('input[name="endereco_id"]:checked');
        const modalidade = document.querySelector('input[name="modalidade_entrega_id"]:checked');
        const pagamento = document.querySelector('input[name="forma_pagamento"]:checked');

        const podeFinalizar = endereco && modalidade && pagamento;

        if (finalizarBtn) {
            finalizarBtn.disabled = !podeFinalizar;
        }
    }

    // ==============================
    // Cupom
    // ==============================

    async function aplicarCupom() {
        const codigo = (cupomInput?.value || "").trim();

        if (!codigo) return;

        try {
            const formData = new FormData();
            formData.append("cupom_codigo", codigo);

            const response = await fetch("/checkout/validar-cupom", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (!data.sucesso) throw new Error();

            descontoAtual = Number(data.dados.desconto || 0);

            descontoElement.textContent = formatCurrency(descontoAtual);
            cupomStatus.textContent = "Cupom aplicado!";
            updateResumoEntrega();

        } catch {
            descontoAtual = 0;
            descontoElement.textContent = formatCurrency(0);
            cupomStatus.textContent = "Cupom inválido.";
        }
    }

    // ==============================
    // Eventos
    // ==============================

    enderecoRadios.forEach((radio) => {
        radio.addEventListener("change", function () {
            filtrarModalidadesPorCidade();
            validarCheckout();
        });
    });

    modalidadeRadios.forEach((radio) => {
        radio.addEventListener("change", function () {
            updateResumoEntrega();
            validarCheckout();
        });
    });

    pagamentoRadios.forEach((radio) => {
        radio.addEventListener("change", validarCheckout);
    });

    if (aplicarCupomBtn) {
        aplicarCupomBtn.addEventListener("click", aplicarCupom);
    }

    // ==============================
    // Init
    // ==============================

    filtrarModalidadesPorCidade();
    updateResumoEntrega();
    validarCheckout();
});