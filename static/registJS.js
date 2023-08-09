let passwordRegister = document.getElementById('pwd_give');
let passwordRegisterRepeat = document.getElementById('pwd_repeat');
let elMismatchmessage = document.querySelector('.mismatch-message')

//회원가입. ajax POST통신이 원활하게 되면 로그인화면으로 redirect.
//ajax POST통신이 원활하지않다면 alert


// password, password 확인 값 틀리면 alert
document.getElementById('registerForm').addEventListener('submit', function(e) {
    if(!isMatch(passwordRegister.value, passwordRegisterRepeat.value)){
        swal("회원가입 실패", 'Password Mismatch !!!', 'warning');
        e.preventDefault();
    }else{
        registerMember();
    }
})

//두 값이 맞는지 판별하는 함수
function isMatch (password1, password2) {
    if ( password1 === password2 ) {
      return true;
    }
    else {
      return false;
    }
}
