def html_return(type_id, method):
    if type_id != 1 and method == "modify":
        html = "professor/layout/curriculum_submit.html" 

    if type_id == 1:
        if method == "create":
            html = "professor/notice/notice_add.html"
        elif method == "modify":
            html = "professor/notice/notice_modify.html"
        elif method == "detail":
            html = "professor/detail/notice_detail.html"
    elif type_id == 2:
        if method == "detail":
            html = "professor/list/assignment_list.html"
        elif method == "assignment":
            html = "professor/detail/guide_detail.html"
    elif type_id == 3:
        if method == "detail":
            html = "professor/list/assignment_list.html"
        elif method == "assignment":
            html = "professor/detail/hand_detail.html"
        elif method == "evaluate":
            html = "professor/hand/hand_evaluate.html"
    elif type_id == 4:
        if method == "detail":
            html = "professor/list/assignment_list.html"
        elif method == "assignment":
            html = "professor/detail/assignment_detail.html"
    elif type_id == 5:
        if method == "detail":
            html = "professor/list/assignment_list.html"
        elif method == "assignment":
            html = "professor/detail/training_detail.html"
    return html
