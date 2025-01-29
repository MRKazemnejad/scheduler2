import json
import pathlib
import traceback

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect

from scheduleapp.models import executer, task, taskprogress, Image,Notification
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from scheduleapp.utility import enddateCal, remaindate
import sweetify
import random
import time
import os
from pathlib import Path
from scheduleapp.forms import AttachedFile
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test



@login_required
def dashboard(request):
    user = request.user



    # if user.has_perm('scheduleapp.view_manager') and user.has_perm('scheduleapp.view_employee'):
    if user.has_perm('scheduleapp.view_manager'):
        request.session['master_permission'] = True
        context = {'segment': 'dashboard'}
        return render(request, 'scheduleapp/home/index.html', context)

    elif user.has_perm('scheduleapp.view_employee'):
        request.session['employee_permission'] = True

        #choose user and its id
        data = task.objects.all().order_by('startdate_store')
        context = {'segment': 'alltaskemployee','data':data}
        return render(request, 'scheduleapp/home/employeealltask.html', context)

    else:
        request.session['master_permission'] = False
        request.session['employee_permission'] = False
        context = {'segment': 'dashboard'}
        return render(request, 'scheduleapp/home/index.html', context)


@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def newtask(request):
    context = {'segment': 'newtask'}
    return render(request, 'scheduleapp/home/newtask.html', context)


@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def newtask_submit(request):
    value = {}
    value1 = {}

    if request.method == 'POST':
        try:
            executer_id = request.POST.get('executer')
            if executer_id == '0':
                raise Exception('executer can not be empty')
            execute_name = executer.objects.filter(exe_code=executer_id).values_list()
            startdate = request.POST.get('from_date')
            remaindate = request.POST.get('remain_date')
            pariority = request.POST.get('priority')
            activity_sub = request.POST.get('activity_sub')
            activity_desc = request.POST.get('activity_desc')

            enddate, startdate_en, enddate_en = enddateCal(startdate, remaindate)

            # ************************************ in task table ***************************************
            # value['id']=None
            random_code = random.randint(1, 100000)

            value['system_code'] = random_code
            value['executer'] = execute_name[0][1]
            value['executer_code'] = executer_id
            value['startdate'] = startdate
            value['preiod'] = remaindate
            value['enddate'] = executer
            value['pariority'] = pariority
            value['enddate'] = enddate
            value['task_sub'] = activity_sub
            value['task_desc'] = activity_desc
            value['active'] = True
            value['is_seen'] = False
            value['startdate_store'] = startdate_en
            value['enddate_store'] = enddate_en
            new_obj = task(**value)
            new_obj.save()

            # ***************************************** in taskprogress table ***************************
            data = task.objects.filter(system_code=random_code).values()
            today_date = JalaliDate.today()

            value1['executer'] = data[0]['executer']
            value1['executer_code'] = int(data[0]['executer_code'])
            value1['startdate'] = data[0]['startdate']
            value1['enddate'] = data[0]['enddate']
            value1['finishdate'] = data[0]['finishdate']
            value1['enterydate'] = today_date
            value1['preiod'] = data[0]['preiod']
            value1['taskcode'] = data[0]['id']
            value1['pariority'] = data[0]['pariority']
            value1['task_sub'] = data[0]['task_sub']
            value1['task_desc'] = data[0]['task_desc']
            value1['active'] = True

            new_obj1 = taskprogress(**value1)
            new_obj1.save()

            sweetify.success(request, 'اطلاعات با موفقیت ذخیره گردید', persistent='تایید', timer='3000')

        except:
            traceback.print_exc()
            sweetify.sweetalert(request, 'خطا در ذخیره سازی اطلاعات', persistent='تایید', timer='3000')

    context = {'segment': 'newtask'}
    return render(request, 'scheduleapp/home/newtask.html', context)


@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def currenttask(request):
    data = task.objects.filter(active=True, is_seen=False).order_by('startdate_store')

    for row in data:
        remain_date = remaindate(row.enddate_store)
        task.objects.filter(id=row.id).update(remain_date=remain_date)

    data = task.objects.filter(active=True, is_seen=False).order_by('startdate_store')
    context = {'segment': 'currenttask', 'data': data}
    return render(request, 'scheduleapp/home/currentask.html', context)


