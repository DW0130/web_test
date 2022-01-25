#This is a python
from flask import Flask,render_template,request,send_file,redirect,session,flash

from werkzeug import secure_filename
import os,sys
import time
import hashlib
import pymysql
import threading
import openpyxl
import statistics
from openpyxl import Workbook, drawing 

DELETE = "rm -f /home/pi/Desktop/Dnet_WEB_/Dnet_Photo-management/Web_server2"
str2 = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'

import json

app = Flask(__name__,template_folder='templates')
app.secret_key = 'asdf'
app.config["SECRET_KEY"] = "ABCD"


def shutdown_server():
    
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

# 화면 슬라이스 생성

@app.route("/") # 프로그램 시작시 먼저 실행
def main():
    return render_template('test_login.html')

@app.route("/test_Sign") # 회원가입
def test_Sign():
    return render_template('test_Sign.html')
    
@app.route("/test_Serch_User") # 계정찾기
def test_Serch_User():
    return render_template('test_Serch_User.html')

@app.route("/test_writing") # 계정찾기
def test_writing():
    return render_template('test_writing.html')

'''
@app.route("/") # 프로그램 시작시 먼저 실행
def main():
    return render_template('login_Before.html')

@app.route("/sign_up") #회원가입화면
def sign_up():
    return render_template('sign_up.html')

@app.route("/login_Before") #메인화면
def login_Before():
    return render_template('login_Before.html')

@app.route("/Serch_ID") #ID찾기
def Serch_ID():
    return render_template('Serch_ID.html')

@app.route("/Serch_PW") #PW찾기
def Serch_PW():
    return render_template('Serch_PW.html')

@app.route("/blog") #blog화면
def blog():
    return render_template('blog.html')
    
@app.route("/login_after") #blog화면
def login_after():
    return render_template('login_after.html')
'''

'''
@app.route("/popup")
def popup():
    return render_template('popup.html')

@app.route("/idd",methods=['POST'])
def idd():
    id=""
    if request.method == 'POST':
        id = request.form.get('id')
   
    session['iddd'] = id
    return ('', 204)

@app.route("/edit",methods=['POST'])
def editspeed():
    ed=""
    if request.method == 'POST':
        ed = request.form.get('ed')
    print(ed)
    fn = session['iddd']
    print(fn)
    f = open("/home/pi/Desktop/Dnet_Photo_New/static/speeddata/speedlimit_"+fn+".txt", 'w')   
    f.write(ed)
    f.close()
    return ('', 204)

@app.route("/list")
def listmain():
    if (session.get('login')) :
        return render_template('listmain.html')
    else :
        flash("로그인이 필요합니다")
        return redirect('/')

@app.route("/analysis")
def analysis():
    if (session.get('login')) :
        return render_template('analysis.html')
    else :
        flash("로그인이 필요합니다")
        return redirect('/')

@app.route("/p2",methods=['POST'])
def realmain():
    num=""
    num2=""
    if request.method == 'POST':
        num = request.form.get('num')
        num2 = request.form.get('num2')
        result = hashlib.sha256(num2.encode()).hexdigest()
        if (num == "dnet" and num2 == "admin") or (num =='a' and result == str2):
            session['login'] = 1
            return redirect('/list')
        else:
            flash("아이디 또는 비밀번호가 일치하지 않습니다")
            return render_template('login.html')

@app.route("/re",methods=['POST'])
def remove():
    if request.method == 'POST':
        a = request.form.get('url')
        DELETE_ORDER = DELETE + a
        print(DELETE_ORDER)
        os.system(DELETE_ORDER)
    return redirect('/list')

@app.route("/searchDB",methods=['POST'])
def searchDB():
    if request.method == 'POST':
        i = request.get_json()
        
        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='speeddb',charset='utf8')  
        sql = DB.cursor()
        sql.execute("select LCT,SPD,TME,PHT from speeddb.CarDB where TME between '"+i.get('startdate')+"' and '"+i.get('enddate')+"' AND SPD >"+i.get('lim')+" AND LCT ='"+i.get('location')+"' ORDER BY TME DESC")
        data = json.dumps(sql.fetchall(),default=str)
        return data

@app.route("/searchDBAn",methods=['POST'])
def searchDBAn():
    if request.method == 'POST':
        i = request.get_json()
        
        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='speeddb',charset='utf8')  
        sql = DB.cursor()
        sql.execute("select LCT,SPD,HOUR(TME) from speeddb.CarDB where TME between '"+i.get('startdate')+"' and '"+i.get('enddate')+"' AND SPD >"+i.get('lim')+" ORDER BY TME DESC")
        data = json.dumps(sql.fetchall(),default=str)
        return data

@app.route("/excelexport",methods=['POST'])
def excelexport():
    if request.method == 'POST':
        i = request.get_json()
        

        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='speeddb',charset='utf8')  
        try:
            with DB.cursor() as curs:
                sql = "select SPD,TME from speeddb.CarDB where TME between '"+i.get('startdate')+"' and '"+i.get('enddate')+"' AND SPD >"+i.get('lim')+" AND LCT ='"+i.get('location')+"' ORDER BY TME DESC"

                sql2 = "select PHT from speeddb.CarDB where TME between '"+i.get('startdate')+"' and '"+i.get('enddate')+"' AND SPD >"+i.get('lim')+" AND LCT ='"+i.get('location')+"' ORDER BY TME DESC"

                curs2 = DB.cursor()

                curs.execute(sql)
                curs2.execute(sql2)
                rs = curs.fetchall()
                rs2 = curs2.fetchall()

                wb = Workbook()
                ws = wb.active

                #첫행 입력
                ws.append(('번호','이름','d','d'))

                #DB 모든 데이터 엑셀로
                index = 2
                for row in rs:
                    ws.append(row)
                    data4 = rs2[index-2][0]
                    img = openpyxl.drawing.image.Image(data4)
                    img.height = 305.5
                    img.width= 405.5
                    a = 'D'+str(index)
                    ws.add_image(img,a)
                    print("index")
                    print(a)
                    index = index+1
                wb.save("/home/pi/Desktop/Dnet_Photo_New/static/exli.xlsx")
        finally:
            DB.close()
            wb.close()
        return '', 204
'''

