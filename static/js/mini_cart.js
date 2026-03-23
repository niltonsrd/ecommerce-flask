document.addEventListener("DOMContentLoaded", function () {
    const miniCartToggle = document.getElementById("miniCartToggle");
    const miniCartDropdown = document.getElementById("miniCartDropdown");

    if (miniCartToggle && miniCartDropdown) {
        miniCartToggle.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            miniCartDropdown.classList.toggle("active");
        });

        document.addEventListener("click", function (e) {
            if (!miniCartDropdown.contains(e.target) && !miniCartToggle.contains(e.target)) {
                miniCartDropdown.classList.remove("active");
            }
        });

        miniCartDropdown.addEventListener("click", function (e) {
            e.stopPropagation();
        });
    }

    inicializarEventosMiniCarrinho();
    inicializarFormsAdicionarCarrinho();
});

function formatarPreco(valor) {
    return Number(valor || 0).toFixed(2).replace(".", ",");
}

function atualizarBadgeCarrinho(totalCarrinho) {
    const badge = document.getElementById("cartCountBadge");
    const headerCount = document.getElementById("miniCartHeaderCount");

    if (badge) {
        badge.textContent = totalCarrinho;
    }

    if (headerCount) {
        headerCount.textContent = `${totalCarrinho} item(ns)`;
    }
}

function garantirEstruturaMiniCarrinho() {
    const dropdown = document.getElementById("miniCartDropdown");
    if (!dropdown) return null;

    let itemsContainer = document.getElementById("miniCartItems");
    let footer = dropdown.querySelector(".mini-cart-footer");
    let totalElement = document.getElementById("miniCartTotalValue");
    let emptyState = document.getElementById("miniCartEmpty");

    if (!itemsContainer) {
        itemsContainer = document.createElement("div");
        itemsContainer.className = "mini-cart-items";
        itemsContainer.id = "miniCartItems";

        if (footer) {
            dropdown.insertBefore(itemsContainer, footer);
        } else {
            dropdown.appendChild(itemsContainer);
        }
    }

    if (!footer) {
        footer = document.createElement("div");
        footer.className = "mini-cart-footer";
        footer.innerHTML = `
            <div class="mini-cart-total">
                <span>Total</span>
                <strong id="miniCartTotalValue">R$ 0,00</strong>
            </div>

            <div class="mini-cart-actions">
                <a href="/carrinho" class="mini-cart-btn secondary">Ver carrinho</a>
                <a href="/checkout" class="mini-cart-btn primary">Checkout</a>
            </div>
        `;
        dropdown.appendChild(footer);
        totalElement = document.getElementById("miniCartTotalValue");
    }

    return {
        dropdown,
        itemsContainer,
        footer,
        totalElement,
        emptyState
    };
}

function renderizarMiniCarrinho(itens, total, totalCarrinho) {
    const estrutura = garantirEstruturaMiniCarrinho();
    if (!estrutura) return;

    const { dropdown, itemsContainer, footer, totalElement } = estrutura;
    let emptyState = document.getElementById("miniCartEmpty");

    itemsContainer.innerHTML = "";

    if (!itens || itens.length === 0) {
        itemsContainer.style.display = "none";
        footer.style.display = "none";

        if (!emptyState) {
            emptyState = document.createElement("div");
            emptyState.className = "mini-cart-empty";
            emptyState.id = "miniCartEmpty";
            emptyState.innerHTML = `
                <p>Seu carrinho está vazio.</p>
                <a href="/produtos" class="mini-cart-btn primary">Continuar comprando</a>
            `;
            dropdown.appendChild(emptyState);
        }

        if (totalElement) {
            totalElement.textContent = "R$ 0,00";
        }

        atualizarBadgeCarrinho(0);
        return;
    }

    if (emptyState) {
        emptyState.remove();
    }

    itemsContainer.style.display = "";
    footer.style.display = "";

    itens.forEach(item => {
        const html = `
            <div class="mini-cart-item">
                <button
                    type="button"
                    class="mini-cart-remove"
                    data-item-id="${item.id}"
                    title="Remover item"
                    aria-label="Remover ${item.nome} do carrinho"
                >
                    ×
                </button>

                <div class="mini-cart-item-image">
                    ${item.imagem
                ? `<img src="/static/uploads/${item.imagem}" alt="${item.nome}">`
                : `<div class="mini-cart-no-image">Sem imagem</div>`
            }
                </div>

                <div class="mini-cart-item-info">
                    <h4>${item.nome}</h4>
                    <p>Tamanho: ${item.tamanho}</p>
                    <p>Qtd: ${item.quantidade}</p>
                    <strong>R$ ${formatarPreco(item.subtotal)}</strong>
                </div>
            </div>
        `;
        itemsContainer.insertAdjacentHTML("beforeend", html);
    });

    if (totalElement) {
        totalElement.textContent = `R$ ${formatarPreco(total)}`;
    }

    atualizarBadgeCarrinho(totalCarrinho);
    inicializarEventosMiniCarrinho();
}

