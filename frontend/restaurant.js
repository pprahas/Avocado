let rest_id = localStorage.getItem('rest_id');

console.log(localStorage.getItem('rest_id'));

const ele = document.getElementById("most_popular");

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
            
            val.forEach(function(menu) {
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
            });
            
            document.getElementById('restaurant_menu').innerHTML = output;
            let btn = document.getElementsByClassName('addToCart');
            // console.log(btn);
            for (var i = 0; i < btn.length; i++) {
                btn[i].addEventListener('click', addToCart);
            }
        }
});

function addToCart() {

    console.log(this);
}