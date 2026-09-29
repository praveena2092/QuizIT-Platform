from flask_restful import Api, Resource, reqparse
from application.models import *
from flask_security import auth_required, roles_required,roles_accepted,current_user
from .utils import *
from datetime import datetime, timedelta
from extension import cache
class UserQuizApi(Resource):
    @auth_required("token")
    @roles_required("user")
    @cache.cached(timeout=300, key_prefix='transactions_data')
    def get(self,id):
        quizs=[]
        quizs_json=[]
        quizs=Quiz.query.filter_by(chapter_id=id).all()
        
        for quiz in quizs:
            this_quiz={}
            this_quiz["id"]=quiz.id
            this_quiz["date_of_quiz"]=quiz.date_of_quiz.isoformat()
            this_quiz["time_duration"]=str(quiz.time_duration)
            this_quiz["remarks"]=quiz.remarks
            this_quiz['chapter']=quiz.chapter.name
            this_quiz["chap_description"]=quiz.chapter.description
            this_quiz["sub_name"]=quiz.chapter.subject.name
            this_quiz["sub_description"]=quiz.chapter.description
            #this_quiz['questions']=quiz.questions
            #this_quiz['scores']=quiz.scores
            quizs_json.append(this_quiz)
        if quizs_json :
            return quizs_json ,200
        else:
            return {
                "message": " No quiz found"
            },404 
   
    
