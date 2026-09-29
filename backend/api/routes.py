from flask import current_app as app,jsonify,request,render_template,send_from_directory
from flask_security import auth_required,roles_required,roles_accepted, current_user,login_user
from flask_security import hash_password
from application.database import db
from werkzeug.security import check_password_hash, generate_password_hash
from .utils import *
from application.models import *
from datetime import datetime
from celery.result import AsyncResult
from application.tasks import csv_report,monthly_report, daily_report
from sqlalchemy import text
from datetime import datetime, timedelta
@app.route("/",methods = ["GET"])
def home():
    return render_template("index.html")

@app.route("/api/admin")
@auth_required("token") # auth
@roles_required('admin') #role
def admin():
    return {
        "message" : "admin logged in successfully"
    }
  
@app.route("/api/home")
@auth_required("token") # auth
@roles_accepted('user',"admin") #role
def user_home():
    user=current_user
    print(user.roles,1234)
    return jsonify(
        {
            "username":user.username,
            "email":user.email,
            "roles":roles_list(user.roles)
        }
    )
     
@app.route("/api/login",methods=["POST"])
def user_login():
    
    body=request.get_json()
    email=body["email"]
    password=body['password'] 
    if not email :
        return jsonify({
            "message": "email is required"
            
        }) ,400
    user=app.security.datastore.find_user(email=email)
    
    if user:
        if check_password_hash(user.password,password):
            
            login_user(user)
            if any(role.name == "admin" for role in current_user.roles):
                print(roles_list(user.roles))
            return jsonify({
                "id":user.id,
                "username":user.username,
                "auth_token":user.get_auth_token(),
                "roles":roles_list(user.roles)
            })  
        else:
            return jsonify({
                "message":"Incorrect password"
            }),400
    else:
        return jsonify({
            "message":"User not found"
        }) ,400
    
    
@app.route("/api/register",methods=["POST"])
def create_user():
    credentials=request.get_json()
    if not app.security.datastore.find_user(email = credentials["email"]):
        app.security.datastore.create_user(email=credentials["email"],
                                           username=credentials["username"],
                                           password=generate_password_hash(credentials["password"]),
                                           dob=credentials["dob"],
                                           roles=['user'])
        db.session.commit()
    
        return jsonify(
             {
                "email": credentials["email"],
                "username": credentials["username"],
                "dob": credentials["dob"]
            },
       ), 201
    return jsonify({
        "message": "User already exists"
    }),400
    
@app.route("/api/up/<int:quiz_id>",methods=["POST"])
@auth_required("token") # auth
@roles_accepted('user',"admin") #role
def score_update(quiz_id):
    user_answer=request.get_json()
    quiz=Quiz.query.get(quiz_id)
    question=quiz.questions
    answer=question_list(question)
    print(answer)
    score=0
    for i in user_answer:
        if i["id"] in answer:
            if i["answer"].strip()==answer[i["id"]].strip() :
                score+=1
    print(score)
    user=current_user
    try:
        scores=Scores(
            quiz_id=quiz_id,
            user_id=user.id,
            total_score=score,
            time_stamp_of_attempt=datetime.now()
        )
        db.session.add(scores)
        db.session.commit()
        daily_report(scores.taker.username)
        return {
            "message": " Score updated successfully"
            },200
    except:
        return {
             "message": "one or more field missing"
        },400
            
    
@app.route("/api/export")
def export_csv():
    result=csv_report.delay()
    return jsonify({
        "id":result.id,
        "result":result.result
    })
    
@app.route("/api/csv_result/<id>")
def csv_results(id):
    result=AsyncResult(id)
    return send_from_directory("static",result.result)            
    



@app.route("/api/mail")
@auth_required("token") # auth
@roles_accepted('user',"admin") #role
def send_reports():
    res=monthly_report.delay()
    return {
        "result":res.result
    }
    
   
    
@app.route("/api/quiz/chart",methods=["POST"])
@auth_required("token") # auth
@roles_accepted('user',"admin") #role
def get_quiz_chart():
    scores=Scores.query.all()
    quiz={}
    for score in scores:
        if score.quiz_id not in quiz:
            quiz[score.quiz_id]=1
        else:
            quiz[score.quiz_id]+=1
    print(quiz)
   
    return jsonify(
        quiz
    )
    
@app.route("/api/quiz/score/chart",methods=["POST"])
@auth_required("token") # auth
@roles_accepted('user',"admin") #role
def get_score_chart():
    scores=Scores.query.all()
    score_user={}
    for score in scores:
        if score.user_id not in score_user:
            score_user[score.taker.username]=score.total_score
        else:
            score_user[score.taker.username]=max(score_user[score.taker.username],score.total_score)
    print(score_user)
   
    return jsonify(
        score_user
    )
    
    
