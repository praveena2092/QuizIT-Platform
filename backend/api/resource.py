from flask_restful import Api, Resource, reqparse
from application.models import *
from flask_security import auth_required, roles_required,roles_accepted,current_user
from .subject_api import *
from .chapter_api import *
from .quiz_api import *
from .question_api import *
from .score_api import *
from .user_quiz import *
from .user_ques import *
api = Api()

    
api.add_resource(SubjectApi,'/api/subject/get',"/api/subject/create","/api/subject/update/<int:sub_id>","/api/subject/delete/<int:sub_id>")
api.add_resource(ChapterApi,'/api/chapter/get/<int:sub_id>',"/api/chapter/create/<int:sub_id>","/api/chapter/update/<int:chapter_id>","/api/chapter/delete/<int:chapter_id>")
api.add_resource(QuizApi,'/api/quiz/get/<int:chapter_id>',"/api/quiz/create/<int:chapter_id>","/api/quiz/update/<int:quiz_id>","/api/quiz/delete/<int:quiz_id>")
api.add_resource(QuestionApi,'/api/question/get/<int:quiz_id>',"/api/question/create/<int:quiz_id>","/api/question/update/<int:question_id>","/api/question/delete/<int:question_id>")
api.add_resource(ScoreApi,'/api/score/get/',"/api/score/create/<int:user_id>/<int:quiz_id>","/api/score/update/<int:score_id>","/api/score/delete/<int:score_id>")   
api.add_resource(UserQuizApi,'/api/user/quiz/get/<int:id>',"/api/user/scoreUpdate/create/<int:quiz_id>")
api.add_resource(UserQuestionApi,"/api/user/question/get/<int:quiz_id>")
    
            
        