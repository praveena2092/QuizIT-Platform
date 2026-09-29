from flask_restful import Api, Resource, reqparse
from application.models import *
from flask_security import auth_required, roles_required,roles_accepted,current_user
from .utils import *
from datetime import datetime, timedelta
from application.tasks import  daily_report,daily_report_quiz
parser2=reqparse.RequestParser()
parser2.add_argument('date_of_quiz')
parser2.add_argument('time_duration')
parser2.add_argument('remarks')

class QuizApi(Resource):
    @auth_required("token")
    @roles_accepted("admin","user")
    def get(self,chapter_id):
        quizs=[]
        quizs_json=[]
        
        quizs=Quiz.query.filter_by(chapter_id=chapter_id).all()
        
        for quiz in quizs:
            this_quiz={}
            this_quiz["id"]=quiz.id
            this_quiz["date_of_quiz"]=quiz.date_of_quiz.isoformat()
            this_quiz["time_duration"]=str(quiz.time_duration)
            this_quiz["remarks"]=quiz.remarks
            this_quiz['chapter']=quiz.chapter.name
            #this_quiz['questions']=quiz.questions
            #this_quiz['scores']=quiz.scores
            quizs_json.append(this_quiz)
        if quizs_json :
            print(quizs_json)
            return quizs_json ,200
        else:
            return {
                "message": " No quiz found"
            },404 
            
    @auth_required("token")
    @roles_required("admin")    
    def post(self,chapter_id):
        if "admin" in roles_list(current_user.roles):
            args = parser2.parse_args()
            date_of_quiz = datetime.strptime(args["date_of_quiz"], "%Y-%m-%d")
            h, m = map(int, args["time_duration"].split(":"))
            time_duration = timedelta(hours=h, minutes=m, seconds=0)  
            try:
                quiz=Quiz(
                        
                    date_of_quiz =date_of_quiz  ,
                    time_duration = timedelta(hours=h, minutes=m, seconds=0) ,
                    remarks=args['remarks'] ,
                    chapter_id=chapter_id
                        )
                db.session.add(quiz)
                db.session.commit()
                #daily_report()
                daily_report_quiz()
                return {
                "message": " Quiz created successfully"
                }
            except:
                return {
                    "message": "one or more field missing"
                },400
            
    @auth_required("token")
    @roles_required("admin")    
    def put(self,quiz_id):
        args = parser2.parse_args()
        quiz=Quiz.query.get(quiz_id)
        print(quiz,123456)
        date_of_quiz = datetime.strptime(args["date_of_quiz"], "%Y-%m-%d")  
        h, m ,s = map(int, args["time_duration"].split(":"))
        time_duration = timedelta(hours=h, minutes=m, seconds=s)  
        quiz.date_of_quiz=date_of_quiz
        quiz.time_duration=timedelta(hours=h, minutes=m, seconds=s) 
        quiz.remarks=args['remarks']
        db.session.commit()
        return {
            "message":" Quiz updated successfully"
        }
    
            
    @auth_required("token")
    @roles_required("admin")    
    def delete(self,quiz_id):
        
        quiz=Quiz.query.get(quiz_id)
        if quiz:
            db.session.delete(quiz)
            db.session.commit()
            return {
            "message":" Quiz deleted successfully"
            }
        else:
            return{
                "message":"No such quiz id"
            },404
        
        

