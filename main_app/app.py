from flask import Flask ,render_template,request,session,redirect

import mysql.connector
from mysql.connector import errors
from main_app.helper import __create_encryption

try:
        mydb=mysql.connector.connect(host='45.76.160.243',user='babun',password='Babun_admin_mysql_1101_1998',database='babun_school')
        if mydb.is_connected():
                print ('database connect')
        else:
                print ('database not conect')
except errors.Error as e:
    print("Db error :",e)  

app=Flask(__name__)
app.secret_key = "babun1234__sec"

from main_app.user.user import user_list
app.register_blueprint(user_list)
from main_app.students.students_login import student_login
app.register_blueprint(student_login)

@app.route('/', methods=['GET']) 
def all_user_func():

        if 'user' in session:
                user_id = session['user']['id']
                user_name = session['user']['name']
                user_email = session['user']['email']
                try:
                        mycursor = mydb.cursor(dictionary=True)
                        sql="SELECT DISTINCT stu_class FROM students "
                        # val=('stu_class'),
                        mycursor.execute(sql)
                        user_details = mycursor.fetchall()

                        if user_details == None:
                                return 'no user found'
                        else:
                                #print(user_details)
                                return render_template('index.html',  data=user_details)
                                
                except errors.Error as e:
                        print("Db error :",e)
                        return 'not able to check ,Please try again letter'
        else:
                return redirect('/user/login')


@app.route('/student_list', methods=['POST','GET'])
def create_func():
        if request.method=='POST':
                post_data=request.form
                db_pass_to_save=__create_encryption(post_data['stu_pass'])
                try:
                        mycursor=mydb.cursor(dictionary=True)
                        sql='INSERT INTO students (stu_class,stu_email,stu_pass,stu_name,stu_result) VALUES (%s,%s,%s,%s,%s)'
                        val=(post_data['stu_class']),(post_data['stu_email']),db_pass_to_save,(post_data['stu_name']),(post_data['stu_result'])
                        mycursor.execute(sql,val)
                        mydb.commit()
                        if (mycursor.rowcount==1):
                               student_saved = True
                        else:
                               student_saved = False

                        sql="SELECT stu_id ,stu_name FROM students"
                        mycursor.execute(sql)
                        student_list=mycursor.fetchall()
                        return render_template('student.html',stu_list=student_list , new_stu_saved=student_saved)
                
                except errors.Error as e:
                        print("Db error :",e) 
                        return 'server error'
       
       
       
        else:
                mycursor=mydb.cursor(dictionary=True)
                sql="SELECT stu_id ,stu_name FROM students"
                mycursor.execute(sql)
                student_list=mycursor.fetchall()
                return render_template('student.html',stu_list=student_list , new_stu_saved = False)

@app.route('/class/<int:cls_id>', methods=['GET']) 
def perticular_class(cls_id):

        if 'user' in session:
                try:
                        

                        mycursor = mydb.cursor(dictionary=True)
                        sql="SELECT stu_id,stu_name FROM students WHERE stu_class= %s "
                        val=(str(cls_id),)
                        mycursor.execute(sql,val)
                        student_details = mycursor.fetchall()
                        if student_details == None:
                                return 'no blog found'
                        else:
                                
                        # return(student_details)
                                return render_template('studen_name.html', data=student_details)
                                
                except errors.Error as e:
                        
                        print("Db error :",e)
                        return 'not able to check ,Please try again letter'
                
        else:
                return redirect('/user/login')
 
@app.route("/student/<int:stu_id>", methods=['GET'])
def student_nam(stu_id):

        mycursor = mydb.cursor(dictionary=True)
        sql="SELECT stu_id,stu_email,stu_result FROM students WHERE stu_id= %s "
        val=(str(stu_id),)
        mycursor.execute(sql,val)
        student_details = mycursor.fetchone()
        if student_details == None:
                return 'no blog found'
        else:
                return render_template('details.html',dt=student_details)
                              
