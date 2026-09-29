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

class QuestionApi(Resource):
    @auth_required("token")
    @roles_accepted("admin","user")
    def get(self,quiz_id):
        questions=[]
        questions_json=[]
        
        questions=Question.query.filter_by(quiz_id=quiz_id).all()
        
        for question in questions:
            this_question={}
            this_question["id"]=question.id
            this_question["question_statement"]=question.question_statement
            this_question["option_1"]=question.option_1
            this_question["option_2"]=question.option_2
            this_question["option_3"]=question.option_3
            this_question["option_4"]=question.option_4
            this_question["correct_answer"]=question.correct_answer
            this_question['quiz_id']=question.quiz_id
            this_question['time']=int(question.question.time_duration.total_seconds())
            print(this_question)
            questions_json.append(this_question)
        if questions_json :
            return questions_json ,200
        else:
            return {
                "message": " No question found"
            },404 
            
    @auth_required("token")
    @roles_required("admin")    
    def post(self,quiz_id):
        args = parser3.parse_args()
        try:
            question=Question(
                question_statement=args['question_statement'],
                option_1=args['option_1'],
                option_2=args['option_2'],
                option_3=args['option_3'],
                option_4=args['option_4'],
                correct_answer=args['correct_answer'],
                quiz_id=quiz_id
                
            )
            db.session.add(question)
            db.session.commit()
            return {
                "message": " Question created successfully"
            }
        except:
            return {
                "message": "one or more field missing"
            },400
            
    @auth_required("token")
    @roles_required("admin")    
    def put(self,question_id):
        args = parser3.parse_args()
        question=Question.query.get(question_id)
        question.question_statement=args['question_statement']
        question.option_1=args['option_1']
        question.option_2=args['option_2']
        question.option_3=args['option_3']
        question.option_4=args['option_4']
        question.correct_answer=args['correct_answer']
        print(f"question_statement:  (type: {type(args['question_statement'])})")


        db.session.commit()
        return {
            "message":" Question updated successfully"
        }
    
            
    @auth_required("token")
    @roles_required("admin")    
    def delete(self,question_id):
        
        question=Question.query.get(question_id)
        if question:
            db.session.delete(question)
            db.session.commit()
            return {
            "message":" Question deleted successfully"
            }
        else:
            return{
                "message":"No such chapter id"
            },404
        
        

