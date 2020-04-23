from config import app, api, jwt
from models import User
from resources.Users import RegisterUser,LoginUser, UpdateDeleteUser, RefreshToken, LogoutUser
from blacklist import blacklists

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.get(identity)
    return {
        'username': user.username,
        'email': user.email
    }

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklists

api.add_resource(RegisterUser,'/register')
api.add_resource(LoginUser,'/login')
api.add_resource(UpdateDeleteUser,'/user/<int:id>')
api.add_resource(RefreshToken,'/refresh')
api.add_resource(LogoutUser,'/logout')

if __name__ == '__main__':
    app.run(debug=True)
