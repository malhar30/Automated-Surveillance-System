from project import db
from project.com.vo.LoginVO import LoginVO


class LoginDAO:

    def insertLogin(self, loginVo):
        db.session.add(loginVo)
        db.session.commit()

    def validateLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername, loginPassword=loginVO.loginPassword,
                                            loginStatus=loginVO.loginStatus).all()
        return loginList

    def loginUpdateUser(self,loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def loginBloackUser(self, loginVO):

        db.session.merge(loginVO)
        db.session.commit()
        # userList=LoginVO.query.get(loginVO.loginId)
        # db.session.delete(userList)
        # db.session.commit()
    def loginUnblockUser(self,loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def validateLoginUsername(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername).all()
        return loginList