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

        let sentiment = "";

        if (each_class.avg_sentiment == 0){
            sentiment = "Neutral";
        }
        else if (each_class.avg_sentiment > 0){
            sentiment = "Positive";
        }
        else if (each_class.avg_sentiment < 0){
            sentiment = "Negative";
        }
        else{
            sentiment = "Channel Empty";
        }
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${each_class.name}</td>
        <td>${sentiment}</td>
        <td>${each_class.avg_sentiment}</td>
        <td>${each_class.last_read}</td>
        `;
        tableBody.appendChild(row);
    }
}

// async function populateCard() {

//     const raw_data = await fetchData();

//     const mainBody = document.createElement('card-container');
    
//     for (let each_class of raw_data){
//         const each_card = document.createElement('div');
//         each_card.classList = 'card-body';
//         const content = `
//             <div class="card">
//             <div class="card-header" id="card-container">
//             </div>
//                 <div class="card-body">
//                     <h5>${each_class.title}</h5>
//                     <p>${each_class.description}</p?
//                 </div>
//             </div>
//         `;

//         mainBody.innerHTML+=each_card;
//     }
//     alert("Data is Fetched!");
// }


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