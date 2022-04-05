class check(object):
    def __init__(self):
        self.mainobj = None
    def checkcollide(self,cursor,groupls,tobebuilt,x=None,y=None):

        # if x ==None:

        #     tobebuilt.position.x = cursor.position.x
        #     tobebuilt.position.y = cursor.position.y
        # else:
        #     tobebuilt.position.x = x
        #     tobebuilt.position.y = y


        for ls in groupls:
            for item in ls:
                if item.getCollisionRect().colliderect(tobebuilt.getCollisionRect(True)):
                    return False
                
        return True