@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def finishtask(request, id):
    active = False
    is_seen = True
    task.objects.filter(id=id).update(active=active, is_seen=is_seen)
    data = task.objects.filter(active=True, is_seen=False)
    sweetify.success(request, 'اطلاعات با موفقیت ذخیره گردید', persistent='تایید', timer='3000')
    context = {'segment': 'currenttask', 'data': data}
    return render(request, 'scheduleapp/home/currentask.html', context)


@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def alltask(request):
    data = task.objects.all().order_by('startdate_store')
    context = {'segment': 'alltask', 'data': data}
    return render(request, 'scheduleapp/home/alltask.html', context)


def executerList(request):
    executerList = []
    executer_code = []

    data = executer.objects.order_by().values('exe_name', 'exe_code').distinct()

    for row in data:
        executerList.append(row['exe_name'])
        executer_code.append(row['exe_code'])

    return JsonResponse(data={
        'executer': executerList,
        'executer_code': executer_code,
    })


@login_required
@permission_required('scheduleapp.view_employee', raise_exception=True)
def searchnewtask(request):
    filter_params = {}
    if request.method == 'POST':
        executer_id = request.POST.get('executer_srch')
        startdate_raw = request.POST.get('startdate_srch')
        pariority_raw = request.POST.get('pariority_srch')

        if executer_id == '0':
            pass
        else:

            filter_params['executer_code__icontains'] = executer_id

        if startdate_raw == '':
            pass
        else:

            date_change_slash = startdate_raw.replace('/', '-')
            year = int(date_change_slash[:4])
            month = int(date_change_slash[5:7])
            day = int(date_change_slash[8:10])
            startdate_en = JalaliDate(year, month, day).to_gregorian()

            filter_params['startdate_store__gte'] = startdate_en

        if pariority_raw == '0':
            pass
        else:
            filter_params['pariority__icontains'] = pariority_raw

        filter_params['active'] = True

    data = task.objects.filter(**filter_params)
    context = {'segment': 'currenttask', 'data': data}
    return render(request, 'scheduleapp/home/currentask.html', context)


@login_required
@permission_required('scheduleapp.view_employee', raise_exception=True)
def searchalltask(request):
    filter_params = {}
    if request.method == 'POST':
        executer_id = request.POST.get('executer_srch')
        startdate_raw = request.POST.get('startdate_srch')
        pariority_raw = request.POST.get('pariority_srch')

        if executer_id == '0':
            pass
        else:

            filter_params['executer_code__icontains'] = executer_id

        if startdate_raw == '':
            pass
        else:

            date_change_slash = startdate_raw.replace('/', '-')
            year = int(date_change_slash[:4])
            month = int(date_change_slash[5:7])
            day = int(date_change_slash[8:10])
            startdate_en = JalaliDate(year, month, day).to_gregorian()

            filter_params['startdate_store__gte'] = startdate_en

        if pariority_raw == '0':
            pass
        else:
            filter_params['pariority__icontains'] = pariority_raw

    data = task.objects.filter(**filter_params)
    context = {'segment': 'alltask', 'data': data}
    return render(request, 'scheduleapp/home/alltask.html', context)


@login_required
@permission_required('scheduleapp.view_employee', raise_exception=True)
def calender(request):
    context = {'segment': 'calender'}
    return render(request, 'scheduleapp/home/calender.html', context)


@login_required
@permission_required('scheduleapp.view_employee', raise_exception=True)
def taskdetails(request, id, part):
    data = taskprogress.objects.filter(taskcode=int(id))
    if part == 'currenttask':
        segment = 'currenttask'
    elif part == 'alltask':
        segment = 'alltask'

    # imgsrc='/Storage/100/1403-10-20/52.jpg'

    context = {'segment': segment, 'data': data, 'id': id}
    return render(request, 'scheduleapp/home/taskdetails.html', context)


