// Initialize Intro.js

const intro = introJs();

// Define the steps for the tour
intro.setOptions({
    steps: [
        {
            intro: "Hi 👋 Welcome to the tour of Comments Analytics! 📊 If you are already familiar with the dashboard, feel free to skip this introductory tour. ⏭️"
        },{
            element: "#first-step-introjs",
            intro: "You can view your current credit and active plan here. 💡 👀"
        }
        ,{
            element: "#second-step-introjs",
            intro: "Here, you can access the list of available services and click on the desired one.  😉👆"
        }
        ,{
            element: "#third-step-introjs",
            intro: "You can test the service by making a Single comment request and verifying the result. For example; Sentiment Analysis Single comment request. ✅ Try it now."
        }
        ,{
            element: "#forth-step-introjs",
            intro: "Here, you can initiate your Bulk request by importing your Bulk file and launching the process 💥. For example; Sentiment Analysis Bulk request for a list of commetns. 👌 Ready to try?"
        }
    ]
});


document.getElementById('startTourButton').addEventListener('click', function() {
    intro.start();
});

if (!getCookie('tourShown_dashboard')) {      
    intro.start();
    setCookie('tourShown_dashboard', 'true', 365); // Cookie expires in 365 days
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