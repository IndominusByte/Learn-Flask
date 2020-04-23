from services.serve import app, api
from services.resources.Items import CrudItem, AllItem
from services.resources.Stores import CrudStore, AllStore
from services.resources.Users import UserRegister, UserDelete, UserLogin

api.add_resource(CrudItem,'/item/<name>')
api.add_resource(CrudStore,'/store/<name>')
api.add_resource(AllItem,'/items')
api.add_resource(AllStore,'/stores')

api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin,'/login')
api.add_resource(UserDelete,'/remove/<username>')

if __name__ == '__main__':
    app.run()
