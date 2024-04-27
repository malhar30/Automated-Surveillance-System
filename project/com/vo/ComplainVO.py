from project import db
from project.com.vo.LoginVO import LoginVO


class ComplainVO(db.Model):
    __tablename__ = 'complainmaster'
    complainId = db.Column('complainId', db.INTEGER, primary_key=True, autoincrement=True)
    complainSubject = db.Column('complainSubject', db.VARCHAR(200), nullable=False)
    complainDescription = db.Column('complainDescription', db.VARCHAR(500), nullable=False)
    complainDate = db.Column('complainDate', db.VARCHAR(100), nullable=False)
    complainTime = db.Column('complainTime', db.VARCHAR(100), nullable=False)
    complainStatus = db.Column('complainStatus', db.VARCHAR(100), nullable=False)
    complainFileName = db.Column('complainFileName', db.VARCHAR(100), nullable=True)
    complainFilePath = db.Column('complainFilePath', db.VARCHAR(200), nullable=True)
    complainTo_LoginId = db.Column('complainTo_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId), nullable=True)
    complainFrom_LoginId = db.Column('complainFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId), nullable=False)
    replySubject = db.Column('replySubject', db.VARCHAR(200), nullable=True)
    replyMessage = db.Column('replyMessage', db.VARCHAR(500), nullable=True)
    replyFileName = db.Column('replyFileName', db.VARCHAR(200), nullable=True)
    replyFilePath = db.Column('replyFilePath', db.VARCHAR(200), nullable=True)
    replyDate = db.Column('replyDate', db.VARCHAR(100), nullable=True)
    replyTime = db.Column('replyTime', db.VARCHAR(100), nullable=True)

    def as_dict(self):
        return {
            'complainId': self.complainId,
            'complainSubject': self.complainSubject,
            'complainDescription': self.complainDescription,
            'complainDate': self.complainDate,
            'complainTime': self.complainTime,
            'complainStatus': self.complainStatus,
            'complainFileName': self.complainFileName,
            'complainFilePath': self.complainFilePath,
            'complainTo_LoginId': self.complainTo_LoginId,
            'complainFrom_LoginId': self.complainFrom_LoginId,
            'replySubject': self.replySubject,
            'replyMessage': self.replyMessage,
            'replyFileName': self.replyFileName,
            'replyFilePath': self.replyFilePath,
            'replyDate': self.replyDate,
            'replyTime': self.replyTime

        }


db.create_all()
