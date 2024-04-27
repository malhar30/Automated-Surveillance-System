from flask import render_template, request, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.ProfileDAO import ProfileDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/user/loadProfile')
def userLoadProfile():
    try:
        if adminLoginSession() == "user":
            profileDAO = ProfileDAO()
            registerVO = RegisterVO()

            register_LoginId = session['session_loginId']
            registerVO.register_LoginId = register_LoginId

            profileVOList = profileDAO.viewProfile(registerVO)
            return render_template('user/profile.html', profileVOList=profileVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/changePassword')
def userChangePassword():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/changePassword.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertPassword',methods=['POST'])
def userInsertPassword():
    try:
        if adminLoginSession() == 'user':
            profileDAO=ProfileDAO()
            loginVO = LoginVO()

            loginId = request.form['loginId']
            oldLoginPassword = request.form['oldLoginPassword']
            loginPassword = request.form['loginPassword']

            loginVO.loginId=loginId

            profileVOList = profileDAO.viewLoginDetails(loginVO)


            if oldLoginPassword == profileVOList.loginPassword:
                loginVO.loginPassword = loginPassword
                profileDAO.insertPassword(loginVO)
                return adminLogoutSession()
            else:
                msg = "Your old password are not match ! "
                return render_template('user/changePassword.html',msg=msg)
        else:
            adminLogoutSession()

    except Exception as ex:
        print(ex)





