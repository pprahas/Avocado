let user_id = localStorage.getItem("user_email");

function addToCart() {

    const data = {
        user_email: user_id,
        rest_id: rest_id,
        food_id: this.id,
    };

    fetch('https://6h77675zrl.execute-api.us-east-1.amazonaws.com/default/restaurants-add_to_cart', {
    method: 'POST',
    body: JSON.stringify(data)
    }).then((res) => res.json())
    .then((data) => {
        if (data.status === 200) {
            console.log(data.statusText);
        } else {
            console.log(data.statusText);
        }
    });

    //Update Cart Quantity when pressed!
    const quantity = document.getElementById("cart_quantity");
    let count = parseInt(quantity.innerHTML);

    count = count + 1;
    quantity.innerHTML = count;
    updateAnimation(quantity, count);
}

function updateAnimation(quantity, count){
  if (count % 2) {
    quantity.style = "background-color: #dc2f02;";
  } else {
    quantity.style = "background-color: #606c38;";
  }
}
