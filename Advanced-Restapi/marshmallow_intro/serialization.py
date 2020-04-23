from marshmallow import Schema, fields, post_load

class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

class User:
    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password

user = User('oman','asd@gmail.com','asdasd')
schema = UserSchema()
print(schema.dump(user))

incoming_data = {'password': 'asdasd', 'email': 'asd@gmail.com', 'username': 'oman'}
new_schema = UserSchema()
new_user = new_schema.load(incoming_data)
print(new_user)
