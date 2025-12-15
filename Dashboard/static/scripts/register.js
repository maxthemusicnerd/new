
const form = document.getElementById('register-form');


form.addEventListener('submit', async (e) => {
    e.preventDefault();


    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === '' || password === '') {
        alert('Please fill in both fields');
        return;
    }

    const res = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (data.success) {
        window.location.href = data.redirect;
    } else {
        alert(data.error);
    }
});



