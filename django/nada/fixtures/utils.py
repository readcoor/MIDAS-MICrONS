

def nuke_all(classes):
    'Destroys all objects'
    for cls in classes:
        for obj in cls.objects.all():
            obj.delete()

def is_empty(classes):
    '''returns False if any instances of the given classes exist, else returns True'''
    for cls in classes:
        if 0 != len(cls.objects.all()):
            return False
    return True
                    
