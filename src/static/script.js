document.getElementById('inputs-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    fetch('/inputs', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('inputs-output').textContent = JSON.stringify(data, null, 2);
        });
});

async function loadInputsData() {
    try {
        const res = await fetch('http://localhost:5000/data');
        const rows = await res.json();

        const tbody = document.querySelector('#data-table tbody');
        tbody.innerHTML = ''; // Clear any existing rows

        rows.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
            <td>${row.id}</td>
            <td>${row.name}</td>
            <td>${row.value}</td>
          `;
            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error('Failed to load table data:', err);
    }
}

async function sendInputs(formElement) {
    const formData = new FormData(formElement);
    // Ensure checkbox value is sent as boolean
    const isActive = formElement.querySelector('#is_active').checked;
    formData.set('is_active', isActive);

    try {
        const response = await fetch('/inputs', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        document.getElementById('inputs-output').textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error('Error sending inputs:', error);
    }
}

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        // Hide all containers
        document.querySelectorAll('.container').forEach(section => {
            section.style.display = 'none';
        });
        // Show the selected container
        const targetId = this.getAttribute('data-target');
        const targetSection = document.getElementById(targetId);
        if (targetSection) {
            targetSection.style.display = 'block';
            // Optionally trigger data load for specific containers
            if (targetId === 'data-table-container') {
                loadInputsData();
            }
        }
    });
});

// Set "cameras" as default visible container on page load
window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.container').forEach(section => {
        section.style.display = 'none';
    });
    const camerasSection = document.getElementById('cameras');
    if (camerasSection) {
        camerasSection.style.display = 'block';
    }
});

setInterval(updateVideoSources, 5000);
updateVideoSources();