@app.route('/admin/popular-quizzes', methods=['GET'])

def get_popular_quizzes():
    query =  text("""
        SELECT 
            q.id AS quiz_id,
            q.date_of_quiz,
            ch.name AS chapter_name,
            COUNT(s.id) AS attempts
        FROM Quiz q
        JOIN Scores s ON s.quiz_id = q.id
        JOIN Chapter ch ON ch.id = q.chapter_id
        GROUP BY q.id, q.date_of_quiz, ch.name
        ORDER BY attempts DESC;
    """)
    result = db.session.execute(query).fetchall()
    quizzes = [{
        "quiz_id": row.quiz_id,
        "date_of_quiz": row.date_of_quiz,
        "chapter_name": row.chapter_name,
        "attempts": row.attempts
    } for row in result]
    return jsonify(quizzes)
    
@app.route('/user/<int:user_id>/attempts')
def user_attempts(user_id):
    query = text("""
        SELECT 
            q.id AS quiz_id,
            ch.name AS chapter_name,
            q.date_of_quiz,
            s.total_score
        FROM Scores s
        JOIN Quiz q ON q.id = s.quiz_id
        JOIN Chapter ch ON ch.id = q.chapter_id
        WHERE s.user_id = :user_id
        ORDER BY q.date_of_quiz;
    """)
    result = db.session.execute(query, {"user_id": user_id}).fetchall()
    return jsonify([{
        "quiz_id": row.quiz_id,
        "chapter_name": row.chapter_name,
        "date_of_quiz": row.date_of_quiz,
        "score": row.total_score
    } for row in result])
    
    
@app.route('/api/quiz/start', methods=['POST'])
@auth_required()
def start_quiz():
    data = request.json
    new_quiz = Quiz(
        date_of_quiz=datetime.utcnow().date(),
        time_duration=timedelta(minutes=data['duration']),
        remarks=data.get('remarks', ''),
        chapter_id=data['chapter_id'],
        internal_status='active'
    )
    db.session.add(new_quiz)
    db.session.commit()
    return jsonify({'quiz_id': new_quiz.id}), 201

@app.route('/api/quiz/<int:quiz_id>/questions', methods=['GET'])
@auth_required()
def get_questions(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    quiz = Quiz.query.get(quiz_id)
    return jsonify({
        'questions': [
            {
                'id': q.id,
                'question_statement': q.question_statement,
                'option_1': q.option_1,
                'option_2': q.option_2,
                'option_3': q.option_3,
                'option_4': q.option_4,
            } for q in questions
        ],
        'duration_seconds': int(quiz.time_duration.total_seconds())
    })


@app.route('/api/quiz/<int:quiz_id>/submit', methods=['POST'])
@auth_required()
def submit_quiz(quiz_id):
    data = request.json  # [{id: question_id, answer: user_answer}]
    user_id = current_user.id
    total_score = 0

    for item in data:
        q = Question.query.get(item['id'])
        if q.correct_answer == item['answer']:
            total_score += 1
        q.user_answer = item['answer']
    
    score_entry = Scores(
        quiz_id=quiz_id,
        user_id=user_id,
        total_score=total_score,
        time_stamp_of_attempt=datetime.utcnow()
    )
    db.session.add(score_entry)
    db.session.commit()
    daily_report(score_entry.taker.username)
    return jsonify({'score': total_score})

@app.route('/api/quiz/<int:quiz_id>/score', methods=['GET'])
@auth_required()
def get_score(quiz_id):
    score = Scores.query.filter_by(quiz_id=quiz_id, user_id=current_user.id).first()
    return jsonify({
        'quiz_id': quiz_id,
        'score': score.total_score,
        'attempted_at': score.time_stamp_of_attempt
    })



@app.route("/api/user/<int:user_id>/past-scores", methods=["GET"])
def get_user_scores(user_id):
    results = (
        db.session.query(Scores, Quiz, Chapter, Subject)
        .join(Quiz, Scores.quiz_id == Quiz.id)
        .join(Chapter, Quiz.chapter_id == Chapter.id)
        .join(Subject, Chapter.subject_id == Subject.id)
        .filter(Scores.user_id == user_id)
        .all()
    )

    data = []
    for score, quiz, chapter, subject in results:
        data.append({
            "quiz_id": quiz.id,
            "quiz_date": quiz.date_of_quiz.isoformat(),
            "score": score.total_score,
            "duration": str(quiz.time_duration),
            "remarks": quiz.remarks,
            "chapter": chapter.name,
            "subject": subject.name,
        })
    print(data)
    return jsonify(data)