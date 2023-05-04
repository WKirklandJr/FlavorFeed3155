from src.models import db, Tag

def create_tag(self, tagname):
    create_tag = Tag(tagname)
    db.session.add(create_tag)
    db.session.commit()
    return create_tag
