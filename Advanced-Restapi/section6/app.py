from services.config import app, api
from services.resources.Users import *
from services.resources.Items import CrudItem
from services.resources.UploadImage import UploadImage, Image, AvatarUpload, Avatar
from services.resources.OAuthLogin import GithubLogin, GithubAuthorize

api.add_resource(RegisterUser,'/register')
api.add_resource(ConfirmUser,'/user_confirm/<token>')
api.add_resource(LoginUser,'/login')
api.add_resource(LogoutUser,'/logout')
api.add_resource(RefreshToken,'/refresh')
api.add_resource(UpdateUser,'/update-user')
api.add_resource(GetUser,'/user')
api.add_resource(ResendEmail,'/resend-email')
api.add_resource(CrudItem,'/items')
api.add_resource(UploadImage,'/upload/image')
api.add_resource(Image,'/image/<filename>')
api.add_resource(AvatarUpload,'/upload/avatar')
api.add_resource(Avatar,'/avatar')

api.add_resource(GithubLogin,'/login/github')
api.add_resource(GithubAuthorize,'/login/github/authorize',endpoint='github.authorize')

if __name__ == '__main__':
    app.run()
