let promptList1 = ['우울', '초조', '산만', '행복', '불안'];
let promptList2 = ['깊은휴식', '피곤함극복', '우울감극복', '신나고싶음'];
let tmpList = []
let tmpList2;

let loginSessionObjectId = session['_id'];

let tmpRegenerateText = "";

let findHistory = "";

$("#img1").hide();
$("#img2").hide();
$("#img3").hide();

$("#promp1").hide();
$("#form2").hide();
$("#chat1").hide();
$("#btnHideShow").hide();

makeCheckbox1();
makeCheckbox2();

function reGenerate(){
    POSTJSON2();
}

function onSubmitCheckbox(){
    var checkboxes = document.getElementsByName("checkValue");
    for(var i = 0; i< checkboxes.length; i++){
        if(checkboxes[i].checked){
            tmpList.push(checkboxes[i].value);
        }
    }

    $("#img1").show();
    $("#promp1").show();
    

    $("#form2").show();
    $("#img2").show();
    $("#submit1").hide();
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
    $("#submit2").hide();
    POSTJSON();

    //create history
    
    return false;
}

function POSTJSON(){

    showLoading();

    var tmp = {
        'user_status': tmpList,
        'user_goal': tmpList2
    };
    
    $("#chat1").show();
    $("#img3").show();
    $.ajax({
        type: 'POST',
        url: window.location.href,
        contentType: 'application/json',
        data: JSON.stringify(tmp),
        dataType: 'json',
        success: function (response) {
            let msg = response['message'];
            document.getElementById('chat1').innerHTML = msg;
            $("#btnHideShow").show();

            createHistory();
        },
        complete: function(){
            hideLoading();
        }
    });
}

function POSTJSON2(){

    showLoading();

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

            tmpRegenerateText = `<img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" alt="" id="img1"/>
            <p>${msg}</p>`;

            //AJAX요청이 성공하면 list에 항목 추가
            $("#sentUl").append("<li class=\"sent\">" + tmpRegenerateText + "</li>");
        },
        complete: function(){
            hideLoading();
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
    <input type="submit" value="Submit" id="submit1">
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
    <input type="submit" value="Submit" id="submit2">
    </form>
    `;

    document.getElementById('form2').innerHTML = tmpHtml2;
}

//어떤 히스토리든 클릭하면 현재 대화상태를 싹 밀어버림.
function clearChat(){
    
}

//메인채팅으로 이동
$("#contact1").click(function(){
    window.location.href = window.location.href;
    
})
//백엔드에 HistoryData 호출
function callHistoryData(){

    showLoading();

    var splitString = document.getElementById(findHistory).split(',');
    var user_goalVariable = splitString[splitString.length-1];
    splitString.pop();
    var user_statusList = splitString;

    var tmp = {
        'user_status': user_statusList,
        'user_goal': user_goalVariable
    };

    var postUrl = "/main/" + loginSessionObjectId;

    $.ajax({
        type: 'POST',
        url: postUrl,
        contentType: 'application/json',
        data: JSON.stringify(tmp),
        dataType: 'json',
        success: function (response) {
            let msg = response['message'];

        },
        complete: function(){
            hideLoading();
        }
    })
}

//히스토리를 클릭하면 그 히스토리로 이동.
function openHistory(){
    window.location.href = window.location.href;
}


//두 번째 버튼을 누르면 히스토리가 생성됨(좌측)
function createHistory(){
    var tmpContent = "";
    
    for(var i = 0; i<tmpList.length; i++){
        tmpContent += tmpList[i] + ",";
    }
    tmpContent += tmpList2;
    findHistory = tmpContent;
    var chatTmp = document.getElementById('chat1').textContent.length;
    var chatAll = document.getElementById('chat1').textContent;

    var tmpDetail = pTagTextNumber(chatTmp, chatAll);

    var tmpHistory = `
    <div class="wrap">
      <span class="contact-status online"></span>
      <img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" alt="" />
      <div class="meta">
        <p class="name" id="${tmpContent}">${tmpContent}</p>
        <p class="preview">${tmpDetail}</p>
      </div>
    </div>
  </li>`
    $("#ulAppend").append("<li class=\"contact active\">" + tmpHistory + "</li>");
}

function pTagTextNumber(chat, chatAll){
    //ai의 text가 15를 넘어가면 생략하여 넣어줌.
    if(chat > 15){
        chatAll = chatAll.substring(0, 15) + '...';
    }
    return chatAll;
}


//모달 로딩애니메이션
function showLoading() {
    $("#loading").show();
  }
  
  function hideLoading() {
    $("#loading").hide();
  }
