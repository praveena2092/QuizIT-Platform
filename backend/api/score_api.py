from flask_restful import Api, Resource, reqparse
from application.models import *
from flask_security import auth_required, roles_required,roles_accepted,current_user
from datetime import datetime, timedelta
from .utils import *
parser4=reqparse.RequestParser()
parser4.add_argument('time_stamp_of_attempt')
parser4.add_argument('total_score')


class ScoreApi(Resource):
    @auth_required("token")
    @roles_accepted("admin","user")
    def get(self):
        scores=[]
        scores_json=[]
        
        scores=Scores.query.all()
        for score in scores:
            this_score={}
            this_score["id"]=score.id
            this_score["total_score"]=score.total_score
            this_score["time_stamp_of_attempt"]=score.time_stamp_of_attempt.isoformat()
            this_score['quiz_id']=score.quiz_id
            this_score['user_id']=score.user_id
            scores_json.append(this_score)
        if scores_json :
            return scores_json ,200
        else:
            return {
                "message": " No scores found"
            },404 
            
    @auth_required("token")
    @roles_required("admin")    
    def post(self,user_id,quiz_id):
        args = parser4.parse_args()
        time_stamp_of_attempt = datetime.strptime(args["time_stamp_of_attempt"], "%d/%m/%Y") 
        try:
            score=Scores(
                user_id=user_id,
                quiz_id=quiz_id,
                time_stamp_of_attempt=time_stamp_of_attempt,
                total_score=args['total_score']
                
            )
            db.session.add(score)
            db.session.commit()
            return {
                "message": " Score created successfully"
            }
        except:
            return {
                "message": "one or more field missing"
            },400
            
    @auth_required("token")
    @roles_required("admin")    
    def put(self,score_id):
        args = parser4.parse_args()
        score=Scores.query.get(score_id)
        time_stamp_of_attempt = datetime.strptime(args["time_stamp_of_attempt"], "%d/%m/%Y") 
        score.time_stamp_of_attempt=time_stamp_of_attempt
        score.total_score=args['total_score']
        db.session.commit()
        return {
            "message":" Score updated successfully"
        }
    
            
    @auth_required("token")
    @roles_required("admin")    
    def delete(self,score_id):
        
        score=Scores.query.get(score_id)
        if score:
            db.session.delete(score)
            db.session.commit()
            return {
            "message":" Score deleted successfully"
            }
        else:
            return{
                "message":"No such score id"
            },404
        
        

