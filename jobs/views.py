import csv
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from .models import JobApplication
from .forms import ApplicationForm

def signup(request):
    form=UserCreationForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        login(request,form.save())
        return redirect('dashboard')
    return render(request,'registration/signup.html',{'form':form})

@login_required
def dashboard(request):
    all_jobs=JobApplication.objects.filter(user=request.user)
    jobs=all_jobs
    q=request.GET.get('q','').strip()
    status=request.GET.get('status','')
    if q: jobs=jobs.filter(Q(company__icontains=q)|Q(role__icontains=q))
    if status: jobs=jobs.filter(status=status)
    stats=[{'label':label,'count':all_jobs.filter(status=value).count(),'status':value} for value,label in JobApplication.Status.choices]
    return render(request,'jobs/dashboard.html',{'applications':jobs,'total':all_jobs.count(),'stats':stats,'q':q,'selected_status':status,'statuses':JobApplication.Status.choices,'upcoming':all_jobs.filter(status='interview',interview_at__gte=timezone.now()).order_by('interview_at')[:5]})

@login_required
def application_form(request,pk=None):
    obj=get_object_or_404(JobApplication,pk=pk,user=request.user) if pk else None
    form=ApplicationForm(request.POST or None,instance=obj)
    if request.method=='POST' and form.is_valid():
        job=form.save(commit=False)
        job.user=request.user
        job.save()
        messages.success(request,'Application saved successfully.')
        return redirect('dashboard')
    return render(request,'jobs/form.html',{'form':form,'editing':obj is not None})

@login_required
def delete_application(request,pk):
    obj=get_object_or_404(JobApplication,pk=pk,user=request.user)
    if request.method=='POST':
        obj.delete()
        messages.success(request,'Application deleted.')
        return redirect('dashboard')
    return render(request,'jobs/delete.html',{'application':obj})

@login_required
def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="applications.csv"'
    writer=csv.writer(response)
    writer.writerow(['Company','Role','Salary','Status','Applied date','Interview','Job link','Notes'])
    def safe(value):
        text=str(value or '')
        return "'"+text if text.lstrip().startswith(('=','+','-','@')) else text
    for j in JobApplication.objects.filter(user=request.user):
        writer.writerow([safe(v) for v in [j.company,j.role,j.salary,j.get_status_display(),j.applied_date,j.interview_at,j.job_link,j.notes]])
    return response
