
console.log(localStorage.getItem("user_email"));

const ele = document.getElementById("most_popular");

const data = {};


fetch('https://5kwlyceua3.execute-api.us-east-1.amazonaws.com/default/home-most_popular', {
    method: 'POST',
    body: JSON.stringify(data)
}).then((res) => res.json())
.then((data) => {
    // console.log(data);
    let output = "";
    data.forEach(function(restaurant) {
        // console.log(restaurant.image);
        // output += `
        // <div>
        // <p>Some</p>
        //     <img src="data:image/png;base64, ${restaurant.image}" alt="Red dot" />
        // </div>
        // `
        // output += `
        // <div class="rest_container">
        //     <a class="rest_link" href="rest_pandaexpress.html"><img class="rest_image "src="data:image/png;base64, ${restaurant.image}" alt="Red dot" /></a>
        //     ${restaurant.rest_name}
        // </div>
        // `
        output += `
        <div class="rest_container">
            <a class="rest_link" href="rest_pandaexpress.html"><img class="rest_image "src=${restaurant.image} alt="Red dot" /></a>
            ${restaurant.rest_name}
        </div>
        `

    });
    document.getElementById('most_popular').innerHTML = output;
})
