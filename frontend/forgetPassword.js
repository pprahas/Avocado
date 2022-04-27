const element = document.getElementById("submit_button");
element.addEventListener("click", myFunction);

function myFunction(e) {
  e.preventDefault();
  let user_email = document.getElementById("user_id").value;

  fetch("https://8307zzf0x2.execute-api.us-east-1.amazonaws.com/default/user-forgot_password",
  {
      method: "POST",
      body: JSON.stringify({user_email: user_email})
  })
  .then((res) => res.json())
  .then((data) => {
      console.log(data);

      if (data.status === 200) {
          localStorage.setItem('user_email', user_email);
          window.location = 'resetPassword.html';
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