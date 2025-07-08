
    // Fonction pour mettre à jour l'heure
    function updateRates() {
        const now = new Date();
        const options = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZone: 'GMT' };
        const timeString = now.toLocaleTimeString('fr-FR', options);
        document.getElementById('lastUpdate').textContent = timeString + ' GMT';
    }

    // Mettre à jour l'heure au chargement de la page
    window.onload = function() {
        updateRates();
    };
