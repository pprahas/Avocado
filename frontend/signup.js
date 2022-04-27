
const ele = document.getElementById("submitbutton");

ele.addEventListener('click', signup);

function signup(e) {
    e.preventDefault();

    let name = document.getElementById('name').value;
    let email = document.getElementById('email').value;
    let birthday = document.getElementById('birthday').value;
    let password = document.getElementById('password').value;
    let confirmPassword = document.getElementById('confirmPassword').value;
    
    let data = {
        name: name,
        email: email,
        birthday: birthday,
        password: password,
        confirm_password: confirmPassword
    }
    fetch('https://n71zqssqee.execute-api.us-east-1.amazonaws.com/default/user-register', {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data);

        if (data.status === 200) {
            localStorage.setItem('user_email', email);
            window.location = ("index.html");
        } else if (data.status === 422) {
            let errors = data.body;
            let output = "";
            errors.forEach(element => {
                output += `
                <div class="error_signup">
                    <li>${element}</li>
                </div>
                `
            });
            document.getElementById('errors').innerHTML = output;
        }
    })
}