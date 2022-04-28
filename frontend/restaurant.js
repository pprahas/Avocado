let rest_id = localStorage.getItem('rest_id');
console.log("rest_id:", rest_id)

let user_id = localStorage.getItem("user_email");
const loading_screen = document.getElementById("loading_container");


const data = {
    rest_id: rest_id
};


fetch('https://3b01ihtpq4.execute-api.us-east-1.amazonaws.com/default/restaurants-menu', {
    method: 'POST',
    body: JSON.stringify(data)
    }).then((res) => res.json())
    .then((data) => {
        if (data.status == 200) {
            let val = data.body;
            let output = "";
            
            let pic = data.body.pic;
            let no_pic = data.body.no_pic

            let count = 0;
            for (let menu of pic) {
                if (count == 4) { break; }
                output += `
                <div id=${menu.food_id} class="menu_container">
                    <img class="menu_image" src=${menu.image} alt="">
                    <div class="menu_name">
                        ${menu.food_name}
                    </div>
                    <div class="menu_price">
                    ${menu.price}
                </div>
                    <button id=${menu.food_id} class="addToCart" type="submit">Add to Cart</button>
                </div>`
                const menu_name = document.getElementById("rest_name");
                menu_name.innerHTML = menu.rest_name;
                count += 1;
            }

            let output2 = "";
            for (let menu of no_pic) {
                output2 += `
                <tr>
                    <td>${menu.food_name}</td>
                    <td>${menu.price}</td>
                    <td>
                        <button id=${menu.food_id} class="addToCart" type="submit">Add to Cart</button>
                    </td>
                </tr>
                `
            }            

            document.getElementById('restaurant_menu').innerHTML = output;
            document.getElementById('cart_list').innerHTML = output2;

            let btn = document.getElementsByClassName('addToCart');
            // console.log(btn);
            for (var i = 0; i < btn.length; i++) {
                btn[i].addEventListener('click', addToCart);
            }
            finishLoading();
        }
});

if (user_id == null){
  console.log("NOT LOGGED IN!");
} else {
  console.log("LOGGED IN!");
  getCartQuantity();
}

function getCartQuantity(){
  const data = {
      user_email: user_id
  };

  fetch('https://bo48fcsrp9.execute-api.us-east-1.amazonaws.com/default/cart-show_quantity', {
  method: 'POST',
  body: JSON.stringify(data)
  }).then((res) => res.json())
  .then((data) => {
      if (data.status === 200) {
        let val = data.body;
        const quantity = document.getElementById("cart_quantity");
        quantity.innerHTML = val.quantity;
      } else {
          console.log(data.statusText);
      }
});
}

function finishLoading(){
  console.log("fetch complete");
  loading_screen.style.zIndex = "-100";
  loading_screen.style.opacity = "0";
}

function addToCart() {

    console.log(this);
}
