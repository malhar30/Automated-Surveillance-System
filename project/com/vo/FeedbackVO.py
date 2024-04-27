from project import db
from project.com.vo.LoginVO import LoginVO


class FeedbackVO(db.Model):
    __tablename__ = 'feedbackmaster'
    feedbackId = db.Column('feedbackId', db.INTEGER, primary_key=True, autoincrement=True)
    feedbackSubject = db.Column('feedbackSubject', db.VARCHAR(200), nullable=False)
    feedbackDescription = db.Column('feedbackDescription', db.VARCHAR(500), nullable=False)
    feedbackRating = db.Column('feedbackRating', db.INTEGER, nullable=False)
    feedbackDate = db.Column('feedbackDate', db.VARCHAR(100), nullable=False)
    feedbackTime = db.Column('feedbackTime', db.VARCHAR(100), nullable=False)
    feedbackTo_LoginId = db.Column('feedbackTo_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId), nullable=True)
    feedbackFrom_LoginId = db.Column('feedbackFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId), nullable=False)

    def as_dict(self):
        return {
            'feedbackId': self.feedbackId,
            'feedbackSubject': self.feedbackSubject,
            'feedbackDescription': self.feedbackDescription,
            'feedbackRating': self.feedbackRating,
            'feedbackDate': self.feedbackDate,
            'feedbackTime': self.feedbackTime,
            'feedbackTo_LoginId': self.feedbackTo_LoginId,
            'feedbackFrom_LoginId': self.feedbackFrom_LoginId,

        }


db.create_all()
