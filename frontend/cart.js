let user_email = localStorage.getItem("user_email");

if (user_id == null){
  console.log("NOT LOGGED IN!");
  window.location = "login.html";
}

const ele = document.getElementById("cart_list");

const data = {
    user_email: user_email
};

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
const data2 = {
    user_email: user_email,
    date_specified: "2022-03-11"
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
            <div class="totalPrice">$${val.total_price}</div>
            `
            document.getElementById('totalPrice').innerHTML = output;
        } else {
            console.log(data.statusText);
        }
    });
