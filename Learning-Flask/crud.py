from sql_basic import db, Puppy

'''
#create table Puppy
db.create_all()

#add column
golden = Puppy(name='golden',age=10)
labrador = Puppy(name='labrador',age=8)

#add to database
db.session.add_all([golden,labrador])
db.session.commit()

all_puppy = Puppy.query.all()
print(all_puppy)

'''
#select by id
data = Puppy.query.get(1)
print(data)

#filter 
data = Puppy.query.filter_by(name='golden').all()
print(data)

#update 
up = Puppy.query.get(3)
up.name = 'anjing'
db.session.add(up)
db.session.commit()

print(Puppy.query.all())

#limit 
data = Puppy.query.limit(2).all()
print(data)

#order by
data = Puppy.query.order_by(Puppy.age).all()
print(data)

'''
#delete 
deleted = Puppy.query.get(1)
db.session.delete(deleted)
db.session.commit()
'''

print(Puppy.query.all())
