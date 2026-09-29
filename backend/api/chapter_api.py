from flask_restful import Api, Resource, reqparse
from application.models import *
from flask_security import auth_required, roles_required,roles_accepted,current_user
from .utils import *
parser1=reqparse.RequestParser()
parser1.add_argument('name')
parser1.add_argument('id')
parser1.add_argument('description')

class ChapterApi(Resource):
    @auth_required("token")
    @roles_accepted("admin","user")
    def get(self,sub_id):
        chapters=[]
        chapters_json=[]
        
        chapters=Chapter.query.filter_by(subject_id=sub_id).all()
        for chapter in chapters:
            this_chapter={}
            this_chapter["id"]=chapter.id
            this_chapter["name"]=chapter.name
            this_chapter["description"]=chapter.description
           # this_chapter['quizs']=chapter.quizs
            this_chapter['s_id']=chapter.subject_id
            chapters_json.append(this_chapter)
        print(chapters_json)
        if chapters_json :
            return chapters_json ,200
        else:
            return {
                "message": " No chapters found"
            },404 
            
    @auth_required("token")
    @roles_required("admin")    
    def post(self,sub_id):
        args = parser1.parse_args()
        try:
            chapter=Chapter(
                name=args['name'],
                description=args['description'],
                subject_id=sub_id
                
            )
            db.session.add(chapter)
            db.session.commit()
            return {
                "message": " Chapter created successfully"
                }
        except:
            return {
                "message": "one or more field missing"
            },400
            
    @auth_required("token")
    @roles_required("admin")    
    def put(self,chapter_id):
        args = parser1.parse_args()
        chapter=Chapter.query.get(chapter_id)
        print(chapter)
        chapter.name=args['name']
        chapter.description=args['description']
        db.session.commit()
        return {
            "message":" Chapter updated successfully"
        }
    
            
    @auth_required("token")
    @roles_required("admin")    
    def delete(self,chapter_id):
        
        chapter=Chapter.query.get(chapter_id)
        if chapter:
            db.session.delete(chapter)
            db.session.commit()
            return {
            "message":" Chapter deleted successfully"
            }
        else:
            return{
                "message":"No such chapter id"
            },404
        
        

