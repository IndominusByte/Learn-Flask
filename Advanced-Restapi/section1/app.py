from services import app, api
from services.resources.Users import *
from services.resources.Items import CrudItem

api.add_resource(RegisterUser,'/register')
api.add_resource(LoginUser,'/login')
api.add_resource(LogoutUser,'/logout')
api.add_resource(RefreshToken,'/refresh')
api.add_resource(CrudUser,'/user/<int:user_id>')
api.add_resource(CrudItem,'/items')
api.add_resource(ActivateUser,'/user_confirm/<token>')
api.add_resource(ResendEmail,'/resendemail')

if __name__ == '__main__':
    app.run(debug=True)
