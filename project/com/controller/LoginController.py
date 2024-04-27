from flask import render_template, request, redirect, url_for, session
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from project import app
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.LoginVO import LoginVO
from project.com.dao.FaceDAO import FaceDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.dao.DatasetDAO import DatasetDAO


@app.route('/')
def adminLoadLogin():
    try:
        session.clear()
        return render_template('admin/login.html')
    except Exception as ex:
        print(ex)


@app.route("/admin/validateLogin", methods=['POST'])
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginStatus = "active"

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:

            msg = "Something Is Wrong!"

            return render_template('admin/login.html', error=msg)

        else:
            for row1 in loginDictList:

                loginId = row1['loginId']

                loginUsername = row1['loginUsername']

                loginRole = row1['loginRole']

                session['session_loginId'] = loginId

                session['session_loginUsername'] = loginUsername

                session['session_loginRole'] = loginRole

                session.permanent = True

                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))
                elif loginRole == 'user':
                    return redirect(url_for("userLoadDashboard"))


    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard')
def adminLoadDashboard():
    try:
        if adminLoginSession() == "admin":
            known = 0
            unknown = 0
            active=0
            deactive=0


            registerDAO = RegisterDAO()
            registerVOList = registerDAO.viewUser()
            user=len(registerVOList)
            for status in registerVOList:
                if status[1].loginStatus == "active":
                    active=active+1
                else:
                    deactive=deactive+1

            datasetDAO = DatasetDAO()
            datasetVOList = datasetDAO.viewDataset()
            dataset=len(datasetVOList)

            faceDAO = FaceDAO()
            faceVOList = faceDAO.viewFace()

            for face in faceVOList:
                if face.faceName == "Unknown":
                    unknown = unknown + 1
                else:
                    known = known + 1
            return render_template('admin/index.html',known=known,unknown=unknown,user=user,active=active,deactive=deactive,dataset=dataset)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/loadDashboard')
def userLoadDashboard():
    try:
        if adminLoginSession() == "user":
            known = 0
            unknown = 0
            faceDAO = FaceDAO()
            faceVOList = faceDAO.viewFace()
            for face in faceVOList:
                if face.faceName == "Unknown":
                    unknown = unknown + 1
                else:
                    known = known + 1

            return render_template('user/index.html',known=known,unknown=unknown)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:
            if session['session_loginRole'] == "admin":

                return "admin"

            elif session['session_loginRole'] == "user":

                return "user"

        else:
            return False

    except Exception as ex:
        print(ex)


@app.route('/admin/logoutSession')
def adminLogoutSession():
    try:
        session.clear()
        return redirect(url_for('adminLoadLogin'))
    except Exception as ex:
        print(ex)

@app.route("/admin/forgotPassword")
def adminForgotPassword():
    try:
        return render_template("admin/forgotPassword.html")
    except Exception as ex:
        print(ex)



@app.route("/admin/insertUsername",methods=["post"])
def adminInsertUsername():
    try:
        loginDAO=LoginDAO()
        loginVO=LoginVO()

        loginUsername=request.form['loginUsername']
        loginVO.loginUsername=loginUsername
        loginVOList=loginDAO.validateLoginUsername(loginVO)
        loginDictList = [i.as_dict() for i in loginVOList]
        lenLoginDictList = len(loginDictList)
        if lenLoginDictList == 0:
            err="E - mail is not exist !"
            return render_template("admin/forgotPassword.html",err=err)
        else:
            for row1 in loginDictList:

                loginId = row1['loginId']

                loginUsername = row1['loginUsername']

                session['session_loginId'] = loginId

                session['session_loginUsername'] = loginUsername


            otp = ''.join((random.choice(string.digits)) for x in range(6))

            sender = "automatesurveillancesystem@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "Reset Password"

            msg.attach(MIMEText(otp, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "m@lh@r3003")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            server.quit()

            session["otp"]=otp
            return render_template("admin/addOTP.html")


    except Exception as ex:
        print(ex)


@app.route("/admin/insertOtp",methods=['post'])
def adminInsertOtp():
    try:

        loginOtp=request.form["loginOtp"]
        if session["otp"] == loginOtp:
            return render_template("admin/addNewPassword.html")
        else:
            err="Otp is not Match!"
            return render_template("admin/addOTP.html",err=err)
    except Exception as ex:
        print(ex)

@app.route("/admin/insertNewPassword",methods=['post'])
def adminInsertNewPassword():
    try:
        loginDAO=LoginDAO()
        loginVO=LoginVO()
        loginPassword=request.form["loginPassword"]

        sender = "automatesurveillancesystem@gmail.com"

        receiver = session["session_loginUsername"]

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "New Password"

        msg.attach(MIMEText(loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender, "m@lh@r3003")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        server.quit()

        loginVO.loginId=session['session_loginId']
        loginVO.loginPassword=loginPassword
        loginDAO.loginUpdateUser(loginVO)
        return render_template("admin/login.html")

    except Exception as ex:
        print(ex)