from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from function.professor.curriculum import *
from function.professor.html import *


@login_required(redirect_field_name=None)
def student_evaluate(request, subject_id):
    context = {
        "subject_id": subject_id,
        "type_id": 7
    }
    return render(request, "professor/student_evaluation/evaluation_list.html", context)


@login_required(redirect_field_name=None)
def professor_evaluate(request, subject_id):
    if request.method == "POST":
        for data in request.POST:
            if "percent" in data:
                eval_id = data.replace("percent", "")
                eval_percent = request.POST[data]
                if "New" in eval_id:
                    eval_id = eval_id.replace("New", "")
                    if eval_percent is None or eval_percent.isdigit() is False:
                        eval_percent = 0
                    SubjectEvaluationItem.objects.create(subject_id=subject_id, name=eval_id, percentage=eval_percent)
                else:
                    eval_object = SubjectEvaluationItem.objects.filter(subject_id=subject_id, id=eval_id)
                    if eval_object.exists():
                        eval_object = eval_object[0]
                        if eval_object.percentage == eval_percent:
                            pass
                        else:
                            eval_object.percentage = eval_percent
                            eval_object.save()
        return redirect("professor:professor_evaluate", subject_id)
    student_objects = User.objects.filter(profile__group__name="student", enrollment__subject_id=subject_id,
                                          enrollment__status=True).all()
    evaluation_items = SubjectEvaluationItem.objects.filter(subject_id=subject_id).all()
    context = {
        "subject_id": subject_id,
        "student_objects": student_objects,
        "evaluation_items": evaluation_items,
        "type_id": 8
    }
    return render(request, "professor/professor_evaluation/evaluation_list.html", context)


@login_required(redirect_field_name=None)
def professor_evaluate_detail(request, subject_id, student_id):
    if request.method == "POST":
        curriculum_eval_objects = Post.objects.filter(postsubjectmapping__subject_id=subject_id,
                                                      type_id__in=[2, 3, 4, 5], postevaluationstatus__status=True).all()
        for data in curriculum_eval_objects:
            request_percentage = request.POST.get("eval-" + str(data.id))
            post_eval_object, created = PostEvaluation.objects.get_or_create(post_id=data.id, target_id=student_id)
            post_eval_object.percentage = request_percentage
            post_eval_object.save()
        return redirect("professor:professor_evaluate_detail", subject_id, student_id)
    if request.method == "GET":
        enrollment_object = Enrollment.objects.filter(subject_id=subject_id, student_id=student_id).get()
        subject_object = Subject.objects.get(id=subject_id)
        total_score = 0

        curriculum_objects = {
            "guide_objects": {"objects": {}, "curriculum_name": ""},
            "hand_objects": {"objects": {}, "curriculum_name": ""},
            "assignment_objects": {"objects": {}, "curriculum_name": ""},
            "journal_objects": {"objects": {}, "curriculum_name": ""},
        }

        # 커리큘럼 오브젝트
        guide_curriculum_objects = Post.objects.filter(postsubjectmapping__subject_id=subject_id, type_id=2).all()
        hand_curriculum_objects = Post.objects.filter(postsubjectmapping__subject_id=subject_id, type_id=3).all()
        assignment_curriculum_objects = Post.objects.filter(postsubjectmapping__subject_id=subject_id, type_id=4).all()
        journal_curriculum_objects = Post.objects.filter(postsubjectmapping__subject_id=subject_id, type_id=5).all()

        # 평가 항목 퍼센트
        guide_eval_percentage = SubjectEvaluationItem.objects.filter(subject_id=subject_id,
                                                                     post_type=2).get().percentage
        hand_eval_percentage = SubjectEvaluationItem.objects.filter(subject_id=subject_id,
                                                                    post_type=3).get().percentage
        assignment_eval_percentage = SubjectEvaluationItem.objects.filter(subject_id=subject_id,
                                                                          post_type=4).get().percentage
        journal_eval_percentage = SubjectEvaluationItem.objects.filter(subject_id=subject_id,
                                                                       post_type=5).get().percentage

        curriculums = [
            guide_curriculum_objects,
            hand_curriculum_objects,
            assignment_curriculum_objects,
            journal_curriculum_objects
        ]

        for curriculum in curriculums:
            tmp = []
            score_sum_tmp = 0
            for data in curriculum:
                title = data.title
                status = None
                eval_status = True
                score = None
                link = None
                assignment_object = Post.objects.filter(
                    child_post__parent_post=data,
                    author_id=student_id
                )
                eval_object = PostEvaluation.objects.filter(post_id=data.id, target_id=student_id)
                if eval_object:
                    score = eval_object.get().percentage
                    score_sum_tmp += score
                if assignment_object.exists():
                    status = True
                    link = "/p/%d/%d/%d/%d" % (subject_id, data.type.id, data.id, assignment_object.get().id)
                if not data.postevaluationstatus_set.exists() or data.postevaluationstatus_set.get().status is False:
                    eval_status = False
                tmp.append({
                    "id": data.id,
                    "title": title,
                    "link": link,
                    "status": status,
                    "eval_status": eval_status,
                    "score": score
                })
            if curriculum == guide_curriculum_objects:
                curriculum_objects["guide_objects"]["objects"] = tmp
                curriculum_objects["guide_objects"]["curriculum_name"] = PostType.objects.get(id=2).name
                total_score += score_sum_tmp * (guide_eval_percentage / 100)
            elif curriculum == hand_curriculum_objects:
                curriculum_objects["hand_objects"]["objects"] = tmp
                curriculum_objects["hand_objects"]["curriculum_name"] = PostType.objects.get(id=3).name
                total_score += score_sum_tmp * (hand_eval_percentage / 100)
            elif curriculum == assignment_curriculum_objects:
                curriculum_objects["assignment_objects"]["objects"] = tmp
                curriculum_objects["assignment_objects"]["curriculum_name"] = PostType.objects.get(id=4).name
                total_score += score_sum_tmp * (assignment_eval_percentage / 100)
            elif curriculum == journal_curriculum_objects:
                curriculum_objects["journal_objects"]["objects"] = tmp
                curriculum_objects["journal_objects"]["curriculum_name"] = PostType.objects.get(id=5).name
                total_score += score_sum_tmp * (journal_eval_percentage / 100)

        # 추가 평가 항목 (커스텀)
        additional_eval_objects = SubjectEvaluationItem.objects.filter(subject_id=subject_id, post_type=None)

        total_eval_percentage = (guide_eval_percentage + hand_eval_percentage +
                                 assignment_eval_percentage + journal_eval_percentage)
        if additional_eval_objects.exists():
            total_eval_percentage += additional_eval_objects.annotate(total=Sum('percentage')).first().total

        context = {
            "subject_id": subject_id,
            "type_id": 8,
            "enrollment_object": enrollment_object,
            "subject_object": subject_object,
            "curriculum_objects": curriculum_objects,
            "total_score": total_score,
            "eval": {
                "guide_eval_percentage": guide_eval_percentage,
                "hand_eval_percentage": hand_eval_percentage,
                "assignment_eval_percentage": assignment_eval_percentage,
                "journal_eval_percentage": journal_eval_percentage,
                "additional_eval_objects": additional_eval_objects.all(),
                "total_eval_percentage": total_eval_percentage
            }
        }
        return render(request, "professor/professor_evaluation/evaluation_detail.html", context)