'''
@app.route("/testpost",methods=['POST'])
def testpost(): #연습용Post
    Realid = 1234
    Realpw = 5678
    if request.method == 'POST':
        i = request.get_json()
        recvdata = i.get('numder')
        Realid = i.get('ID')
        Realpw = i.get('PW')

        if Realid == '1234' and Realpw == '5678':
            return json.dumps("{'data' : 로그인 되었습니다.}")
        else:
            return json.dumps("{'data' : 비닐번호가 틀렸습니다.}")
       
newid = ''
newpw = ''
@app.route("/Signup_post",methods=['POST']) #회원가입POST
def Signup_post(): #연습용Post
    global newid
    global newpw

    if request.method == 'POST':
        i = request.get_json()
        newid = i.get('New_ID')
        newpw = i.get('New_PW')
        newname = i.get('New_NAME')
        newphone = i.get('New_Phone')
        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='test',charset='utf8')  
        cur = DB.cursor()
        sql = "INSERT IGNORE INTO test.testtable (name,phone,id,pw)  VALUES (%s, %s, %s, %s)"

        val = (newid,newpw,newname,newphone)

        cur.execute(sql, val)
        DB.commit()
        return json.dumps ("{'data' : '회원가입이 되었습니다.'}")


@app.route("/Signup_post_1",methods=['POST']) #회원가입POST
def Signup_post_1(): #연습용Post
    global newid
    global newpw

    if request.method == 'POST': # POST방식으로 요구
        i = request.get_json() # json타입으로 정보가져와 i에 대입
        newid = i.get('New_ID')
        newpw = i.get('New_PW')
        newname = i.get('New_NAME')
        newphone = i.get('New_Phone')
        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='test_naver',charset='utf8')  
        cur = DB.cursor()
        sql = "INSERT IGNORE INTO test_naver.test_table_naver (ID,PW,Name,Phone)  VALUES (%s, %s, %s, %s)"

        val = (newid,newpw,newname,newphone)

        cur.execute(sql, val)
        DB.commit()
        return json.dumps ("{'data' : 'test_회원가입이 되었습니다.'}")


@app.route("/testpost_1",methods=['POST']) #NAVER로그인POST
def testpost_1(): #연습용Post
    global newid
    global newpw
    if request.method == 'POST':
        i = request.get_json()

        if newid == i.get('ID') and newpw == i.get('PW'):
            return json.dumps("{'data' : 로그인 되었습니다.}")
        else:
            return json.dumps("{'data' : 비밀번호가 틀렸습니다.}")


@app.route("/dbsearch",methods=['POST'])
def dbsearch():
    if request.method == 'POST':
        i = request.get_json()
        idd = i.get('ID') #a
        pw = i.get('PW') #a2
        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='test',charset='utf8')  
        sql = DB.cursor()
        sql.execute("select * from test.testtable where id='"+idd+"' and pw='"+pw+"'")
        data = json.dumps(sql.fetchall(),default=str)
        return data
# select * from  test.testtable where id= 'a' and pw='a2'


@app.route("/dbsearch_1",methods=['POST'])
def dbsearch_1():

    if request.method == 'POST':
        i = request.get_json()
        sql_ID = i.get('ID') #a
        sql_PW = i.get('PW') #a2
        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='test_naver',charset='utf8')  
        sql = DB.cursor()
        sql.execute("select * from test_naver.test_table_naver where ID='"+sql_ID+"' and PW='"+sql_PW+"'")
        data = json.dumps(sql.fetchall(),default=str)
        return data
        

        
@app.route("/Serch_User",methods=['POST'])
def Serch_User():
    if request.method == 'POST':
        i = request.get_json()
        sql_Phone = i.get('Serch_Phone')

        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='test_naver',charset='utf8')  
        sql = DB.cursor()
        sql.execute("select * from test_naver.test_table_naver where Phone='"+sql_Phone+"'")
        data = json.dumps(sql.fetchall(),default=str)
        return data



@app.route("/text_Update",methods=['POST']) #블로그 글 업로드
def text_Update():
    global Title
    global Notice

    if request.method == 'POST': # POST방식으로 요구
        i = request.get_json() # json타입으로 정보가져와 i에 대입
        Title = i.get('Title')
        Notice = i.get('Contents')
        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='test_naver',charset='utf8')  
        cur = DB.cursor()
        sql = "INSERT IGNORE INTO test_naver.test_table_blog (Title, Notice)  VALUES (%s, %s)"

        val = (Title, Notice)

        cur.execute(sql, val)
        DB.commit()
        return json.dumps ("{'data' : '게시글이 올라갔습니다.'}")


@app.route("/Serch_Title",methods=['POST']) # 블로그 제목 찾기
def Serch_Title():
    if request.method == 'POST':
        i = request.get_json()
        sql_Title = i.get('ST')

        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='test_naver',charset='utf8')  
        sql = DB.cursor()
        sql_1 = DB.cursor()
        sql.execute("select * from test_naver.test_table_blog where Title='"+sql_Title+"'")
        sql.execute("SELECT * FROM test_table_blog WHERE Title LIKE'%"+sql_Title+"%'") # 특정단어 검색용도이나 도저히 사용 못하겠음
        data = json.dumps(sql.fetchall(),default=str)
        return data
'''


