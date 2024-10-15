const API_URL = import.meta.env.VITE_BACKEND_API_URL;


async function fetchData() {
    try {
        const response = await fetch(API_URL);
        
        // Check if the response is successful
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();

        // Display the data in the #data-container div
        const dataContainer = document.getElementById('data-container');
        dataContainer.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        document.getElementById('data-container').innerHTML = 'Failed to load data';
    }
}

// Call the function to fetch and display data
fetchData();

// Function to handle the POST request
async function addData() {
    try {
        const response = await fetch(API_URL+"/test", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                course: 'Web Development',
                sentiment_score: 0.9
             }) // Replace with your actual data
        });

        // Check if the response is successful
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        console.log('Data successfully added:', result);
    } catch (error) {
        console.error('There was a problem with the POST operation:', error);
    }
}

// Add event listener to the button
document.getElementById('add-data').addEventListener('click', addData);