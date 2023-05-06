from src.models import db, Tag

class TagRepository:

    def create_tag(self, tagname):
        create_tag = Tag(tagname)

        db.session.add(create_tag)
        db.session.commit()

        return create_tag
    
    def get_tag(self, tagname):
        tag_name = Tag.query.filter_by(tagname=tagname).first_or_404()

        return tag_name

tag_repository_singleton = TagRepository()