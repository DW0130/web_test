// window.addEventListener('DOMContentLoaded', function() { 
//     document.getElementById("btn").addEventListener('click',hello);

//     function hello(){
//         var a = document.getElementById("in").value
//         var b = document.getElementById("in_1").value
//         var c = Number(a) + Number(b)
//         document.getElementById("in_2").value = c
//       alert(c);
//     }
// })



function search(id, pw){

    var ID = id
    var PW = pw

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/testpost", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        ID : id,
        PW : pw

    }));
    xhr.onload = function() {
    var data = JSON.parse(this.responseText)
    console.log(data);


    }

}


function login(){
    var id = document.getElementById('ID').value
    var pw = document.getElementById('PW').value

    console.log(id)
    console.log(pw)

    search(id, pw)
}

function search_test(N_ID, N_PW){

    var ID = N_ID
    var PW = N_PW

    var xhr = new XMLHttpRequest(); // XMLHttpRequest = 서버와 상호작용
    xhr.open("POST", "/testpost_1", true); // 서버로부터 데이터 받아오기위한 객체 "open()함수를 통해 요청초기화"
    xhr.setRequestHeader('Content-Type', 'application/json'); //HTTP요청헤더 값 설정  "serRequestheader()함수설정"
    xhr.send(JSON.stringify({   // send()함수를 통해 요청전송 "setRequestHeader() 함수로 JSON이라고 설정하고, send() 함수로 서버에 보내는 데이터를 JSON 문자열변경"

        ID : N_ID,
        PW : N_PW

    }));
    xhr.onload = function() {
    var data = JSON.parse(this.responseText)
    console.log(data);


    }

}

function login_test(){
    var N_ID = document.getElementById('N_UserID').value
    var N_PW = document.getElementById('N_UserPW').value

    console.log(N_ID)
    console.log(N_PW)

    // search_test(N_ID, N_PW)


    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/dbsearch_1", true);
    xhr.setRequestHeader('Content-Type', 'application/json'); 
    xhr.send(JSON.stringify({ 

        ID : N_ID,
        PW : N_PW

    }));
    xhr.onload = function() {
    
        data = JSON.parse(this.responseText)
        
        if (data == false){
            Swal.fire(
                '로그인에 실패하였습니다.',
                '아이디 또는 비밀번호를가 일치하지 않습니다.',
                'error'
            )
        }else{
            Swal.fire(
                '로그인에 성공하였습니다.',
                'ID : ' + (data[0][0]) + ' Name: ' + (data[0][2]),
                'success'
            )
            
            var test_data = 1
            console.log(test_data)
        }
    }

}

function mail_bt(){console.log("mail_버튼눌림")}
function cafe_bt(){console.log("cafe_버튼누림")}

function blog_bt(){


}

function know_bt(){console.log("know_버튼눌림")}
function shop_bt(){console.log("shop_버튼눌림")}
function pay_bt(){console.log("pay_버튼눌림")}
function NTv_bt(){console.log("NTv_버튼눌림")}

function Sign_up(){

    var New_UserID = document.getElementById('NEW_User_ID').value
    var New_UserPW = document.getElementById('NEW_User_PW').value
    var New_UserNAME = document.getElementById('NAME').value
    var New_User_Phone = document.getElementById('Phone_Number').value

    console.log(New_UserID)
    console.log(New_UserPW)
    console.log(New_UserNAME)
    console.log(New_User_Phone)

    search_Signup(New_UserID, New_UserPW, New_UserNAME, New_User_Phone)
}

function search_Signup(New_UserID, New_UserPW, New_UserNAME, New_User_Phone){

    var New_ID = New_UserID
    var New_PW = New_UserPW
    var New_NAME = New_UserNAME
    var New_Phone = New_User_Phone

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/Signup_post_1", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({

        New_ID : New_UserID,
        New_PW : New_UserPW,
        New_NAME : New_UserNAME,
        New_Phone : New_User_Phone

    }));
    xhr.onload = function() {
    var data = JSON.parse(this.responseText)
    console.log(data);
    }

}


function Serch_User(){

    var P_Number = document.getElementById('User_Phone').value

    console.log(P_Number)

    Serch_User1(P_Number)
}



function Serch_User1(P_Number){

    var Serch_Phone = P_Number

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/Serch_User", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({

        Serch_Phone : P_Number

    }));
    xhr.onload = function() {
    var data = JSON.parse(this.responseText)
    console.log("아이디 : ",data[0][0]); // SQL파일기준
    console.log("비밀번호 : ",data[0][1]);
    console.log("이름 : ",data[0][2]);
    console.log("전화번호 : ",data[0][3]);
    }

}

function text_Update(){

    var blog_title = document.getElementById('Limiting_title_text').value
    var blog_text = document.getElementById('Limiting_text').value

    console.log(blog_title)
    console.log(blog_text)

    text_Update_1(blog_title, blog_text)
}


function text_Update_1(blog_title, blog_text){

    var Title = blog_title
    var Contents = blog_text

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/text_Update", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({

        Title : blog_title,
        Contents : blog_text

    }));
    xhr.onload = function() {
    var data = JSON.parse(this.responseText)
    console.log(data); 
    }
}


function Title_Serch(){

    var blog_title = document.getElementById('Title_Serch').value
    console.log(blog_title)

    Title_Serch_1(blog_title)
}

function Title_Serch_1(blog_title){


    var ST = blog_title

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/Serch_Title", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({

        ST : blog_title

    }));
    xhr.onload = function() {
    var data = JSON.parse(this.responseText)

    console.log(data)
    console.log("제목 : ",data[0][0]); // SQL파일기준
    console.log("내용 : ",data[0][1]);
         
    }
}