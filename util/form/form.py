# coding=utf-8


def validate_form(form):
    if not form.validate():
        errors = [u'有错误发生:']
        for k, v in form.errors.iteritems():
            for m in v:
                errors.append(u'%s:%s' % (getattr(form, k).label.text, m))
        raise Exception(u'<br/>'.join(errors))
