const user_email = localStorage.getItem("user_email")
const account = document.getElementById("account");
const loading_screen = document.getElementById("loading_container");

if (user_email == null){
  console.log("NOT LOGGED IN!");
  account.innerHTML = 'Log-In';
} else {
  console.log("LOGGED IN!");
  account.innerHTML = user_email;
  account.href = "signout.html";
}

async function most_popular_list() {
    const ele = document.getElementById("most_popular");
    
    const data = {};
    
    fetch('https://5kwlyceua3.execute-api.us-east-1.amazonaws.com/default/home-most_popular', {
          method: 'POST',
          body: JSON.stringify(data)
      }).then((res) => res.json())
      .then((data) => {
    
          if (data.status == 200) {
              let val = data.body;
              let output = "";
              val.forEach(function(restaurant) {
                  output += `
                  <div class="rest_container">
                      <a id=${restaurant.rest_id} class="rest_link" href="restaurant.html"><img class="rest_image" src=${restaurant.image}
                       alt="Red dot" /></a>
                      ${restaurant.rest_name}
                  </div>`
              });
    
              document.getElementById('most_popular').innerHTML = output;
              let btn = document.getElementsByClassName('rest_link');
              for (var i = 0; i < btn.length; i++) {
                  btn[i].addEventListener('click', clickFunc);
              }
          }    
    
      })
}

async function order_again() {
    const ele = document.getElementById("Order Again");
    
    const data = {
        user_email: "munhong@gmail.com"
    };


    fetch('https://mso6sc71q3.execute-api.us-east-1.amazonaws.com/default/home-order_again', {
          method: 'POST',
          body: JSON.stringify(data)
      }).then((res) => res.json())
      .then((data) => {

        console.log(data)
    
          if (data.status == 200) {
              let val = data.body;
              let output = "";
              val.forEach(function(restaurant) {
                  output += `
                  <div class="rest_container">
                      <a id=${restaurant.rest_id} class="rest_link" href="restaurant.html"><img class="rest_image" src=${restaurant.image}
                       alt="Red dot" /></a>
                      ${restaurant.rest_name}
                  </div>`
              });
    
              document.getElementById("Order Again").innerHTML = output;
              let btn = document.getElementsByClassName('rest_link');
              for (var i = 0; i < btn.length; i++) {
                  btn[i].addEventListener('click', clickFunc);
              }
          }     
    })   
}


async function food_list(food_type) {
    const ele = document.getElementById(food_type);
    
    const data = {
        rest_type: food_type
    };


    fetch('https://m77sejmw7h.execute-api.us-east-1.amazonaws.com/default/home-category', {
          method: 'POST',
          body: JSON.stringify(data)
      }).then((res) => res.json())
      .then((data) => {

        console.log(data);
    
          if (data.status == 200) {
              let val = data.body;
              let output = "";
              val.forEach(function(restaurant) {
                  output += `
                  <div class="rest_container">
                      <a id=${restaurant.rest_id} class="rest_link" href="restaurant.html"><img class="rest_image" src=${restaurant.image}
                       alt="Red dot" /></a>
                      ${restaurant.rest_name}
                  </div>`
              });
    
              document.getElementById(food_type).innerHTML = output;
              let btn = document.getElementsByClassName('rest_link');
              for (var i = 0; i < btn.length; i++) {
                  btn[i].addEventListener('click', clickFunc);
              }
          }     
    })   
}

if (user_email != null) {
}
order_again();
most_popular_list();
food_list("Fast Food");
food_list("Asian");


console.log("Complete!");
loading_screen.style.zIndex = "-100";
loading_screen.style.opacity = "0";


