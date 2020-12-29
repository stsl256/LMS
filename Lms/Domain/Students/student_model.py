from app import db
from Domain.Students import Group


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    year = db.Column(db.Integer)
    degree = db.Column(db.String(64))
    education_form = db.Column(db.String(64))
    education_basis = db.Column(db.String(64))

    def __repr__(self):
        return 'User_id: {user_id}, ' \
               'Учебная группа: {group}, Год поступления: {year}, Степень: {degree}, ' \
               'Форма обучения: {education}, Основа обучения: {basis} |'.format(
            group=self.group_id, year=self.year, degree=self.degree, education=self.education_form,
            basis=self.education_basis, user_id=self.user_id)
