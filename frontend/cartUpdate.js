
// var carts = [].slice.call(document.querySelectorAll('cart_list'), 0)

// function cartItems(cart) {
//     // console.log(event.target.id);
//     console.log(carts.indexOf(cart));
// }

function modifyCart() {
    console.log(this.id);
    const myArray = this.id.split("+");
    let rest_id = myArray[0];
    let food_id = myArray[1]

    // console.log(rest_id, food_id);
}