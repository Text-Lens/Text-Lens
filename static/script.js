// Récupération des éléments
const submitBtn = document.getElementById('submitBtn');
const textInput = document.getElementById('textInput');
const loader = document.getElementById('loader');
const displayText = document.getElementById('displayText');

// Écouteur d'événement pour le bouton
submitBtn.addEventListener('click', () => {
    const userInput = textInput.value.trim();

    if (userInput !== "") {
        // Affiche le loader
        loader.style.display = "block";
        displayText.textContent = ""; // Efface le texte précédent

        // Simulation de chargement (2 secondes)
        setTimeout(() => {
            loader.style.display = "none"; // Cache le loader
            displayText.textContent = `Vous avez saisi : ${userInput}`;
        }, 2000);
    } else {
        displayText.textContent = `PLEASE ENTER YOUR TEXT`;
    }
});
