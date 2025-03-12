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
        dataContainer.innerHTML = '<center>Data is Successfully Fetched.</center>';
        return data;

    } catch (error) {
        console.error('<center>There was a problem with the fetch operation.</center>', error);
        document.getElementById('data-container').innerHTML = 'Failed to load data.';
    }
}

async function populateTable() {

    const raw_data = await fetchData();

    const tableBody = document.querySelector('#data-table tbody');
    tableBody.innerHTML = ''; 
    
    for (let each_class of raw_data){

        let sentiment = "Neutral";

        // Somewhat random values
        if (each_class.avg_sentiment > 0.3){
            sentiment = "Positive";
        }
        else if (each_class.avg_sentiment < -0.3){
            sentiment = "Negative";
        }
        else{
            sentiment = "Channel Empty";
        }
        const row = document.createElement('tr');
        var timestamp = new Date(parseFloat(each_class.last_read) * 1000);
        row.innerHTML = `
        <td><a href="/course?name=${each_class.name}">${each_class.name}</a></td>
        <td>${sentiment}</td>
        <td>${each_class.avg_sentiment}</td>
        <td>${timestamp}</td>
        `;
        tableBody.appendChild(row);
    }
    populateCharts(raw_data);
}

async function populateCharts(courses) {
    if (!courses){
        // empty list
        return
    }
    courses.sort((a,b) => b.num_messages -  a.num_messages)
    const max_messages = courses[0].num_messages
    console.log(max_messages)
    const container = document.getElementById('charts');
    courses.forEach(function(course, index, array){
        if (!course.num_messages){
            return
        }
        const node = document.createElement("div")
        const canvas = document.createElement("canvas")
        node.appendChild(canvas)
        const height = `${10 + 30 * Math.sqrt(course.num_messages / max_messages)}vh`
        node.style.height = height
        node.style.width = height
        console.log(node.style.height)
        container.appendChild(node)
        const chart = new Chart(canvas, {
            type: 'pie',
            data: {
                labels: ['Positive', 'Negative', 'Neutral'],
                datasets: [{
                    label: '# of Messages',
                    data: [course.num_positive, course.num_negative, course.num_messages - course.num_positive - course.num_negative],
                    borderWidth: 1,
                    backgroundColor: ["#22aa22", '#aa2222', '#888888']
                }]
            },
            options: {
                animation: false,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: course.name
                    },
                    legend: {
                        display: false,
                    }
                },
                onClick: (events, elements, chart) => {
                    window.location.href = `/course?name=${course.name}`
                }
            }
        });
    })
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
