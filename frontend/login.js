const element = document.getElementById("submit_button");
element.addEventListener("click", myFunction);

function myFunction(e) {
  e.preventDefault();
  let user_id = document.getElementById("user_id").value;
  let password = document.getElementById("password").value;

  fetch("https://9udp7kgai1.execute-api.us-east-1.amazonaws.com/default/user-login",
  {
      headers: {
      //   // 'Accept': 'application/json, text/plain, */*',
        'Content-type': 'application/json'
      },
      method: "POST",
      body: JSON.stringify({user_id: user_id, user_password: password})
  })
  .then(function(res){ console.log(res) })
  .catch(function(res){ console.log(res) })
}
