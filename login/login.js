const { use } = require("react");

const form = document.getElementById('login-form');


form.addEventListener('submit', (e) => {
    e.preventDefault();


    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === '' || password === '') {
        alert('Please fill in both fields');
        return;
    }

    check_database(username, password)
});

function check_database(username, password) {
    console.log(`Username: ${username}, Password: ${password}`);

    //fill in with logic to check if username and password is in DB

    //if match send them to the dashboard with their username in the corner

    //if not, say not in system
}