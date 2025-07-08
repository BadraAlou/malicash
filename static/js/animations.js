// Animations JavaScript pour la navigation
document.addEventListener('DOMContentLoaded', function() {
    // Animation des liens au survol
    const navLinks = document.querySelectorAll('.animated-nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Animation du dropdown
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function() {
            const menu = this.nextElementSibling;
            if (menu) {
                menu.style.animation = 'slideDown 0.3s ease';
            }
        });
    });
    
    // Animation des drapeaux
    const flags = document.querySelectorAll('.flag-emoji');
    
    flags.forEach(flag => {
        flag.addEventListener('mouseenter', function() {
            this.style.animation = 'wave 0.5s ease-in-out infinite';
        });
        
        flag.addEventListener('mouseleave', function() {
            this.style.animation = 'none';
        });
    });
    
    // Effet de particules sur le brand
    const brand = document.querySelector('.animated-brand');
    
    if (brand) {
        brand.addEventListener('click', function(e) {
            createParticles(e.clientX, e.clientY);
        });
    }
    
    function createParticles(x, y) {
        for (let i = 0; i < 6; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: fixed;
                width: 6px;
                height: 6px;
                background: #ffc107;
                border-radius: 50%;
                pointer-events: none;
                z-index: 9999;
                left: ${x}px;
                top: ${y}px;
                animation: particle-explosion 0.6s ease-out forwards;
            `;
            
            document.body.appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, 600);
        }
    }
    
    // Ajouter l'animation CSS pour les particules
    const style = document.createElement('style');
    style.textContent = `
        @keyframes particle-explosion {
            0% {
                transform: translate(0, 0) scale(1);
                opacity: 1;
            }
            100% {
                transform: translate(${Math.random() * 200 - 100}px, ${Math.random() * 200 - 100}px) scale(0);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});


// Référence des emojis de drapeaux
const flagEmojis = {
    'US': '🇺🇸', // États-Unis
    'GA': '🇬🇦', // Gabon
    'CM': '🇨🇲', // Cameroun
    'GQ': '🇬🇶', // Guinée Équatoriale
    'GN': '🇬🇳', // Guinée
    'CA': '🇨🇦', // Canada
    'BF': '🇧🇫', // Burkina Faso
    'BJ': '🇧🇯', // Bénin
    'NE': '🇳🇪', // Niger
    'TG': '🇹🇬', // Togo
    'MA': '🇲🇦', // Maroc
    'TN': '🇹🇳', // Tunisie
    'ES': '🇪🇸', // Espagne
    'CN': '🇨🇳', // Chine
    'JP': '🇯🇵', // Japon
    'RU': '🇷🇺', // Russie
    'ML': '🇲🇱', // Mali
    'FR': '🇫🇷', // France
    'GB': '🇬🇧', // Royaume-Uni
    'DE': '🇩🇪', // Allemagne
    'IT': '🇮🇹', // Italie
};

// Taux de change en temps réel (simulation)
const exchangeRates = {
    'USD': 600,    // 1 USD = 600 XOF
    'EUR': 655,    // 1 EUR = 655 XOF
    'XAF': 1,      // 1 XAF = 1 XOF (parité)
    'GNF': 0.067,  // 1 GNF = 0.067 XOF
    'CAD': 445,    // 1 CAD = 445 XOF
    'MAD': 60.6,   // 1 MAD = 60.6 XOF
    'TND': 204.7,  // 1 TND = 204.7 XOF
    'CNY': 83.3,   // 1 CNY = 83.3 XOF
    'JPY': 4,      // 1 JPY = 4 XOF
    'RUB': 6.32    // 1 RUB = 6.32 XOF
};

// Fonction pour mettre à jour les taux
function updateExchangeRates() {
    const rateElements = document.querySelectorAll('.currency-rate small');
    
    rateElements.forEach(element => {
        // Animation de mise à jour
        element.style.opacity = '0.5';
        
        setTimeout(() => {
            element.style.opacity = '1';
            // Ici vous pouvez intégrer une vraie API de taux de change
        }, 300);
    });
}

// Mise à jour automatique toutes les heures
setInterval(updateExchangeRates, 3600000);


// Taux de change complets (tous vers XOF comme référence)
const exchangeRatesComplete = {
    // Devise de référence (Mali)
    XOF: 1.0,

    // Devises principales
    EUR: 655.0, // Euro vers XOF
    USD: 600.0, // Dollar US vers XOF
    CAD: 445.0, // Dollar canadien vers XOF
    GBP: 750.0, // Livre sterling vers XOF

    // Devises africaines
    XAF: 1.0, // Franc CFA BEAC (parité avec XOF)
    GNF: 0.0667, // Franc guinéen vers XOF
    MAD: 60.65, // Dirham marocain vers XOF
    TND: 204.69, // Dinar tunisien vers XOF
    DZD: 4.48, // Dinar algérien vers XOF
    NGN: 0.39, // Naira nigérian vers XOF
    GHS: 54.17, // Cedi ghanéen vers XOF
    SLL: 0.0305, // Leone vers XOF

    // Autres devises
    CNY: 83.33, // Yuan chinois vers XOF
    JPY: 4.05, // Yen japonais vers XOF
    CHF: 675.0, // Franc suisse vers XOF
    AUD: 395.0, // Dollar australien vers XOF
    }

    // Symboles de devises
    const currencySymbols = {
    XOF: "XOF",
    XAF: "XAF",
    EUR: "€",
    USD: "$",
    CAD: "CAD",
    GBP: "£",
    GNF: "GNF",
    MAD: "MAD",
    TND: "TND",
    DZD: "DZD",
    NGN: "₦",
    GHS: "GHS",
    SLL: "SLL",
    CNY: "¥",
    JPY: "¥",
    CHF: "CHF",
    AUD: "AUD",
    }

    // Grille tarifaire en XOF
    const feeStructure = [
    { min: 0, max: 65500, fee: 1965, type: "fixed" },
    { min: 65501, max: 327500, fee: 3275, type: "fixed" },
    { min: 327501, max: 655000, fee: 5240, type: "fixed" },
    { min: 655001, max: Number.POSITIVE_INFINITY, fee: 0.01, type: "percentage" },
    ]

    function updateCurrencySymbol() {
    const fromCurrency = document.getElementById("fromCurrency")
    const selectedOption = fromCurrency.options[fromCurrency.selectedIndex]
    const symbol = selectedOption.dataset.symbol || fromCurrency.value
    document.getElementById("currencySymbol").textContent = symbol
    }

    function calculateFee(amountInXOF) {
    for (const tier of feeStructure) {
        if (amountInXOF >= tier.min && amountInXOF <= tier.max) {
        if (tier.type === "fixed") {
            return tier.fee
        } else {
            return amountInXOF * tier.fee
        }
        }
    }
    return 0
    }

    function calculateAmountAuto() {
    const amount = Number.parseFloat(document.getElementById("amount").value) || 0
    const fromCurrency = document.getElementById("fromCurrency").value
    const toCurrency = document.getElementById("toCurrency").value

    if (amount <= 0) {
        document.getElementById("calculationResult").style.display = "none"
        return
    }

    // Convertir le montant d'entrée vers XOF (devise de référence)
    const amountInXOF = amount * exchangeRatesComplete[fromCurrency]

    // Calculer les frais en XOF
    const feesInXOF = calculateFee(amountInXOF)

    // Montant après frais en XOF
    const amountAfterFeesXOF = amountInXOF - feesInXOF

    // Convertir vers la devise de destination
    const finalAmount = amountAfterFeesXOF / exchangeRatesComplete[toCurrency]

    // Convertir les frais vers la devise d'origine pour l'affichage
    const feesInOriginalCurrency = feesInXOF / exchangeRatesComplete[fromCurrency]

    // Taux de change effectif
    const effectiveRate = exchangeRatesComplete[fromCurrency] / exchangeRatesComplete[toCurrency]

    // Mise à jour de l'affichage
    document.getElementById("sentAmount").textContent = `${amount.toFixed(2)} ${fromCurrency}`
    document.getElementById("fees").textContent = `${feesInOriginalCurrency.toFixed(2)} ${fromCurrency}`
    document.getElementById("exchangeRate").textContent = `1 ${fromCurrency} = ${effectiveRate.toFixed(4)} ${toCurrency}`
    document.getElementById("receivedAmount").textContent = `${finalAmount.toFixed(2)} ${toCurrency}`

    // Afficher les résultats avec animation
    const resultDiv = document.getElementById("calculationResult")
    resultDiv.style.display = "block"
    resultDiv.style.opacity = "0"
    resultDiv.style.transform = "translateY(20px)"

    setTimeout(() => {
        resultDiv.style.transition = "all 0.4s ease"
        resultDiv.style.opacity = "1"
        resultDiv.style.transform = "translateY(0)"
    }, 100)
    }

    function updateRates() {
    // Simulation de mise à jour des taux
    const now = new Date()
    document.getElementById("lastUpdate").textContent = now.toLocaleString("fr-FR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    })

    // Animation des taux
    const rateItems = document.querySelectorAll(".rate-item")
    rateItems.forEach((item, index) => {
        setTimeout(() => {
        item.style.transform = "scale(1.05)"
        setTimeout(() => {
            item.style.transform = "scale(1)"
        }, 200)
        }, index * 50)
    })
    }

    // Initialisation au chargement
    document.addEventListener("DOMContentLoaded", () => {
    updateCurrencySymbol()
    updateRates()

    // Calcul automatique lors de la saisie
    document.getElementById("amount").addEventListener("input", calculateAmountAuto)
    document.getElementById("fromCurrency").addEventListener("change", () => {
        updateCurrencySymbol()
        calculateAmountAuto()
    })
    document.getElementById("toCurrency").addEventListener("change", calculateAmountAuto)
    })


// Animation au scroll
document.addEventListener('DOMContentLoaded', function() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.animated-title, .animated-text, .mobile-image-container').forEach(el => {
        observer.observe(el);
    });
});


