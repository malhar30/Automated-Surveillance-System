from datetime import datetime

from flask import render_template, request, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO


@app.route('/admin/viewFeedback')
def adminViewFeedback():
    try:
        if adminLoginSession() == "admin":
            feedbackDAO = FeedbackDAO()
            feedbackVOList = feedbackDAO.adminViewFeedback()
            return render_template('admin/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/reviewFeedback', methods=['GET'])
def adminReviewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackId = request.args.get('feedbackId')
            feedbackTo_LoginId = session['session_loginId']

            feedbackVO.feedbackId = feedbackId
            feedbackVO.feedbackTo_LoginId = feedbackTo_LoginId

            feedbackDAO.adminReviewFeedback(feedbackVO)

            return redirect(url_for('adminViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# user

@app.route('/user/loadFeedback')
def userLoadFeedback():
    try:
        if adminLoginSession() == "user":
            return render_template('user/addFeedback.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertFeedback', methods=['POST'])
def userInsertFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']
            feedbackDate = datetime.today().strftime("%d/%m/%Y")
            feedbackTime = datetime.now().strftime("%H:%M:%S")
            feedbackFrom_LoginId = session['session_loginId']

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime
            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId

            feedbackDAO.userInsertFeedback(feedbackVO)

            return redirect(url_for('userViewFeedback'))

        else:
            return adminLogoutSession
    except Exception as ex:
        print(ex)


@app.route('/user/viewFeedback')
def userViewFeedback():
    try:
        if adminLoginSession() == "user":
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()
            feedbackFrom_LoginId = session['session_loginId']
            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId
            feedbackVOList = feedbackDAO.userViewFeedback(feedbackVO)
            return render_template('user/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteFeedback', methods=['GET'])
def userDeleteFeedback():
    try:
        if adminLoginSession() == "user":
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackId = request.args.get('feedbackId')
            feedbackVO.feedbackId = feedbackId

            feedbackDAO.userDeleteFeedback(feedbackVO)
            return redirect(url_for('userViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
