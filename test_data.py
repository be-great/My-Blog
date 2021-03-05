import logging
from main import db
from models import Post,User,Tag
from  faker import Faker
import random

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

log = logging.getLogger(__name__)
faker = Faker()

def generate_posts(n,users,tags):
    for i in range(n):
        post =Post(faker.sentence())
        post.text = faker.text(max_nb_chars=1000)
        post.publish_date=faker.date_this_century(before_today=True,after_today=False)
        post.user_id = users[random.randrange(0,len(users))].id
        post.tags = [tags[random.randrange(0,len(tags))] for i in range(0,2)] # have two tags random
        try :
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            log.error("Fail to add post %s: %s"% (str(post),e))
            db.session.rollback()



def generate_users(n):
    users = list()
    for i in range(n):
        user =User(i)
        user.username = faker.name()
        user.password = "anypassword"
        try :
            db.session.add(user)
            db.session.commit()
            users.append(user)
        except Exception as e :
            log.error("Error add user %s : %s"%(str(user),e))
            db.session.rollback()
    return users
def generate_tags(n):
    tags= list()
    for i in range(n):
        tag = Tag(i)
        tag.title = faker.color_name()
        try :
            db.session.add(tag)
            db.session.commit()
            tags.append(tag)
        except Exception as e :
            log.error("Error add tag %s : %s"%(str(tag),e))
            db.session.rollback()
    return tags

generate_posts(15,generate_users(10),generate_tags(10))
