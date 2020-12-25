from flask import Flask , render_template,request,Blueprint,session,redirect

from main_app.app import mydb
from mysql.connector import errors

from main_app.helper import __is_alpha_space,__is_email,__create_encryption

user_list=Blueprint('user',__name__,url_prefix='/user')


@user_list.route('/create', methods=['POST','GET'])
def create_func():
        if request.method=='POST':
                post_data=request.form
                if __is_alpha_space(post_data['name']) and __is_email(post_data['email']) and len (post_data['password'])>4:
                        db_pass_to_save=__create_encryption(post_data['password'])

                        
                        
                        try:
                                mycursor=mydb.cursor(dictionary=True)
                                sql='INSERT INTO users (name,email,password) VALUES (%s,%s,%s)'
                                val=(post_data['name']),(post_data['email']),db_pass_to_save,
                                mycursor.execute(sql,val)
                                mydb.commit()
                                if (mycursor.rowcount==1):
                                        success_dis={
                                                'message':'data save successfully'
                                        }
                                        return render_template('user/create.html',success=success_dis)
                                else:
                                        success_dis={
                                                'message':'data not save'
                                        }
                                        return render_template('user/create.html',success=success_dis)
                                        
                                        
                        except errors.Error as e:
                                print("Db error :",e) 
                                return 'server error'
                else:
                        success_dis={
                                'message':'please provide valid information'
                        }
                        return render_template('user/create.html',success=success_dis)
                      
        else:
                return render_template('user/create.html')

@user_list.route('/login', methods=['POST','GET'])
def login_func():
        if request.method =='POST':
                post_data=request.form
                try:
                        mycursor=mydb.cursor(dictionary=True)
                        sql='SELECT id,name,email,password FROM users WHERE email=%s' 
                        val=(post_data['email']),
                        mycursor.execute(sql,val)
                        user_details = mycursor.fetchone()
                        if user_details == None:
                                error_dis={
                                        'message':'no user found'
                                }
                                return render_template('user/login.html',error=error_dis)
                        else:
                                if user_details['password'] ==__create_encryption(post_data['password']):
                                        session["user"] ={
                                                'id' : user_details['id'],
                                                'name' : user_details['name'],
                                                'email' : user_details['email']
                                        }
                                        return redirect('/')
                                else:
                                        error_message={
                                        'message':'email or password wrong'
                                        }
                                        return render_template('user/login.html',error_mess=error_message)
                except errors.Error as e:
                        print("Db error :",e) 
                        return 'server error'
        else:
                return render_template('user/login.html')



@user_list.route('/logout', methods=['GET']) 
def user_logout_fun():
        session.pop('user', None)
        return redirect('/user/login')  


      


        