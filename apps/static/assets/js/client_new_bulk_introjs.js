// Initialize Intro.js

const intro = introJs();

// Define the steps for the tour
intro.setOptions({
    steps: [
        {
            element: "#first-step-introjs-new-bulk",
            intro: "Please input the title for your bulk request Here."

        }
        ,{
            element: "#second-step-introjs-new-bulk",
            intro: "Here, you can access the list of various import comments data methods available and choose the method that suits your needs."
        }
        ,{
            element: "#third-step-introjs-new-bulk",
            intro: "Let's select the JSON import method, which allows you to import comments data that exported using our Chrome extension."
        }
        ,{
            element: "#forth-step-introjs-new-bulk",
            intro: "Here, you should browse your Json file that contains your comments data."
        }
        ,{
            element: "#fifth-step-introjs-new-bulk",
            intro: "Click on this button to preview your imported data."
        }
    ]
});
// // Start the tour
// // document.getElementById('startTour').addEventListener('click', function() {
// //     intro.start();
// // });


intro.start();
