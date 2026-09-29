from celery import shared_task
from .models import Quiz,User 
from api.utils import format_report
from datetime import datetime, timedelta
import datetime
import csv
from .mail import send_email
import requests
import os 
from flask_security import  current_user,login_user


@shared_task(ignore_results=False, name="Download_csv")
def csv_report():
    # user =User.query.get()
    # quiz=user.taker 
    quiz=Quiz.query.all()
    csv_file_name=f"transaction_{datetime.datetime.now().strftime("%f")}.csv"
    with open (f"static/{csv_file_name}","w",newline="") as csvfile:
        srno=1
        quiz_csv=csv.writer(csvfile,delimiter=",")
        quiz_csv.writerow(["srno","subject Name","Subject description","Chapter","Chapter Desription", "Quiz time","Quiz duration","Remarks"])
        for q in quiz :
            this_quiz=[srno,q.chapter.subject.name,q.chapter.subject.description,q.chapter.name,q.chapter.description, str(q.date_of_quiz),str(q.time_duration),q.remarks]
            quiz_csv.writerow(this_quiz)
            srno+=1
            
    return csv_file_name




@shared_task(ignore_results=False, name="monthly_report")
def monthly_report():
    users = User.query.all()
    for user in users[1:]:
        user_data = {}
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_quiz= []
        quizs=Quiz.query.all()
        for quiz in quizs:
            this_quiz={}
            this_quiz["quiz_time"]=quiz.date_of_quiz.isoformat()
            this_quiz["remarks"]=quiz.remarks
            this_quiz['chapter']=quiz.chapter.name    
            this_quiz['chapter_description']=quiz.chapter.description  
            this_quiz['subject']=quiz.chapter.subject.name    
            this_quiz['subject_desciption']=quiz.chapter.subject.description
            user_quiz.append(this_quiz)    
        user_data['quizs'] = user_quiz
        message = format_report('templates/mail_details.html', user_data)
        if user.email and '@' in user.email:
            send_email(user.email, subject="Monthly quiz Report - QuizIt", message=message)
        else:
            print(f"Skipped sending email: Invalid or empty email for user  {getattr(user, 'id', '<unknown>')}")

        #send_email(user.email, subject = "Monthly quiz Report - QuizIt", message = message)
    return "Monthly reports sent"

@shared_task(ignore_results=False, name="daily_remainder")
def daily_report(username):
    text=f"Hi {username} you have completed the quiz ...Please visit our app to view your score at http://127.0.0.5000"
    response=requests.post("https://chat.googleapis.com/v1/spaces/AAQAnO_4dNo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=7sAcWRf9gvG-sFHOgTWolXw5YAykYSZFGeGhN97rki8",json={"text":text})
    return "daily remainder"

@shared_task(ignore_results=False, name="daily_remainder_quiz")
def daily_report_quiz():
    text=f"Hi all , new quiz was created ...Please visit our app to give the new quiz at http://localhost:5173/"
    response=requests.post("https://chat.googleapis.com/v1/spaces/AAQAnO_4dNo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=7sAcWRf9gvG-sFHOgTWolXw5YAykYSZFGeGhN97rki8",json={"text":text})
    return "daily remainder quiz"