@app.route("/Login_DB",methods=['POST']) # 로그인
def Login_DB():
    if request.method == 'POST': # POST방식으로 들어온 데이터가 있다면 다음과 같이 실행하라
        i = request.get_json()
        UserID = i.get('ID')
        UserPW = i.get('PW')

        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='DW_test',charset='utf8')  
        sql = DB.cursor()
        sql.execute("select * from DW_test.test where ID='"+UserID+"' and PW='"+UserPW+"'")
        data = json.dumps(sql.fetchall(),default=str)
        return data


@app.route("/Sign_DB",methods=['POST']) # 회원가입
def Sign_DB(): #연습용Post

    if request.method == 'POST': # POST방식으로 요구
        i = request.get_json() # json타입으로 정보가져와 i에 대입
        New_ID = i.get('ID')
        New_PW = i.get('PW')
        New_Name = i.get('Name')
        New_Phone = i.get('Phone')
        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='DW_test',charset='utf8')  
        cur = DB.cursor()
        sql = "INSERT IGNORE INTO DW_test.test (ID,PW,Name,Phone)  VALUES (%s, %s, %s, %s)"

        val = (New_ID, New_PW, New_Name, New_Phone)

        cur.execute(sql, val)
        DB.commit()
        return json.dumps ("{'회원가입이 되었습니다.'}")


@app.route("/User_DB",methods=['POST']) # 계정찾기
def User_DB():
    if request.method == 'POST':
        i = request.get_json()
        Name = i.get('Name')
        Phone = i.get('Phone')

        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='DW_test',charset='utf8')  
        sql = DB.cursor()
        sql.execute("select * from DW_test.test where Name='"+Name+"' and Phone='"+Phone+"'")
        data = json.dumps(sql.fetchall(),default=str)
        return data


@app.route("/Notice_DB",methods=['POST']) # 글 업로드
def Notice_DB():

    if request.method == 'POST': # POST방식으로 요구
        i = request.get_json() # json타입으로 정보가져와 i에 대입
        Title = i.get('Title')
        Notice = i.get('Main_Text')
        print(Notice)
        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='DW_test',charset='utf8')  
        cur = DB.cursor()
        sql = "INSERT IGNORE INTO DW_test.Notice (Title, Notice)  VALUES (%s, %s)"

        val = (Title, Notice)

        cur.execute(sql, val)
        DB.commit()
        return json.dumps ("{'data' : '게시글이 올라갔습니다.'}")


@app.route("/Title_DB",methods=['POST']) # 제목 찾기
def Title_DB():
    if request.method == 'POST':
        i = request.get_json()
        sql_Title = i.get('Title')

        DB = pymysql.connect(host='192.168.0.43',user='root',password='1234',db='DW_test',charset='utf8')  
        sql = DB.cursor()
        sql.execute("select * from DW_test.Notice where Title='"+sql_Title+"'")
        sql.execute("SELECT * FROM Notice WHERE Title LIKE'%"+sql_Title+"%'") # 특정단어 검색용도이나 도저히 사용 못하겠음
        data = json.dumps(sql.fetchall(),default=str)
        return data




if __name__ == '__main__':

    app.run(host='0.0.0.0',port=5000, threaded=True)
    
    #os.execl(sys.executable, sys.executable, *sys.argv)