function inicializarEventosMiniCarrinho() {
    const botoesRemover = document.querySelectorAll(".mini-cart-remove");

    botoesRemover.forEach((botao) => {
        botao.onclick = async function (e) {
            e.preventDefault();

            const itemId = this.dataset.itemId;
            if (!itemId) return;

            const formData = new FormData();
            formData.append("item_id", itemId);

            try {
                const response = await fetch("/carrinho/remover", {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });

                const data = await response.json();

                if (!response.ok || !data.ok) {
                    if (data.redirect) {
                        window.location.href = data.redirect;
                        return;
                    }
                    alert(data.message || "Não foi possível remover o item.");
                    return;
                }

                renderizarMiniCarrinho(
                    data.mini_carrinho,
                    data.mini_carrinho_total,
                    data.total_carrinho
                );

                const miniCartDropdown = document.getElementById("miniCartDropdown");
                if (miniCartDropdown) {
                    miniCartDropdown.classList.add("active");
                }
            } catch (error) {
                console.error("Erro ao remover item:", error);
                alert("Erro ao remover item do carrinho.");
            }
        };
    });
}

function inicializarFormsAdicionarCarrinho() {
    const forms = document.querySelectorAll(".produto-card-form");

    forms.forEach((form) => {
        form.onsubmit = async function (e) {
            e.preventDefault();

            const formData = new FormData(form);
            const botao = form.querySelector('button[type="submit"]');

            if (botao) {
                botao.disabled = true;
                botao.dataset.textoOriginal = botao.textContent;
                botao.textContent = "Adicionando...";
            }

            try {
                const response = await fetch("/carrinho/adicionar", {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });

                const data = await response.json();

                if (!response.ok || !data.ok) {
                    if (data.redirect) {
                        window.location.href = data.redirect;
                        return;
                    }

                    alert(data.message || "Não foi possível adicionar ao carrinho.");
                    if (botao) {
                        botao.textContent = botao.dataset.textoOriginal || "Adicionar ao carrinho";
                        botao.disabled = false;
                    }
                    return;
                }

                renderizarMiniCarrinho(
                    data.mini_carrinho,
                    data.mini_carrinho_total,
                    data.total_carrinho
                );

                const miniCartDropdown = document.getElementById("miniCartDropdown");
                if (miniCartDropdown) {
                    miniCartDropdown.classList.add("active");
                }

                if (botao) {
                    botao.textContent = "Adicionado!";
                    setTimeout(() => {
                        botao.textContent = botao.dataset.textoOriginal || "Adicionar ao carrinho";
                        botao.disabled = false;
                    }, 1200);
                }
            } catch (error) {
                console.error("Erro ao adicionar item:", error);
                alert("Erro ao adicionar produto ao carrinho.");

                if (botao) {
                    botao.textContent = botao.dataset.textoOriginal || "Adicionar ao carrinho";
                    botao.disabled = false;
                }
            }
        };
    });
}
async function atualizarMiniCarrinho() {
    try {
        const response = await fetch("/carrinho/mini");
        const data = await response.json();

        if (!data.ok) return;

        const badge = document.getElementById("cartCountBadge");
        const headerCount = document.getElementById("miniCartHeaderCount");
        const itemsContainer = document.getElementById("miniCartItems");
        const totalValue = document.getElementById("miniCartTotalValue");
        const emptyContainer = document.getElementById("miniCartEmpty");

        // Atualiza contador
        if (badge) badge.textContent = data.total_carrinho;
        if (headerCount) headerCount.textContent = `${data.total_carrinho} item(ns)`;

        // Limpa itens
        if (itemsContainer) itemsContainer.innerHTML = "";

        if (data.mini_carrinho.length === 0) {
            if (emptyContainer) emptyContainer.style.display = "block";
            if (itemsContainer) itemsContainer.style.display = "none";
        } else {
            if (emptyContainer) emptyContainer.style.display = "none";
            if (itemsContainer) itemsContainer.style.display = "block";

            data.mini_carrinho.forEach(item => {
                const el = document.createElement("div");
                el.classList.add("mini-cart-item");

                el.innerHTML = `
                    <div>
                        <h4>${item.nome}</h4>
                        <p>Qtd: ${item.quantidade}</p>
                        <strong>R$ ${item.subtotal.toFixed(2)}</strong>
                    </div>
                `;

                itemsContainer.appendChild(el);
            });
        }

        if (totalValue) {
            totalValue.textContent = `R$ ${data.mini_carrinho_total.toFixed(2)}`;
        }

    } catch (error) {
        console.error("Erro ao atualizar mini carrinho:", error);
    }
}