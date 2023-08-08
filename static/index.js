
// password, password 확인 값 틀리면 alert
let passwordRegister = document.getElementById('pwd_give');
let passwordRegisterRepeat = document.getElementById('pwd_repeat');

let elMismatchmessage = document.querySelector('.mismatch-message')


passwordRegisterRepeat.onkeyup = function () {
    if ( isMatch(passwordRegister.value, passwordRegisterRepeat.value) ) {
        elMismatchmessage.classList.add('hide')
        }
      else {
        elMismatchmessage.classList.remove('hide')
        }
    }

function isMatch (password1, password2) {
    if ( password1 === password2 ) {
      return true;
    }
    else {
      return false;
    }
    }

//json pasing
function jsonParsing(){

}