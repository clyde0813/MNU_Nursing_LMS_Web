from models.models import *


def html_return(type_id, method):
    if type_id == 1:
        html = "student/notice/notice_detail.html"
    elif type_id == 2:
        if method == "detail":
            html = "student/guide/guide_detail.html"
        elif method == "create":
            html = "student/guide/guide_submit.html"
    elif type_id == 3:
        if method == "detail":
            html = "student/hand/hand_detail.html"
        elif method == "create":
            html = "student/hand/hand_submit.html"
    elif type_id == 4:
        if method == "detail":
            html = "student/assignment/assignment_detail.html"
        elif method == "create":
            html = "student/assignment/assignment_submit.html"
    elif type_id == 5:
        if method == "detail":
            html = "student/training/training_detail.html"
        elif method == "create":
            html = "student/training/training_submit.html"
    elif type_id == 8:
        html = "student/evaluation/evaluation_detail.html"
    return html
