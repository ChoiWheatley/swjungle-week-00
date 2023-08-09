let promptList1 = ['우울', '초조', '산만', '행복', '불안'];
let promptList2 = ['깊은휴식', '피곤함극복', '우울감극복', '신나고싶음'];
let tmpList = []
let tmpList2;

let loginSessionObjectId = sessionStorage.getItem("user_id");

let tmpRegenerateText = "";

let findHistory = "";

let gSession = {
    chatId: null,

    setChatId: function(id) {
        this.chatId = id;
    },
};

let $messages = document.querySelector(".messages");
let $sentUl = document.querySelector("#sentUl");


window.onload = function() {

    callHistoryData();

};

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
        // console.log(selectedValue.value);
    }else{
        // console.log("없음");
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
            let msg = response['ai_response'];
            document.getElementById('chat1').innerHTML = msg;
            $("#btnHideShow").show();

            createHistory(response);
            callHistoryData();
            gSession.setChatId(response["_id"]);
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
        url: "/api/chat/" + gSession.chatId,
        contentType: 'application/json',
        data: JSON.stringify(tmp),
        dataType: 'json',
        success: function (response) {
            let msg = response['ai_response'].at(-1);

            tmpRegenerateText = `<img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" alt="" id="img1"/>
            <p>${msg}</p>`;

            //AJAX요청이 성공하면 list에 항목 추가
            // createSentLiElement($sentUl, tmpRegenerateText);
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
    document.querySelectorAll(".replies").forEach((elem) => {
        elem.remove()
    });
    document.querySelectorAll(".sent").forEach((elem) => {
        elem.remove()
    });
}

//메인채팅으로 이동
$("#contact1").click(function(){
    window.location.href = window.location.href;
    
})
//백엔드에 HistoryData 호출
function callHistoryData(){

    var postUrl = "/api/history/" + loginSessionObjectId;

    $.ajax({
        type: 'GET',
        url: postUrl,
        contentType: 'application/json',
        success: function (responses) {
            for (let response of responses) {
                createHistory(response);
            }
        },
        complete: () => {
            hideLoading();
        }
    })
    .done((data) => {
        // console.log(data);
        document.querySelectorAll("[type=history]").forEach((elem) => {

            elem.addEventListener("click", (e) => {
                /**
                 * 
                */
                gSession.setChatId(elem.getAttribute("id"));
                clearChat();
                $.ajax({
                    type: "GET",
                    url: "/api/chat/" + elem.id,
                    contentType: "application/json",
                    success: (chat) => {
                        $sentUl.innerHTML = `
          <li class="sent">
            <img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" alt="" />
            <p>현재 상태를 모두 체크해 주세요.</p>
          </li>
          <li class="replies">
            <img src="https://velog.velcdn.com/images/doyolee/post/8ad37313-2695-4a32-af27-af51d50f7387/image.png" alt="" />
            <p id ="form1"></p>
          </li>

          <li class="sent">
            <img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" alt="" id="img1"/>
            <p id="promp1">이루고자 하는 목표는 무엇인가요?</p>
          </li>

          <li class="replies">
            <img src="https://velog.velcdn.com/images/doyolee/post/8ad37313-2695-4a32-af27-af51d50f7387/image.png" alt="" id="img2"/>
            <p id ="form2"></p>
          </li>
                        `;
                        makeCheckbox1();
                        makeCheckbox2();

                        for (let stat of chat.user_status) {
                            document.querySelector(`[value=${stat}]`).checked = true;
                        }

                        document.querySelector(`[value=${chat.user_goal}]`).checked = true;

                        for (let ai_response of chat.ai_response) {
                            createSentLiElement($sentUl, ai_response);
                        }
                    },
                    complete: () => {
                        hideLoading();
                        $("#btnHideShow").show();
                    }
                })
            });
        });
    })
}

function createSentLiElement(parentNode, innerText) {
    const $li = document.createElement("li");
    $li.className = "sent";
    $li.innerHTML = `
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" alt="">
    <p>${innerText}</p>
    `;
    // TODO - 이것저거 추가하기
    parentNode.appendChild($li);
}

//히스토리를 클릭하면 그 히스토리로 이동.
function openHistory(){

}


//두 번째 버튼을 누르면 히스토리가 생성됨(좌측)
function createHistory(chat){
    var tmpContent = "";
    var tmpDetail = "";

    for (let user_status of chat.user_status) {
        tmpContent += user_status + ",";
    }
    findHistory = tmpContent;

    tmpDetail = chat.user_goal

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
    $("#ulAppend").append(`<li type='history' class=\"contact active\" id='${chat._id}'>` + tmpHistory + "</li>");
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
