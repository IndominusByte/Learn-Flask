#CREATE ENTRIES INTO THE TABLES
from relationship import db, Owner, Puppy, Toy

'''
#create 2 puppies
rufus = Puppy('rufus')
fido = Puppy('fido')

#add puppies to db
db.session.add_all([rufus,fido])
db.session.commit()

#check
print(Puppy.query.all())
rufus = Puppy.query.filter_by(name='rufus').first()
print(rufus)

#create owner object
jose = Owner('jose',rufus.id)
db.session.add(jose)
db.session.commit()
print(rufus)

#give rufus some toys 2 data
chew = Toy('chew toy',rufus.id)
ball = Toy('Ball',rufus.id)
db.session.add_all([chew,ball])
db.session.commit()

'''
#grab rufus after those additions!
rufus = Puppy.query.filter_by(name='rufus').first()
rufus.report_toys()
