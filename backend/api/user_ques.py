from flask_restful import Api, Resource, reqparse
from application.models import *
from flask_security import auth_required, roles_required,roles_accepted,current_user
from .utils import *

parser3=reqparse.RequestParser()
parser3.add_argument('question_statement')
parser3.add_argument('option_1')
parser3.add_argument('option_2')
parser3.add_argument('option_3')
parser3.add_argument('option_4')
parser3.add_argument('correct_answer')

class UserQuestionApi(Resource):
    @auth_required("token")
    @roles_required("user")
    def get(self,quiz_id):
        print(123)
        questions=[]
        questions_json=[]
        
        questions=Question.query.filter_by(quiz_id=quiz_id).all()
        print(questions,999999)
        for question in questions:
            this_question={}
            this_question["id"]=question.id
            this_question["question_statement"]=question.question_statement
            this_question["option_1"]=question.option_1
            this_question["option_2"]=question.option_2
            this_question["option_3"]=question.option_3
            this_question["option_4"]=question.option_4
            # this_question["correct_answer"]=question.correct_answer
            #this_question['quiz_id']=question.quiz_id
            questions_json.append(this_question)
        if questions_json :
            return questions_json ,200
        else:
            return {
                "message": " No question found"
            },404 
            
    
            
    