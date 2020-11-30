from flask import Flask ,render_template,request,Blueprint,session,redirect
from main_app.app import mydb
from mysql.connector import errors

from main_app.helper import __create_encryption

student_login=Blueprint('students_login',__name__,url_prefix='/stu_login')


@student_login.route('/login', methods=['POST','GET'])
def log_func():
        if request.method =='POST':
                post_data=request.form
                try:
                        mycursor=mydb.cursor(dictionary=True)
                        sql='SELECT stu_id,stu_name,stu_email,stu_pass FROM students WHERE stu_email=%s' 
                        val=(post_data['stu_email']),
                        mycursor.execute(sql,val)
                        user_details = mycursor.fetchone()
                        if user_details == None:
                                return 'no user found'
                        else:
                                if user_details['stu_pass'] ==__create_encryption(post_data['stu_pass']):
                                        session["students"] ={
                                                'stu_id' : user_details['stu_id'],
                                                'stu_name' : user_details['stu_name'],
                                                'stu_email' : user_details['stu_email']
                                        }
                                        return redirect ('/stu_login/')
                                else:
                                        return 'email not match' 
                except errors.Error as e:
                        print("Db error :",e) 
                        return 'server error'
        else:
                return render_template('students_login/students_login.html')
   

@student_login.route('/', methods=['GET']) 
def all_user_func():

        try:
                
                mycursor = mydb.cursor(dictionary=True)
                sql="SELECT stu_name,stu_result FROM students "
                
                mycursor.execute(sql)
                user_details = mycursor.fetchall()
                if user_details == None:
                         return 'no user found'
                else:
                 #print(user_details)
                        return render_template('students_login/stu_index.html',  data=user_details)
                 
        except errors.Error as e:
                print("Db error :",e)
                return 'not able to check ,Please try again letter'