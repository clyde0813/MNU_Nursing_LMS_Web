def html_return(type_id, method):
    if type_id == 1:
        if method == "create":
            html = "professor/notice/notice_add.html"
        elif method == "modify":
            html = "professor/notice/notice_modify.html"
        elif method == "detail":
            html = "professor/notice/notice_detail.html"
    elif type_id == 2:
        if method == "create" or method == "modify":
            html = "professor/guide/guide_add.html"
        elif method == "detail":
            html = "professor/list/assignment_list.html"
        elif method == "assignment":
            html = "professor/guide/guide_detail.html"
    elif type_id == 3:
        if method == "create" or method == "modify":
            html = "professor/hand/hand_add.html"
        elif method == "detail":
            html = "professor/list/assignment_list.html"
        elif method == "assignment":
            html = "professor/hand/hand_detail.html"
        elif method == "evaluate":
            html = "professor/hand/hand_evaluate.html"
    elif type_id == 4:
        if method == "create" or method == "modify":
            html = "professor/assignment/assignment_add.html"
        elif method == "detail":
            html = "professor/list/assignment_list.html"
        elif method == "assignment":
            html = "professor/assignment/assignment_detail.html"
    elif type_id == 5:
        if method == "create" or method == "modify":
            html = "professor/training/training_add.html"
        elif method == "detail":
            html = "professor/list/assignment_list.html"
        elif method == "assignment":
            html = "professor/training/training_detail.html"
    return html
