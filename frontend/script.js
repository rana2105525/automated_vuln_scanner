document.getElementById('scanForm').addEventListener('submit', function(e) {
    e.preventDefault();

    let url = document.getElementById('url').value.trim();
    if (url === "") {
        alert("Please enter a URL.");
        return;
    }

    // Show loading text while scanning
    document.getElementById('loading').style.display = 'block';
    document.getElementById('report').style.display = 'none';

    // Send the scan request to the backend
    fetch('http://127.0.0.1:5000/scan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading and show results
        document.getElementById('loading').style.display = 'none';
        document.getElementById('report').style.display = 'block';

        let resultsContainer = document.getElementById('scanResults');
        resultsContainer.innerHTML = ''; // Clear previous results

        data.forEach(entry => {
            let entryDiv = document.createElement('div');
            entryDiv.classList.add('result-entry');

            let entryTitle = document.createElement('h3');
            entryTitle.textContent = entry.url;
            entryDiv.appendChild(entryTitle);

            entry.results.forEach(result => {
                let resultDiv = document.createElement('p');
                resultDiv.textContent = `${result.type}: ${result.status}`;
                entryDiv.appendChild(resultDiv);
            });

            resultsContainer.appendChild(entryDiv);
        });
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none';
        alert('An error occurred during the scan.');
    });
});
