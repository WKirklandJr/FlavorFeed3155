from src.models import db, Tag

class TagRepository:

    
    def get_tag(self, tagname):
        tag_name = Tag.query.filter_by(tagname=tagname).first()

        return tag_name

tag_repository_singleton = TagRepository()
