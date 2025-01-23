document.getElementById("login-btn").addEventListener("click", () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (email && password) {
        alert(`Welcome back, ${email}!`);
    } else {
        alert("Please fill in all fields!");
    }
});

document.getElementById("signup-btn").addEventListener("click", () => {
    alert("Sign-up functionality coming soon!");
});
