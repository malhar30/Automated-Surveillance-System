from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.DetectionVO import DetectionVO

class DetectionDAO():

    def insertDetection(self,detectionVO):
        db.session.add(detectionVO)
        db.session.commit()

    def viewDetection(self):
        videoList = db.session.query(DetectionVO, LoginVO).join(LoginVO, DetectionVO.detection_LoginId == LoginVO.loginId).all()

        return videoList

    def viewLoginUser(self):
        userList = db.session.query(LoginVO).all()

        return userList

    def viewRegisterUser(self):
        userList = db.session.query(RegisterVO).all()

        return userList

    def deleteDetection(self,detectionVO):
        detectionList = DetectionVO.query.get(detectionVO.detectionId)
        db.session.delete(detectionList)
        db.session.commit()
        return detectionList
