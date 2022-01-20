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


@app.route("/")
def main():
    return render_template('login.html')

@app.route("/sign_up") #회원가입화면
def sign_up():
    return render_template('sign_up.html')

@app.route("/login") #메인화면
def login():
    return render_template('login.html')

@app.route("/Serch_ID") #메인화면
def Serch_ID():
    return render_template('Serch_ID.html')

@app.route("/Serch_PW") #메인화면
def Serch_PW():
    return render_template('Serch_PW.html')


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
        recvdata = i.get('numder')
        newid = i.get('New_ID')
        newpw = i.get('New_PW')

        return json.dumps ("{'data' : '회원가입이 되었습니다.'}")


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



if __name__ == '__main__':

    app.run(host='0.0.0.0',port=5000, threaded=True)
    
    #os.execl(sys.executable, sys.executable, *sys.argv)

