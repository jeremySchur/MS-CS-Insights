const API_URL = import.meta.env.VITE_BACKEND_API_URL;


async function fetchData() {
    try {
        const response = await fetch(API_URL);
        
        // Check if the response is successful
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        const dataContainer = document.getElementById('data-container');
        dataContainer.innerHTML = 'Data is Successfully Fetched.';
        return data;

    } catch (error) {
        console.error('There was a problem with the fetch operation1', error);
        document.getElementById('data-container').innerHTML = 'Failed to load data';
    }
}

async function populateTable() {

    const raw_data = await fetchData();

    const tableBody = document.querySelector('#data-table tbody');
    tableBody.innerHTML = ''; 
    
    for (let each_class of raw_data){
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${each_class.name}</td>
        <td>${each_class.avg_sentiment}</td>
        `;
        tableBody.appendChild(row);
    }
}

populateTable(); 

// Function to handle the POST request
// async function addData() {
//     try {
//         const response = await fetch(API_URL+"/test", {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ 
//                 course: 'Web Development',
//                 sentiment_score: 0.9
//              }) // Replace with your actual data
//         });

//         // Check if the response is successful
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }

//         const result = await response.json();
//         console.log('Data successfully added:', result);
//     } catch (error) {
//         console.error('There was a problem with the POST operation:', error);
//     }
// }

// Add event listener to the button
// document.getElementById('add-data').addEventListener('click', addData);