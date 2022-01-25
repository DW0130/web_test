
function Login(){ // 로그인
    var ID = document.getElementById('Login_ID').value
    var PW = document.getElementById('Login_PW').value

    console.log(ID)
    console.log(PW)

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/Login_DB", true);
    xhr.setRequestHeader('Content-Type', 'application/json'); 
    xhr.send(JSON.stringify({ 

        ID : document.getElementById('Login_ID').value,
        PW : document.getElementById('Login_PW').value

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
        }
    }

}

function Sign_in(){ //회원가입

    var ID = document.getElementById('New_ID').value
    var PW = document.getElementById('New_PW').value
    var Name = document.getElementById('New_Name').value
    var Phone = document.getElementById('New_Phone').value

    console.log(ID)
    console.log(PW)
    console.log(Name)
    console.log(Phone)
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/Sign_DB", true);
    xhr.setRequestHeader('Content-Type', 'application/json'); 
    xhr.send(JSON.stringify({ 

        ID : document.getElementById('New_ID').value,
        PW : document.getElementById('New_PW').value,
        Name : document.getElementById('New_Name').value,
        Phone : document.getElementById('New_Phone').value

    }));
    xhr.onload = function() {
        data = JSON.parse(this.responseText)
        console.log(data)
    }
}

function Serch_User(){ // 계정찾기

    var Name = document.getElementById('Name').value
    var Phone = document.getElementById('Phone').value

    console.log(Name)
    console.log(Phone)

    var xhr = new XMLHttpRequest()
    xhr.open("POST", "/User_DB", true)
    xhr.setRequestHeader('Content-Type','application/json')
    xhr.send(JSON.stringify({

        Name : document.getElementById('Name').value,
        Phone : document.getElementById('Phone').value

    }))
    xhr.onload = function(){
        var data = JSON.parse(this.responseText)
        console.log("아이디 : ", data[0][0])
        console.log("비밀번호 : ", data[0][1])
    }
    
}

function Notice_Board(){ //게시판 글올리기

    var Title = document.getElementById('Title').value
    var Main_Text = document.getElementById('Main_Text').value

    console.log(Title)
    console.log(Main_Text)

    var xhr = new XMLHttpRequest()
    xhr.open("POST", "/Notice_DB", true)
    xhr.setRequestHeader('Content-Type','application/json')
    xhr.send(JSON.stringify({

        Title : Title,
        Main_Text : Main_Text

    }))
    xhr.onload = function(){
        var data = JSON.parse(this.responseText)
        console.log(data)
    }
}


function Serch_Title(){ // 게시판 찾기

    var Title = document.getElementById('Title_text').value

    console.log(Title)

    var xhr = new XMLHttpRequest()
    xhr.open("POST", "/Title_DB", true)
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.send(JSON.stringify({

        Title : document.getElementById('Title_text').value
    }))
    xhr.onload = function(){
        var data = JSON.parse(this.responseText)
        console.log("제목 : ", data[0][0])
        console.log("내용 : ", data[0][1])
    }
}