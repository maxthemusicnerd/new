
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

async function check_database(username, password) {
    const res = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (data.success) {
        window.location.href = data.redirect;
    } else {
        alert("Invalid username or password");
    }
}