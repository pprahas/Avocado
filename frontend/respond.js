
function clickFunc(event) {
    // sendId of the restaurant being clicked
    localStorage.setItem('rest_id', this.id)
    console.log(this.id);
}
