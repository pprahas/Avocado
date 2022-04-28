const form = document.getElementById('form');
form.addEventListener('submit', gotoRest);

function gotoRest() {
  /* this function returns the user input restaurant.
  Get rest_id of the searched restuarnt, set localStorage,
  and go to rest.html */

  var input_restaurant = document.getElementById('myInput').value;

  console.log(input_restaurant);

  fetch("https://jz07hxy2zb.execute-api.us-east-1.amazonaws.com/default/home-search",
  {
      method: "POST",
      body: JSON.stringify({search_key: inp.value})
  })
  .then((res) => res.json())
  .then((data) => {
      // console.log(data);
  
      if (data.status === 200) {
          let data_list = data.body;
          localStorage.setItem("rest_id" , data_list[0].rest_id);
          window.location = "restaurant.html";
      }
  });
}


var search_key = document.getElementById("myInput").value;

autocomplete(document.getElementById("myInput"));

function autocomplete(inp) {
    
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
    
    let arr = [];
    let rest_id_list = [];
    console.log("search_key", inp.value)

    fetch("https://jz07hxy2zb.execute-api.us-east-1.amazonaws.com/default/home-search",
      {
          method: "POST",
          body: JSON.stringify({search_key: inp.value})
      })
      .then((res) => res.json())
      .then((data) => {
          // console.log(data);
      
          if (data.status === 200) {
              let data_list = data.body;
              // console.log(data_list);
      
              for (let rest_info of data_list) {
                // arr.push(JSON.stringify(rest_info))
                arr.push(String(rest_info.rest_name))
                rest_id_list.push(rest_info.rest_id)
              }

              // console.log(arr);

              var a, b, i, search_key = this.value;
              /*close any already open lists of autocompleted values*/
              closeAllLists();
              if (!search_key) { return false;}
              currentFocus = -1;
              /*create a DIV element that will contain the items (values):*/
              a = document.createElement("DIV");
              a.setAttribute("id", this.id + "autocomplete-list");
              a.setAttribute("class", "autocomplete-items");
              /*append the DIV element as a child of the autocomplete container:*/
              this.parentNode.appendChild(a);
              /*for each item in the array...*/
              if (arr.length) {
                for (i = 0; i < arr.length; i++) {
  
                  let indexOfMatch = arr[i].toLowerCase().indexOf(search_key.toLowerCase());
  
                  /*check if the item starts with the same letters as the text field value:*/
                  if (indexOfMatch != -1) {
                    /*create a DIV element for each matching element:*/
                    b = document.createElement("DIV");
                    b.setAttribute("id", rest_id_list[i]);
                    b.setAttribute("class", "rest_link");
                    b.setAttribute("onclick", "location.href='restaurant.html';");
  
                    wordMatch = `
                      ${arr[i].substr(0 ,indexOfMatch)}<strong>${arr[i].substr(indexOfMatch, search_key.length)}</strong>${arr[i].substr(indexOfMatch + (search_key.length), arr[i].length)}
                    `
                    output = `
                      <a id=${rest_id_list[i]} class="rest_link" href="restaurant.html">${wordMatch}
                      </a>
                    `
                    b.innerHTML += output
  
                    /*insert a input field that will hold the current array item's value:*/
                    b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                    // console.log("here: " + arr[i]);
                    b.addEventListener("click", function(e) {
                      /*insert the value for the autocomplete text field:*/
                      inp.value = this.getElementsByTagName("input")[0].value;
                      /*close the list of autocompleted values,
                      (or any other open lists of autocompleted values:*/
                      closeAllLists();
                    });
                    /*execute a function when someone clicks on the item value (DIV element):*/
                    a.appendChild(b);
                  }
                }
              } else {
                // add if no search result
                
              }

              let btn = document.getElementsByClassName('rest_link');
              for (var i = 0; i < btn.length; i++) {
                btn[i].addEventListener('click', clickFunc);
                
              }
              
          } else if (data.status === 422) {
          }
      })

  });

  function clickFunc() {
    localStorage.setItem('rest_id', this.id)
    console.log(this.id);
  }

  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
}
