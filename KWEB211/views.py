from django.shortcuts import render, redirect
from .models import Account, Lecture, LecturePost, Takes
from django.contrib.auth.models import User
from django.contrib import messages, auth
from .forms import LecturePostForm
import hashlib
from datetime import datetime

# Create your views here.


def index(request):
    try:
        if request.user:
            nickname = Account.objects.filter(username=request.user).values_list()[0][3]
            return render(request, 'KWEB211/index.html', {
                'nickname': nickname
            })
    except:
        return render(request, 'KWEB211/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/KWEB211/')
        else:
            messages.info(request, '아이디 혹은 비밀번호가 잘못되었습니다')
            return redirect('login')
    else:
        return render(request, 'KWEB211/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/KWEB211/')

def signup(request):
    if request.method == 'POST':
        # 아이디가 이미 존재하는 경우
        if Account.objects.filter(username=request.POST['username']).values():
            messages.info(request, '이미 존재하는 아이디 입니다.')
            return redirect('signup')

        # 비밀번호가 10자리 미만으로 구성 될 경우
        elif len(request.POST['password1']) < 10:
            messages.info(request, '비밀번호는 10자 이상으로 설정해주세요')
            return redirect('signup')

        # 비밀번호가 서로 일치 하지 않는 경우
        elif request.POST['password1'] != request.POST['password2']:
            messages.info(request, '비밀번호가 서로 일치하지 않습니다. 확인해 주세요')
            return redirect('signup')

        # 비밀번호가 서로 일치 할 경우
        elif request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']
            password = request.POST['password1']
            password_crypt = hashlib.sha256(password.encode('utf-8')).hexdigest()
            nickname = request.POST['nickname']
            studentId = request.POST['studentId']
            position = request.POST['position']
            email = request.POST['email']
            user = Account(username=username,
                         password=password_crypt,
                         nickname=nickname,
                         studentId=studentId,
                         position=position,
                         email=email)
            user.save()
            User.objects.create_user(username=username,
                                     password=password)
            return redirect('/KWEB211/')
    else:
        return render(request, 'KWEB211/signup.html')


def lecturelist(request):
    temp_user = request.user
    user_id = Account.objects.filter(username=temp_user).values_list()[0][0]
    user_takes = Takes.objects.filter(user_id=user_id).values_list()
    lecture_takes_id_list = [i[1] for i in user_takes]
    current_lecture_takes_name_list = []
    previous_lecture_takes_name_list = []
    lecture = Lecture.objects.values_list()

    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_semester = 1
    if 9 <= current_month <= 12:
        current_semester = 2

    for i in lecture_takes_id_list:
        lecture_name = Lecture.objects.filter(id=i).values_list()[0][1]
        professor_name = Lecture.objects.filter(id=i).values_list()[0][2]
        year = Lecture.objects.filter(id=i).values_list()[0][3]
        seme = Lecture.objects.filter(id=i).values_list()[0][4]
        semester = year+"년 "+seme+"학기"
        lecture_id = i
        if year == str(current_year) and seme == str(current_semester):
            current_lecture_takes_name_list.append([lecture_name,professor_name,semester,lecture_id])
        else:
            previous_lecture_takes_name_list.append([lecture_name,professor_name,semester,lecture_id])
    return render(request, 'KWEB211/lecturelist.html', {
        'current_lecture_takes_name_list': current_lecture_takes_name_list,
        'previous_lecture_takes_name_list': previous_lecture_takes_name_list,
        'lecture': lecture
    })


def update(request):
    post = LecturePost.objects.all().order_by('-created_at')
    temp_user = request.user
    user_id = Account.objects.filter(username=temp_user).values_list()[0][0]
    user_takes = Takes.objects.filter(user_id=user_id).values_list()
    lecture_takes_id_list = [i[1] for i in user_takes]
    new_post_list = post.values_list()

    filtered_lecture_id_list = []
    for n in new_post_list:
        if n[1] in lecture_takes_id_list:
            lecture_name = Lecture.objects.filter(id=n[1]).values_list()[0][1]
            date_time = LecturePost.objects.filter(lecture_id=n[1]).values_list()[0][4]
            filtered_lecture_id_list.append([date_time,lecture_name, n[2], n[3], n[1]])


    return render(request, 'KWEB211/update.html',{
        'post': post,
        'new_post_list': new_post_list,
        'filtered_lecture_id_list': filtered_lecture_id_list,
    })


