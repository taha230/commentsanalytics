// Initialize Intro.js

const intro = introJs();

// Define the steps for the tour
intro.setOptions({
    steps: [
        {
            element: "#first-step-introjs-new-bulk",
            intro: "📝 Please input the title for your bulk request Here. 📦"

        }
        ,{
            element: "#second-step-introjs-new-bulk",
            intro: "🔍 Here, you can access the list of various import comments data methods available and choose the method that suits your needs. 💡"
        }
        ,{
            element: "#third-step-introjs-new-bulk",
            intro: "👉 Let's select the JSON import method, which allows you to import comments data that exported using our Chrome extension. 📥"
        }
        ,{
            element: "#forth-step-introjs-new-bulk",
            intro: "📂 Here, you should browse your Json file that contains your comments data. 🗃️"
        }
        ,{
            element: "#fifth-step-introjs-new-bulk",
            intro: "👆 Click on this button to preview your imported data. 👀"
        }
    ]
});

document.getElementById('startTourButton').addEventListener('click', function() {
    intro.start();
});



if (!getCookie('tourShown_new_bulk')) {      
    intro.start();
    setCookie('tourShown_new_bulk', 'true', 365); // Cookie expires in 365 days
}

// Function to set a cookie
function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = name + '=' + value + ';expires=' + expires.toUTCString();
}

// Function to get a cookie by name
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}