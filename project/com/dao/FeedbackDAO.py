from project import db
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.vo.LoginVO import LoginVO


class FeedbackDAO:

    def adminViewFeedback(self):
        feedbackList = db.session.query(FeedbackVO, LoginVO).join(LoginVO,
                                                                  FeedbackVO.feedbackFrom_LoginId == LoginVO.loginId).all()

        return feedbackList

    def adminReviewFeedback(self, feedbackVO):
        db.session.merge(feedbackVO)
        db.session.commit()

    def userInsertFeedback(self, feedbackVO):
        db.session.add(feedbackVO)
        db.session.commit()

    def userViewFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.filter_by(feedbackFrom_LoginId=feedbackVO.feedbackFrom_LoginId).all()
        return feedbackList

    def userDeleteFeedback(self, feedbackVO):
        feedbackId = FeedbackVO.query.get(feedbackVO.feedbackId)

        db.session.delete(feedbackId)

        db.session.commit()
