from project import db


class FaceVO(db.Model):
    __tablename__ = 'facemaster'
    faceId = db.Column('faceId', db.INTEGER, primary_key=True, autoincrement=True)
    faceName = db.Column('faceName', db.String(100))
    faceFileName = db.Column('faceFileName', db.String(100))
    faceFilePath = db.Column('faceFilePath', db.VARCHAR(200))
    faceUploadDate = db.Column('faceUploadDate', db.String(100))
    faceUploadTime = db.Column('faceUploadTime', db.String(100))

    def as_dict(self):
        return {
            'faceId': self.faceId,
            'faceName':self.faceName,
            'faceFileName': self.faceFileName,
            'faceFilePath': self.faceFilePath,
            'faceUploadDate': self.faceUploadDate,
            'faceUploadTime': self.faceUploadTime
        }


db.create_all()
