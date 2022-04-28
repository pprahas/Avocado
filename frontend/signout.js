const element = document.getElementById("delete_account_button");
element.addEventListener("click", myFunction);

function deleteAccount(a){
  a.preventDefault();
  let user_email = document.getElementById("user_id").value;

  fetch("https://3a5aeuk5d7.execute-api.us-east-1.amazonaws.com/default/user-delete_account",
  {
      method: "POST",
      body: JSON.stringify({user_email: user_email})
  })
  .then((res) => res.json())
  .then((data) => {
      console.log(data);

      if (data.status === 200) {
          localStorage.setItem('user_email', user_email);
          window.location = 'changePassword.html';
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

function changePassword(a){

    console.log("PASSWORD CHANGE PAGE");
    localStorage.clear();
    window.location = 'changePassword.html';

}

function signout(){
  console.log("SIGN OUT");
  localStorage.clear();
  window.location = 'index.html';
}
