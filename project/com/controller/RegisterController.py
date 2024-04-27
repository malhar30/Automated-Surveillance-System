import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/admin/loadUser')
def adminLoadUser():
    try:
        if adminLoginSession() == "admin":
            return render_template('admin/addUser.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertRegister', methods=['post'])
def adminInsertRegister():
    try:
        if adminLoginSession() == "admin":
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            registerVO = RegisterVO()
            registerDAO = RegisterDAO()

            loginUsername = request.form['loginUsername']

            registerFirstname = request.form['registerFirstname']
            registerLastname = request.form['registerLastname']
            registerGender = request.form['registerGender']
            registerContactNumber = request.form['registerContactNumber']

            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

            sender = "automatesurveillancesystem@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "LOGIN PASSWORD"

            msg.attach(MIMEText(loginPassword, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "m@lh@r3003")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            loginVO.loginUsername = loginUsername
            loginVO.loginPassword = loginPassword
            loginVO.loginRole = "user"
            loginVO.loginStatus = "active"

            loginDAO.insertLogin(loginVO)

            registerVO.registerFirstname = registerFirstname
            registerVO.registerLastname = registerLastname
            registerVO.registerGender = registerGender
            registerVO.registerContactNumber = registerContactNumber

            registerVO.register_LoginId = loginVO.loginId

            registerDAO.insertRegister(registerVO)

            server.quit()

            return redirect(url_for("adminViewUser"))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewUser')
def adminViewUser():
    try:
        if adminLoginSession() == "admin":
            registerDAO = RegisterDAO()
            registerVOList = registerDAO.viewUser()

            return render_template("admin/viewUser.html", registerVOList=registerVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/blockUser', methods=['GET'])
def adminBlockUser():
    try:
        if adminLoginSession() == 'admin':
            registerDAO = RegisterDAO()
            registerVO = RegisterVO()

            loginDAO=LoginDAO()
            loginVO=LoginVO()

            loginId = request.args.get('loginId')
            #registerId=request.args.get('registerId')
            loginStatus = "deactive"

            # registerVO.registerId = registerId
            # registerDAO.registerDeleteUser(registerVO)

            loginVO.loginId=loginId
            loginVO.loginStatus = loginStatus
            loginDAO.loginBloackUser(loginVO)

            return adminViewUser()
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/unblockUser', methods=['GET'])
def adminUnblockUser():
    try:
        if adminLoginSession() == 'admin':
            registerDAO = RegisterDAO()
            registerVO = RegisterVO()

            loginDAO=LoginDAO()
            loginVO=LoginVO()

            loginId = request.args.get('loginId')
            #registerId=request.args.get('registerId')
            loginStatus = "active"

            # registerVO.registerId = registerId
            # registerDAO.registerDeleteUser(registerVO)

            loginVO.loginId=loginId
            loginVO.loginStatus = loginStatus
            loginDAO.loginUnblockUser(loginVO)

            return adminViewUser()
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/editUser', methods=['GET'])
def adminEditUser():
    try:
        if adminLoginSession() == 'admin':
            registerDAO=RegisterDAO()
            registerVO = RegisterVO()
            loginId = request.args.get('loginId')
            registerVO.register_LoginId = loginId
            userVOList=registerDAO.editUser(registerVO)
            print(userVOList)
            return render_template('admin/editUser.html', userVOList=userVOList)
        else:
            return adminLogoutSession
    except Exception as ex:
        print(ex)

@app.route('/admin/updateUser', methods=['POST'])
def adminUpdateUser():
    try:
        if adminLoginSession() == 'admin':
            registerDAO = RegisterDAO()
            loginDAO = LoginDAO()
            loginVO = LoginVO()
            registerVO = RegisterVO()

            loginId = request.form['loginId']
            loginUsername=request.form['loginUsername']
            oldUsername=request.form['oldUsername']
            registerId = request.form['registerId']
            registerFirstname = request.form['registerFirstname']
            registerLastname = request.form['registerLastname']
            registerGender = request.form['registerGender']
            registerContactNumber = request.form['registerContactNumber']

            if oldUsername == loginUsername:
                loginVO.loginId=loginId
                loginVO.loginUsername=loginUsername
                loginDAO.loginUpdateUser(loginVO)
            else:
                loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

                sender = "automatesurveillancesystem@gmail.com"

                receiver = loginUsername

                msg = MIMEMultipart()

                msg['From'] = sender

                msg['To'] = receiver

                msg['Subject'] = "LOGIN PASSWORD"

                msg.attach(MIMEText(loginPassword, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "m@lh@r3003")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                server.quit()

                loginVO.loginId=loginId
                loginVO.loginUsername = loginUsername
                loginVO.loginPassword = loginPassword
                loginDAO.loginUpdateUser(loginVO)


            registerVO.registerId = registerId
            registerVO.registerFirstname = registerFirstname
            registerVO.registerLastname = registerLastname
            registerVO.registerGender = registerGender
            registerVO.registerContactNumber = registerContactNumber
            registerDAO.registerUpdateUser(registerVO)


            return redirect(url_for('adminViewUser'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)