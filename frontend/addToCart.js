let user_id = localStorage.getItem("user_email");

function addToCart() {

    // console.log(this);
    // console.log(user_id);
    
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