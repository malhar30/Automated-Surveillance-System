from project import db
from project.com.vo.FaceVO import FaceVO

class FaceDAO():
    def insertFace(self,faceVO):
        db.session.add(faceVO)
        db.session.commit()

    def viewFace(self):
        faceList=FaceVO.query.all()
        return faceList