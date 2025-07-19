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
            targetSection.style.display = 'flex';
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
        camerasSection.style.display = 'flex';
    }
});

// ======================== Input Data Functions ========================

// ======================== Output Data Functions ========================

// ======================== Sonar Data Functions ========================

// ======================== Battery Data Functions ========================

// ======================== IMU Data Functions ========================

// ======================== Sensor Data Functions ========================

// ======================== Data Log Functions ========================