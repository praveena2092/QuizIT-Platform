from jinja2 import Template

def roles_list(roles):
    role_list=[]
    for role in roles:
        role_list.append(role.name)
    return role_list

def question_list(questions):
    quiz_list={}
    for q in questions:
        quiz_list[q.id]=q.correct_answer      
    return quiz_list

def format_report(html_template ,data):
    with open(html_template) as file:
        template=Template(file.read())
        return template.render(data=data)