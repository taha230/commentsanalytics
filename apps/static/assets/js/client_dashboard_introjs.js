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
// // Start the tour
// // document.getElementById('startTour').addEventListener('click', function() {
// //     intro.start();
// // });


intro.start();