def lectureread(request, lecture_id):
    lecture_name = Lecture.objects.filter(id=lecture_id).values_list()[0][1]
    temp_lecture_post = LecturePost.objects.all().order_by('-created_at').values_list()
    new_lecture_post = []
    for l in temp_lecture_post:
        if l[1] == lecture_id:
            new_lecture_post.append([l[2],l[3],l[4]])

    temp_user = request.user
    position = Account.objects.filter(username=temp_user).values_list()[0][5]
    is_professor = False
    if position == 'professor':
        is_professor = True
    return render(request, 'KWEB211/lectureread.html', {
        'new_lecture_post': new_lecture_post,
        'is_professor': is_professor,
        'lecture_id': lecture_id,
        'lecture_name': lecture_name,
    })


def lecturewrite(request, lecture_id):
    lecture_name = Lecture.objects.filter(id=lecture_id).values_list()[0][1]
    form = LecturePostForm()
    if request.method == 'POST':

        title = request.POST['title']
        content = request.POST['content']
        post1 = LecturePost(
            lecture_id=Lecture.objects.get(id=lecture_id),
            title=title,
            content=content
        )
        post1.save()
        return redirect('/KWEB211/')
    else:
        return render(request, 'KWEB211/lecturewrite.html',{
            'lecture_id': lecture_id,
            'lecture_name': lecture_name,
            'form' : form
        })


def profile(request):
    temp_username = request.user
    username = Account.objects.filter(username=temp_username).values_list()[0][1]
    nickname = Account.objects.filter(username=temp_username).values_list()[0][3]
    studentId = Account.objects.filter(username=temp_username).values_list()[0][4]
    position = Account.objects.filter(username=temp_username).values_list()[0][5]
    email = Account.objects.filter(username=temp_username).values_list()[0][6]

    return render(request, 'KWEB211/profile.html', {
        'nickname': nickname,
        'username': username,
        'studentId': studentId,
        'position': position,
        'email': email
    })


def profilechange(request):
    temp_username = request.user
    user_id = Account.objects.filter(username=temp_username).values_list()[0][0]
    username = Account.objects.filter(username=temp_username).values_list()[0][1]
    nickname = Account.objects.filter(username=temp_username).values_list()[0][3]
    studentId = Account.objects.filter(username=temp_username).values_list()[0][4]
    position = Account.objects.filter(username=temp_username).values_list()[0][5]
    email = Account.objects.filter(username=temp_username).values_list()[0][6]
    if request.method == 'POST':
        new_username = request.POST['username']
        new_nickname = request.POST['nickname']
        new_studentId = request.POST['studentId']
        new_position = request.POST['position']
        new_email = request.POST['email']
        is_new_username = Account.objects.filter(username=new_username).values_list()
        is_new_studentId = Account.objects.filter(studentId=new_studentId).values_list()

        if is_new_username:
            if is_new_username[0][0] != user_id:
                messages.info(request, '이미 존재하는 아이디 입니다.')
                return redirect('profilechange')
        if is_new_studentId:
            if is_new_studentId[0][0] != user_id:
                messages.info(request, '이미 존재하는 학번 입니다.')
                return redirect('profilechange')

        new_account = Account.objects.get(id=user_id)
        new_account.username = new_username
        new_account.nickname = new_nickname
        new_account.studentId = new_studentId
        new_account.position = new_position
        new_account.email = new_email
        new_account.save()

        user = request.user
        user.username = new_username
        user.save()
        return redirect('/KWEB211/')

    else:
        return render(request, 'KWEB211/profilechange.html', {
            'username': username,
            'nickname': nickname,
            'studentId': studentId,
            'position': position,
            'email': email,
        })