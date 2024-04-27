from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


class RegisterDAO:

    def insertRegister(self, registerVO):
        db.session.add(registerVO)
        db.session.commit()

    def viewUser(self):
        userList = db.session.query(RegisterVO, LoginVO).join(LoginVO,
                                                              RegisterVO.register_LoginId == LoginVO.loginId).all()

        return userList

    def editUser(self, registerVO):
        userList = db.session.query(RegisterVO, LoginVO).join(LoginVO,
                                                                 RegisterVO.register_LoginId == LoginVO.loginId).filter_by(
            loginId=registerVO.register_LoginId).all()
        return userList

    def registerUpdateUser(self,registerVO):
        db.session.merge(registerVO)
        db.session.commit()

    def registerDeleteUser(self,registerVO):

        userList = RegisterVO.query.get(registerVO.registerId)
        db.session.delete(userList)
        db.session.commit()

