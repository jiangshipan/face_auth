# coding= utf-8

from wtforms import Form, StringField, validators, IntegerField, FieldList


class FaceSearch(Form):
    user_id = IntegerField(u'所属用户id', [validators.required()])
    base64_code = StringField(u'人脸base64编码', [validators.required()])


class FaceRegister(FaceSearch, Form):
    face_name = StringField(u'人脸名称', [validators.Length(min=1, max=32), validators.required()])
    face_class = StringField(u'人脸所属班级', [validators.length(min=2, max=32), validators.required()])

