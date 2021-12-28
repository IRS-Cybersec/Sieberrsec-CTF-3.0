import * as wasm from "wasm-game-of-life";

let hide;
function check_flag() {
    let flag = document.getElementById('flag');
    let result = document.getElementById('result');
    
    clearTimeout(hide);
    result.textContent = wasm.check_flag(flag.value) ?
        'Correct!' : 'Wrong.';
    hide = setTimeout(() => { result.textContent = ''; }, 500);

}

document.getElementById('flag').onkeydown = e => {
       if (e.keyCode == 13) {
           e.preventDefault();
           check_flag();
       }
}
document.getElementById('button').onclick = check_flag;
