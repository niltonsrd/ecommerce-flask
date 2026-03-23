/* ======================================
   UI.JS — Advanced Premium Interactions
====================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* ===============================
       NAVBAR BLUR + SHADOW
    =============================== */

    const navbar = document.querySelector(".navbar");

    window.addEventListener("scroll", () => {

        if (window.scrollY > 40) {

            navbar.style.backdropFilter = "blur(10px)";
            navbar.style.background = "rgba(91,94,252,0.9)";
            navbar.style.boxShadow = "0 10px 40px rgba(0,0,0,0.2)";

        } else {

            navbar.style.backdropFilter = "none";
            navbar.style.background = "";
            navbar.style.boxShadow = "none";

        }

    });


    /* ===============================
       SCROLL REVEAL PRO
    =============================== */

    const revealItems = document.querySelectorAll(".produto-card");

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.style.opacity = 1
                entry.target.style.transform = "translateY(0)"

            }

        })

    }, { threshold: 0.1 })

    revealItems.forEach(el => {

        el.style.opacity = 0
        el.style.transform = "translateY(60px)"
        el.style.transition = "all .8s cubic-bezier(.22,1,.36,1)"

        observer.observe(el)

    })


    /* ===============================
       PRODUCT IMAGE HOVER ZOOM
    =============================== */

    const productImages = document.querySelectorAll(".produto-card-image img")

    productImages.forEach(img => {

        img.addEventListener("mousemove", (e) => {

            const rect = img.getBoundingClientRect()

            const x = (e.clientX - rect.left) / rect.width
            const y = (e.clientY - rect.top) / rect.height

            img.style.transform = `
                scale(1.15)
                translate(${(x - 0.5) * 20}px, ${(y - 0.5) * 20}px)
            `

        })

        img.addEventListener("mouseleave", () => {

            img.style.transform = "scale(1)"

        })

    })


    /* ===============================
       MAGNETIC BUTTON EFFECT
    =============================== */

    const buttons = document.querySelectorAll(".btn-produto")

    buttons.forEach(btn => {

        btn.addEventListener("mousemove", (e) => {

            const rect = btn.getBoundingClientRect()

            const x = e.clientX - rect.left - rect.width / 2
            const y = e.clientY - rect.top - rect.height / 2

            btn.style.transform = `translate(${x * 0.15}px,${y * 0.2}px)`

        })

        btn.addEventListener("mouseleave", () => {

            btn.style.transform = "translate(0,0)"

        })

    })


    /* ===============================
       PRODUCT CARD GLOW
    =============================== */

    const cards = document.querySelectorAll(".produto-card")

    cards.forEach(card => {

        card.addEventListener("mousemove", (e) => {

            const rect = card.getBoundingClientRect()

            const x = e.clientX - rect.left
            const y = e.clientY - rect.top

            card.style.background =
                `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.2), transparent 40%)`

        })

        card.addEventListener("mouseleave", () => {

            card.style.background = ""

        })

    })


    /* ===============================
       SMOOTH SCROLL
    =============================== */

    document.querySelectorAll("a[href^='#']").forEach(link => {

        link.addEventListener("click", (e) => {

            const target = document.querySelector(link.getAttribute("href"))

            if (target) {

                e.preventDefault()

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                })

            }

        })

    })


})

