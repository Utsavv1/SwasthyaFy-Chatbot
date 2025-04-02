// Translation dictionary
const translations = {
    "hindi": {
        "Swasthyafy Report": "स्वस्थ्यफाई रिपोर्ट",
        "User Information": "उपयोगकर्ता जानकारी",
        "Swasthyafy AI assistant": "स्वस्थ्यफाई एआई सहायक",
        "welcome": "स्वस्थ्यफाई AI में आपका स्वागत है",
        "disclaimer": "यह मूल्यांकन केवल सूचनात्मक उद्देश्यों के लिए है और चिकित्सा निदान प्रदान नहीं करता है। चिकित्सा आपातकाल की स्थिति में, तुरंत अपने स्थानीय आपातकालीन नंबर पर कॉल करें।",
        "instructions": "कृपया आगे बढ़ने से पहले नीचे दिया गया संक्षिप्त फ़ॉर्म पूरा करें। यह आपके लक्षणों का अधिक सटीक आकलन करने में मदद करेगा। यदि आप यह मूल्यांकन किसी और के लिए कर रहे हैं, तो कृपया उनकी जानकारी प्रदान करें।",
        "Name": "नाम",
        "Age": "आयु",
        "gender": "लिंग",
        "male": "पुरुष",
        "female": "महिला",
        "other": "अन्य",
        "note": "हमारा चैटबॉट सहायक अंतर्दृष्टि और मार्गदर्शन प्रदान करता है, लेकिन यह पेशेवर चिकित्सा सलाह, निदान या उपचार का विकल्प नहीं है। किसी भी स्वास्थ्य समस्या के लिए हमेशा एक योग्य स्वास्थ्य सेवा प्रदाता से परामर्श करें।"
    },
    "spanish": {
        "welcome": "Bienvenido a Swasthyafy AI",
        "disclaimer": "Esta evaluación es solo para fines informativos y no proporciona diagnósticos médicos. En caso de una emergencia médica, llame inmediatamente a su número de emergencia local.",
        "instructions": "Por favor complete el breve formulario a continuación antes de continuar. Esto permitirá una evaluación más precisa de sus síntomas. Si está haciendo esta evaluación en nombre de otra persona, proporcione su información en lugar de la suya.",
        "Name": "Nombre",
        "Age": "Edad",
        "gender": "Género",
        "male": "Hombre",
        "female": "Mujer",
        "other": "Otro",
        "note": "Si bien nuestro chatbot proporciona información útil y orientación, no sustituye el consejo, diagnóstico o tratamiento médico profesional. Siempre consulte a un proveedor de atención médica calificado para cualquier problema de salud."
    },
    "french": {
        "welcome": "Bienvenue sur Swasthyafy AI",
        "disclaimer": "Cette évaluation est à titre informatif uniquement et ne fournit pas de diagnostics médicaux. En cas d'urgence médicale, appelez immédiatement votre numéro d'urgence local.",
        "instructions": "Veuillez remplir le bref formulaire ci-dessous avant de continuer. Cela permettra une évaluation plus précise de vos symptômes. Si vous faites cette évaluation pour quelqu'un d'autre, veuillez fournir ses informations au lieu des vôtres.",
        "Name": "Nom",
        "Age": "Âge",
        "gender": "Genre",
        "male": "Homme",
        "female": "Femme",
        "other": "Autre",
        "note": "Bien que notre chatbot fournisse des informations utiles et des conseils, il ne remplace pas un avis médical professionnel, un diagnostic ou un traitement. Consultez toujours un professionnel de santé qualifié pour toute préoccupation médicale."
    }
};

// Function to translate page
function translatePage() {
    let selectedLang = localStorage.getItem("chatbotLanguage") || "english";

    if (selectedLang !== "english") {
        document.querySelectorAll("[data-translate]").forEach(element => {
            let key = element.getAttribute("data-translate");
            if (translations[selectedLang] && translations[selectedLang][key]) {
                element.textContent = translations[selectedLang][key];
            }
        });
    }
}

// Ensure translation occurs when page loads
document.addEventListener("DOMContentLoaded", translatePage);

document.addEventListener("DOMContentLoaded", function () {
    const translations = {
        "en": {
            "download": "Download Report",
            "user_information": "User Information",
            "return_home": "Return to Home"
        },
        "hi": {
            "download": "रिपोर्ट डाउनलोड करें",
            "user_information": "उपयोगकर्ता जानकारी",
            "return_home": "होम पर लौटें"
        }
    };

    // Get the stored language or default to English
    let selectedLanguage = localStorage.getItem("chatbotLanguage") || "en";

    // Function to update all elements with data-translate
    function applyTranslations() {
        document.querySelectorAll("[data-translate]").forEach(element => {
            let key = element.getAttribute("data-translate");
            if (translations[selectedLanguage][key]) {
                element.textContent = translations[selectedLanguage][key];
            }
        });
    }

    applyTranslations(); // Apply translations on page load
});
