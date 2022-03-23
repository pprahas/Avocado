
// var carts = [].slice.call(document.querySelectorAll('cart_list'), 0)

// function cartItems(cart) {
//     // console.log(event.target.id);
//     console.log(carts.indexOf(cart));
// }

const element = document.getElementById("submit_order");
element.addEventListener("click", submitOrder);

function submitOrder() {
    
}


function modifyCart() {
    // console.log(this.id);
    const myArray = this.id.split("+");
    let rest_id = myArray[0];
    let food_id = myArray[1]

    fetch("https://sc2q39qq80.execute-api.us-east-1.amazonaws.com/default/cart-delete_items",
    {
        method: "POST",
        body: JSON.stringify({user_email: user_email, food_id: food_id})
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data);

        if (data.status === 200) {
            var elem = document.getElementById(String(this.id)+"+cart-items");
            elem.remove();
            displayPricing();
        } else {
            console.log(data.statusText)
        }
    })

}