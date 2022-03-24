let user_email = localStorage.getItem("user_email");

const ele = document.getElementById("cart_list");
const submit_order = document.getElementById("submit_order");
submit_order.addEventListener('click', submitOrder());

function submitOrder(){
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
}


const data = {
    user_email: user_email
};

if (user_email == null){
  console.log("NOT LOGGED IN!");
  window.location = "login.html";
}

fetch('https://q6y9jbmbwl.execute-api.us-east-1.amazonaws.com/default/cart-list_of_items', {
    method: 'POST',
    body: JSON.stringify(data)
    }).then((res) => res.json())
    .then((data) => {
        if (data.status == 200) {
            let val = data.body;
            let output = "";

            val.forEach(function(cart) {
                output += `
                <tr class="cart-items">
                    <td id=${cart.rest_id} data-column="Restaurant">${cart.rest_name}</td>
                    <td id=${cart.food_id} data-column="Menu">${cart.food_name}</td>
                    <td data-column="Quantity">${cart.quantity}</td>
                    <td data-column="Price">$${cart.price}</td>
                    <td><button id="${cart.rest_id}+${cart.food_id}" class="delete_button">DELETE</button></td>
                </tr>
                `
            });
            document.getElementById('cart_list').innerHTML = output;
            let btn = document.getElementsByClassName('delete_button');
            for (var i = 0; i < btn.length; i++) {
                btn[i].addEventListener('click', modifyCart);
            }
        }
});

const ele2 = document.getElementById("totalPrice");

var todayDate = new Date().toISOString().slice(0, 10);
const data2 = {
    user_email: user_email,
    // date_specified: "2022-03-11"
    date_specified: String(todayDate)
};



fetch('https://bt02rinmvl.execute-api.us-east-1.amazonaws.com/default/cart-discount', {
    method: 'POST',
    body: JSON.stringify(data2)
    }).then((res) => res.json())
    .then((data) => {
        if (data.status == 200) {
            let val = data.body;
            let output = "";
            output += `
            <div>TOTAL PRICE</div>
            <div class="totalPrice">$${Number((val.total_price).toFixed(2))}</div>
            `
            document.getElementById('totalPrice').innerHTML = output;

            if (val.discount_percent != 0 && val.total_price != 0) {
                let output2 = "";
                let discounted_price = val.total_price * (val.discount_percent/ 100)
                discounted_price = Number((discounted_price).toFixed(2));
                output2 = `
                <div>${val.discount_name} discount</div>
                <div class="discountPrice">- $${discounted_price}</div>
                `
                document.getElementById('discount').innerHTML = output2;
            }

        } else {
            console.log(data.statusText);
        }
    });
