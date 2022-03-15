const element = document.getElementById("submit_button");
element.addEventListener("click", myFunction);

function myFunction(e) {
  e.preventDefault();
  let user_email = document.getElementById("user_id").value;
  let password = document.getElementById("password").value;

  fetch("https://9udp7kgai1.execute-api.us-east-1.amazonaws.com/default/user-login",
  {
      method: "POST",
      body: JSON.stringify({user_email: user_email, user_password: password})
  })
  .then((res) => res.json())
  .then((data) => {
      console.log(data);

      if (data.status === 200) {
          localStorage.setItem('user_email', user_email);
          window.location = 'index.html';
      } else if (data.status === 422) {
          let errors = data.body;
          let output = "";
          output += `
          <div class="error_signup">
              <li>${data.statusText}</li>
          </div>
          `
          document.getElementById('errors').innerHTML = output;
      }
  })
}
