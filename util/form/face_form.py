# coding= utf-8

from wtforms import Form, StringField, validators, IntegerField, FieldList


class FaceSearch(Form):
    user_id = IntegerField(u'所属用户id', [validators.required()])


class FaceRegister(FaceSearch, Form):
    face_name = StringField(u'人脸名称', [validators.Length(min=1, max=32), validators.required()])


class UserSearchFace(Form):
    user_ids = FieldList(IntegerField(u'用户id', [validators.required()]))
    page = IntegerField(u'页码', [validators.required()])