@login_required
@permission_required('scheduleapp.view_employee', raise_exception=True)
def printexcel(request, id):
    from openpyxl import Workbook

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="details.xlsx"'

    # Add data from the model
    products = taskprogress.objects.filter(taskcode=id)

    # Add headers
    headers = ["کد", "مجری", "عنوان تسک", "شرح تسک",
               "تاریخ شروع", "تاریخ پایان", "مدت اجرا", "تاریخ انجام", "الویت", "وضعیت"]

    title = 'TASK DETAILS'
    wb = Workbook()
    ws = wb.active
    ws.title = title

    ws.append(headers)

    for product in products:
        if product.active:
            status = 'جاری'
        else:
            status = 'خاتمه'
        ws.append([product.taskcode, product.executer, product.task_sub, product.task_desc, product.startdate,
                   product.enddate, product.preiod, product.finishdate, product.pariority,
                   status])
    # Save the workbook to the HttpResponse
    wb.save(response)
    return response


@login_required
@permission_required('scheduleapp.view_employee', raise_exception=True)
def printpdf(request, id):
    response = FileResponse(generate_pdf_file(id),
                            as_attachment=True,
                            filename='book_catalog.pdf')
    return response



def generate_pdf_file(id):
    from io import BytesIO

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Create a PDF document
    books = taskprogress.objects.filter(taskcode=id)
    p.drawString(100, 750, "Book Catalog")

    y = 700
    for book in books:
        p.drawString(100, y, f"Title: {book.executer}")
        p.drawString(100, y - 20, f"Author: {book.task_sub}")
        p.drawString(100, y - 40, f"Year: {book.task_desc}")
        y -= 60

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer


@login_required
@permission_required('scheduleapp.view_employee', raise_exception=True)
def desktop(request):
    exe_code = '100'
    data = task.objects.filter(active=True, executer_code=exe_code)

    enddate_list = []

    for row in data:
        enddate_list.append(row.enddate)

    context = {'segment': 'desktop', 'data': data, 'enddate_list': json.dumps(enddate_list), 'code': exe_code}
    return render(request, 'scheduleapp/home/desktop.html', context)


@login_required
@permission_required('scheduleapp.view_employee', raise_exception=True)
def taskprogresspart(request, taskcode):
    tasklist = taskprogress.objects.filter(taskcode=taskcode)
    context = {'segment': 'desktop', 'data': tasklist, 'taskcode': taskcode}
    return render(request, 'scheduleapp/home/mytaskprogresslist.html', context)


@login_required
@permission_required('scheduleapp.view_employee', raise_exception=True)
def currenttaskcmplt(request, taskcode):
    newtaskcode = taskcode
    form = AttachedFile()

    context = {'segment': 'desktop', 'taskcode': newtaskcode, 'form': form}
    return render(request, 'scheduleapp/home/completetask.html', context)


@login_required
@permission_required('scheduleapp.view_employee', raise_exception=True)
def currenttaskcmplt_submit(request,taskcode):

    value = {}

    tasklist = task.objects.filter(id=taskcode).order_by('id').values().last()


    if request.method == 'POST':
        taskprog = request.POST.get('task_prog')
        activity_date = request.POST.get('activity_date')
        activity_desc = request.POST.get('activity_desc')
        finishtask = request.POST.get('finishtask')

        images_check = request.FILES.getlist('images')
        if images_check:
            attach = True
        else:
            attach = False

        if finishtask == 'on':
            prog = 100
            finishdate = activity_date
        else:
            prog = taskprog
            finishdate = ''

        value['id'] = None
        value['executer'] = tasklist['executer']
        value['executer_code'] = int(tasklist['executer_code'])
        value['startdate'] = tasklist['startdate']
        value['enddate'] = tasklist['enddate']

        value['finishdate'] = finishdate
        value['enterydate'] = activity_date
        value['preiod'] = tasklist['preiod']
        value['taskcode'] = taskcode
        value['pariority'] = tasklist['pariority']
        value['task_sub'] = tasklist['task_sub']
        value['task_desc'] = activity_desc
        value['progress'] = prog
        value['active'] = True
        value['attachment'] = attach

        new_obj1 = taskprogress(**value)
        new_obj1.save()

    # *************************************************************************************
        images = request.FILES.getlist('images')

        for image in images:
            img = Image(product=new_obj1, image=image)
            img.save()
            print('saved')

     # *************************************************************************************

        task.objects.filter(id=taskcode).update(progress=prog)

     # ********************************** Notification insertion **************************
        notiff=Notification(notif_code=new_obj1,notif=tasklist['task_sub'],exe_code=int(tasklist['executer_code']),is_read=False)
        notiff.save()

    # ********************************************************************************
    tasklist = taskprogress.objects.filter(taskcode=taskcode)
    context = {'segment': 'desktop', 'data': tasklist, 'taskcode': taskcode}
    # return render(request, 'scheduleapp/home/mytaskprogresslist.html', context)
    return redirect('scheduleapp:desktop')





