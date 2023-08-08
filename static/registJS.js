let passwordRegister = document.getElementById('pwd_give');
let passwordRegisterRepeat = document.getElementById('pwd_repeat');
let elMismatchmessage = document.querySelector('.mismatch-message')

//회원가입. ajax POST통신이 원활하게 되면 로그인화면으로 redirect.
//ajax POST통신이 원활하지않다면 alert
function registerMember(){
    let userId = document.getElementById('id_give').val();
    let userPassword = document.getElementById('pwd_give').val();

    $.ajax({
        type: "POST",
        url: "/register",
        data: { userId: userId, userPw: userPassword },
        success: function(response){
            if(response.success){
                window.location.href = '/'
            }else{
                alert('데이터 저장 실패 or 뭔가 오류가 생김.');
            }
        },
        //에러 발생시 함수
        error: function(){
            alert('에러발생')
        }
    })

    
}

// password, password 확인 값 틀리면 alert
document.getElementById('registerForm').addEventListener('submit', function(e) {
    if(!isMatch(passwordRegister.value, passwordRegisterRepeat.value)){
        alert('Password Mismatch!!');
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
