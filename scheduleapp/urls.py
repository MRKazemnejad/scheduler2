from django.urls import path
from scheduleapp import views



app_name='scheduleapp'

urlpatterns = [

    path('',views.dashboard,name='dashboard'),
    path('newtask/',views.newtask,name='newtask'),
    path('newtask_submit/',views.newtask_submit,name='newtask_submit'),
    path('currenttask/',views.currenttask,name='currenttask'),
    path('finishtask/<int:id>',views.finishtask,name='finishtask'),
    path('alltask/',views.alltask,name='alltask'),
    path('searchnewtask/',views.searchnewtask,name='searchnewtask'),
    path('searchalltask/',views.searchalltask,name='searchalltask'),
    path('calender/',views.calender,name='calender'),

    path('taskdetails/<int:id>/<str:part>',views.taskdetails,name='taskdetails'),

    path('printexcel/<int:id>',views.printexcel,name='printexcel'),
    path('printpdf/<int:id>',views.printpdf,name='printpdf'),

    path('desktop/',views.desktop,name='desktop'),
    path('taskprogresspart/<int:taskcode>',views.taskprogresspart,name='taskprogresspart'),
    path('currenttaskcmplt/<int:taskcode>',views.currenttaskcmplt,name='currenttaskcmplt'),

    path('currenttaskcmplt_submit/<int:taskcode>',views.currenttaskcmplt_submit,name='currenttaskcmplt_submit'),

    path('currenttaskdelete/<int:taskcode>/<int:id>',views.currenttaskdelete,name='currenttaskdelete'),

    path('taskdelete/<int:id>',views.taskdelete,name='taskdelete'),

    path('report/',views.report,name='report'),

    path('loadimages/',views.loadimages,name='loadimages'),


    path('executerList/',views.executerList,name='executerList'),

    path('notification/',views.notification,name='notification'),
    path('notification_details/<int:id>',views.notification_details,name='notification_details'),
    path('notifications/',views.notifications,name='notifications'),


    path('settings/',views.settings,name='settings'),
    path('addexecuter/',views.addexecuter,name='addexecuter'),
    path('newexecuter_submit/',views.newexecuter_submit,name='newexecuter_submit'),
    path('deleteexecuter/',views.deleteexecuter,name='deleteexecuter'),
    path('deleteexecuter_submit/',views.deleteexecuter_submit,name='deleteexecuter_submit'),

    path('newaccount/',views.newaccount,name='newaccount'),

    path('employeealltask/',views.employeealltask,name='employeealltask'),




]