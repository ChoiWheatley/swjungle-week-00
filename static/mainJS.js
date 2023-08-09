let promptList1 = ['우울', '초조', '산만', '행복', '불안'];
let promptList2 = ['깊은휴식', '피곤함극복', '우울감극복', '신나고싶음'];
let tmpList = []
let tmpList2;

makeCheckbox1();
makeCheckbox2();


function reGenerate(){
    POSTJSON();
}

function onSubmitCheckbox(){
    var checkboxes = document.getElementsByName("checkValue");
    for(var i = 0; i< checkboxes.length; i++){
        if(checkboxes[i].checked){
            tmpList.push(checkboxes[i].value);
        }
    }
    console.log(tmpList);
    return false;
}

function onSubmitCheckbox2(){

    var selectedValue = document.querySelector('input[name="choice"]:checked');
    if(selectedValue) {
        console.log(selectedValue.value);
    }else{
        console.log("없음");
    }
    tmpList2 = selectedValue.value;

    POSTJSON();
    //user_status 값 저장, user_goal 저장 후 서버측(chatbot)에 POST요청

    return false;
}

function POSTJSON(){
    var tmp = {
        'user_status': tmpList,
        'user_goal': tmpList2
    };
    
    
    $.ajax({
        type: 'POST',
        url: window.location.href,
        contentType: 'application/json',
        data: JSON.stringify(tmp),
        dataType: 'json',
        success: function (response) {
            let msg = response['message'];
            document.getElementById('chat1').innerHTML = msg;
            
        }
    });
}


function makeCheckbox1(){
    var tmp = "";
    for(var i =0; i<promptList1.length; i++){
        tmp += `<input type="checkbox" name="checkValue" value="${promptList1[i]}">${promptList1[i]}<br>`;
    }

    let tmpHtml1 = 
    `<form id="myForm" method="POST" onsubmit="return onSubmitCheckbox();">` +
    tmp
    +
    `
    <input type="submit" value="Submit">
    </form>
    `;
    document.getElementById('form1').innerHTML = tmpHtml1;
}

function makeCheckbox2(){
    var tmp = "";
    for(var i =0; i<promptList2.length; i++){
        tmp += `<input type="radio" name="choice" value="${promptList2[i]}">${promptList2[i]}<br> <label for="${promptList2[i]}"></label>
        `;
    }

    let tmpHtml2 = 
    `<form id="myForm2" method="POST" onsubmit="return onSubmitCheckbox2();">` +
    tmp
    +
    `
    <input type="submit" value="Submit">
    </form>
    `;

    document.getElementById('form2').innerHTML = tmpHtml2;
}
