let hide;
function check_flag() {
    let flag = document.getElementById('flag');
    let result = document.getElementById('result');
    
    clearTimeout(hide);
    result.textContent = btoa(flag.value) === "SVJTe2luc3AzY3RfZTFlbWVudH0=" ?
        'Correct!' : 'Wrong.';
    hide = setTimeout(() => { result.textContent = ''; }, 500);

}

document.getElementById('flag').onkeydown = e => {
       if (e.keyCode == 13) {
           e.preventDefault();
           check_flag();
       }
}