@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def currenttaskdelete(request, taskcode, id):
    try:
        exe_code = taskprogress.objects.filter(taskcode=taskcode, id=id).values()

        code = exe_code[0]['executer_code']
        date = exe_code[0]['enterydate']
        date_convert = str(date).replace('/', '-')
        filename = str(id) + '.' + 'jpg'
        BASE_DIR = Path(__file__).resolve().parent.parent / 'Storage' / code / date_convert
        path = os.path.join(BASE_DIR, filename)
        deleteFile(path)
        taskprogress.objects.filter(taskcode=taskcode, id=id).delete()
        sweetify.success(request, 'تسک مورد نظر با موفقیت حذف گردید.', persistent='تایید', timer='3000')

    except:
        traceback.print_exc()
        sweetify.sweetalert(request, 'خطا در حذف اطلاعات', persistent='تایید', timer='3000')

    tasklist = taskprogress.objects.filter(taskcode=taskcode)
    context = {'segment': 'desktop', 'data': tasklist, 'taskcode': taskcode}
    return render(request, 'scheduleapp/home/mytaskprogresslist.html', context)


@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def taskdelete(request, id):
    try:
        task.objects.filter(id=id).delete()
        taskprogress.objects.filter(taskcode=id).delete()

        data = task.objects.filter(active=True)
        sweetify.success(request, 'تسک مورد نظر با موفقیت حذف گردید.', persistent='تایید', timer='3000')
        context = {'segment': 'currenttask', 'data': data}
        return render(request, 'scheduleapp/home/currentask.html', context)
    except:
        traceback.print_exc()
        data = task.objects.filter(active=True)
        sweetify.sweetalert(request, 'خطا در حذف اطلاعات', persistent='تایید', timer='3000')
        context = {'segment': 'currenttask', 'data': data}
        return render(request, 'scheduleapp/home/currentask.html', context)


def change_extension(file_path, new_extension, id):
    base_name, _ = os.path.splitext(file_path)
    new_file_path = base_name + new_extension

    taskprogress.objects.filter(id=id).update(imgsrc=new_file_path)
    print(f'new fiel path:{new_file_path}')

    os.rename(file_path, new_file_path)


def handle_uploaded_fileok(f, id, date, code):
    qc_date = date
    qc_date_convert = str(qc_date).replace('/', '-')
    BASE_DIR = Path(__file__).resolve().parent.parent / 'Storage' / code
    # path = f'/static/storage/{code}/{qc_date_convert}'

    # BASE_DIR = 'C:/Users/M.kazemnezhad/Desktop/New folder (8)/scheduler2/Storage'
    directory = f"{qc_date_convert}/"
    path = os.path.join(BASE_DIR, directory)

    if os.path.exists(path):
        print('path exist')
    else:
        os.mkdir(path)

    file_name = path + '/' + str(id)

    with open(file_name, 'wb+') as destination:
        # function to return the file extension
        file = str(f)
        file_extension = pathlib.Path(file).suffix

        for chunk in f.chunks():
            destination.write(chunk)
    time.sleep(1)
    change_extension(file_name, file_extension, id)
    return 'ok'
@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def report(request):
    context = {'segment': 'report'}
    return render(request, 'scheduleapp/home/report.html', context)



@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def report_submit(request):


    context = {'segment': 'report'}
    return render(request, 'scheduleapp/home/report_submit.html', context)


def deleteFile(filepath):
    os.remove(filepath)
    print('file deleted')


def loadimages(request):
    data = []
    # image_list=[]
    if request.method == 'GET':
        code = eval(request.GET.get('id'))

    try:
        images = Image.objects.filter(product_id=int(code))
    except Image.DoesNotExist:
        images = None

    for image in images:
        data.append({'url': image.image.url})
    return JsonResponse({'images': data})

