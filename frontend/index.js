
const ele = document.getElementById("most_popular");

const data = {};

fetch('https://5kwlyceua3.execute-api.us-east-1.amazonaws.com/default/home-most_popular', {
    method: 'POST',
    body: JSON.stringify(data)
}).then((res) => res.json())
.then((data) => {
    console.log(data);
})
