from flask_restful import Api, Resource, reqparse
from application.models import *
from flask_security import auth_required, roles_required,roles_accepted,current_user
from .utils import *
parser=reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('id')
parser.add_argument('description')

class SubjectApi(Resource):
    @auth_required("token")
    @roles_accepted("admin","user")
    def get(self):
        subjects=[]
        subjects_json=[]
        
        subjects=Subject.query.all()
        for subject in subjects:
            this_subject={}
            this_subject["id"]=subject.id
            this_subject["name"]=subject.name
            this_subject["description"]=subject.description
            subjects_json.append(this_subject)
        if subjects_json :
            return subjects_json ,200
        else:
            return {
                "message": " No subjects found"
            },404 
            
    @auth_required("token")
    @roles_required("admin")    
    def post(self):
        
        args = parser.parse_args()
        try:
            print(args)
            subject=Subject(
                name=args['name'],
                description=args['description'],
                
            )
            db.session.add(subject)
            db.session.commit()
            return {
                "message": " Subject created successfully"
            }
        except:
            return {
                "message": "one or more field missing or subject already exists"
            },400
            
    @auth_required("token")
    @roles_required("admin")    
    def put(self,sub_id):
        try:
            args = parser.parse_args()
            subject=Subject.query.get(sub_id)
            subject.name=args['name']
            subject.description=args['description']
            db.session.commit()
            return {
                "message":" Subject updated successfully"
            }
        except:
             return {
                "message": "Subject should be unique"
            },404            
    
            
    @auth_required("token")
    @roles_required("admin")    
    def delete(self,sub_id):
        
        subject=Subject.query.get(sub_id)
        if subject:
            db.session.delete(subject)
            db.session.commit()
            return {
            "message":" Subject deleted successfully"
            }
        else:
            return{
                "message":"No such subject id"
            },404
        
        