@login_required
# @permission_required('scheduleapp.view_manager', raise_exception=True)
def notification(request):
    data_list=[]
    data=Notification.objects.filter(is_read=False).values()
    for row in data:
        data_list.append(row)

    return JsonResponse(data={
        'notif': data_list,
    })

@login_required
# @permission_required('scheduleapp.view_manager', raise_exception=True)
def notification_details(request,id):

    Notification.objects.filter(notif_code_id=id).update(is_read=True)
    data = taskprogress.objects.filter(id=id)

    context = {'segment': 'notifications', 'data': data}
    return render(request, 'scheduleapp/home/notif_details.html', context)

@login_required
# @permission_required('scheduleapp.view_manager', raise_exception=True)
def notifications(request):
    notif=[]
    not_seen=Notification.objects.filter(is_read=False)
    for row in not_seen:
        id=row.notif_code_id
        data = taskprogress.objects.filter(id=id).values_list()[0]
        notif.append(data)

    Notification.objects.update(is_read=True)

    context = {'segment': 'notifications', 'data': notif}
    return render(request, 'scheduleapp/home/allnotifications.html', context)

@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def settings(request):

    context = {'segment': 'settings'}
    return render(request, 'scheduleapp/home/settings.html', context)

@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def addexecuter(request):

    context = {'segment': 'settings'}
    return render(request, 'scheduleapp/home/addexecuter.html', context)

@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def newexecuter_submit(request):
    value={}
    if request.method=='POST':
        try:
            name=request.POST.get('exe_name')
            pos=request.POST.get('pos')
            exe_code=executer.objects.all().last()
            new_code=int(exe_code.exe_code)+1
            id=exe_code.id+1

            if pos=='1':
                pos_str='مدیر'
            elif pos=='2':
                pos_str = 'رییس گروه'
            elif pos=='3':
                pos_str = 'کارشناس'
            elif pos=='4':
                pos_str = 'خدمات'

            value['id']=id
            value['exe_name']=name
            value['exe_post']=pos_str
            value['exe_code']=str(new_code)


            obj=executer(**value)
            obj.save()

            context = {'segment': 'settings'}
            sweetify.success(request, 'مجری جدید با موفقیت اضافه گردید.', persistent='تایید', timer='3000')
            return render(request, 'scheduleapp/home/addexecuter.html', context)

        except:
            traceback.print_exc()
            sweetify.sweetalert(request, 'خطا در افزودن مجری', persistent='تایید', timer='3000')
            context = {'segment': 'settings'}
            return render(request, 'scheduleapp/home/addexecuter.html', context)


@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def deleteexecuter(request):

    context = {'segment': 'settings'}
    return render(request, 'scheduleapp/home/deleteexecuter.html', context)




@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def deleteexecuter_submit(request):
    try:
        if request.method=='POST':
            executer_id = request.POST.get('executer')

            executer.objects.filter(exe_code=executer_id).delete()

            sweetify.success(request, 'مجری با موفقیت از لیست حذف گردید.', persistent='تایید', timer='3000')
            context = {'segment': 'settings'}
            return render(request, 'scheduleapp/home/deleteexecuter.html', context)

    except:
        traceback.print_exc()
        sweetify.sweetalert(request, 'خطا در حذف مجری', persistent='تایید', timer='3000')
        context = {'segment': 'settings'}
        return render(request, 'scheduleapp/home/deleteexecuter.html', context)


@login_required
def newaccount(request):
    pass

@login_required
@permission_required('scheduleapp.view_employee', raise_exception=True)
def employeealltask(request):

    data = task.objects.all().order_by('startdate_store')
    context = {'segment': 'alltaskemployee', 'data': data}
    return render(request, 'scheduleapp/home/employeealltask.html', context)

@login_required
@permission_required('scheduleapp.view_manager', raise_exception=True)
def subjectList(request):
    subjectList = []
    subject_code = []

    data =task.objects.all().values()

    for row in data:
        subjectList.append(row['task_sub'])
        subject_code.append(row['id'])


    return JsonResponse(data={
        'subjectList': subjectList,
        'subject_code': subject_code,
    })








