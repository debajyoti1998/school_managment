from flask import Flask ,render_template,request,Blueprint,session,redirect
from main_app.app import mydb
from mysql.connector import errors

from main_app.helper import __create_encryption

student_login=Blueprint('students_login',__name__,url_prefix='/students')


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
                                error_dis={
                                        'message':'no user found'
                                }
                                return render_template('students_login/students_login.html',error=error_dis)
                        else:
                                if user_details['stu_pass'] ==__create_encryption(post_data['stu_pass']):
                                        session["students"] ={
                                                'stu_id' : user_details['stu_id'],
                                                'stu_name' : user_details['stu_name'],
                                                'stu_email' : user_details['stu_email']
                                        }
                                        return redirect ('/students/')
                                else:
                                        success_dis={
                                                'message':'email or password not match'
                                        }
                                        return render_template('students_login/students_login.html',success=success_dis)
                except errors.Error as e:
                        print("Db error :",e) 
                        return 'server error'
        else:
                return render_template('students_login/students_login.html')
   

@student_login.route('/', methods=['POST','GET']) 
def all_user_func():

        try:
                
                mycursor = mydb.cursor(dictionary=True)
                sql="SELECT stu_name,stu_result FROM students WHERE stu_id=%s"
                val=(session['students']['stu_id']),
                
                mycursor.execute(sql,val)
                result = mycursor.fetchone()
                if result == None:
                        return 'no user found'
                else:
                        # return (session['students'])
                        return render_template('students_login/stu_index.html',data= result)
                 
        except errors.Error as e:
                print("Db error :",e)
                return 'not able to check ,Please try again letter'

@student_login.route('/logout', methods=['GET']) 
def students_logout_fun():
        session.pop('user', None)
        return redirect('/students/login')  



