from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from datetime import date
from .mailer import send_email

# Create your views here.
def indexPageView(request,semester_id=None):
    if(semester_id == None):
        today = date.today()
        month = today.month
        if(1 <= month <= 4):
            season = Season.objects.get(name='Winter')
        elif(5 <= month <= 8):
            season = Season.objects.get(name='Spring/Summer')
        elif(9 <= month <= 12):
            season = Season.objects.get(name='Fall')
        semester = Semester.objects.get(year=today.year, season__id=season.id)
        semester_id = semester.id
    else:
        semester = Semester.objects.get(pk=semester_id)
    employments = Semester.objects.get(pk=semester_id).employment_set.all()
    context = {
        'employments': employments,
        'semester': semester,
        'semesters': Semester.objects.all(),
    }
    return render(request, 'index.html', context)

def reportsPageView(request):
    return render(request, 'reports.html')

def notificationsPageView(request):
    return render(request, 'notifications.html')

def testPageView(request):
    return render(request, 'test.html')

def createStudentPageView(request):
    if(request.method=="POST"):
        person_form = PersonForm(request.POST, prefix="person")
        student_form = StudentForm(request.POST, prefix="student")
        if(person_form.is_valid() and student_form.is_valid()):
            person = person_form.save()
            student_form.instance.person_id = person.pk
            student = student_form.save()
            return redirect('index')
    else:
        person_form, student_form = PersonForm(prefix="person"), StudentForm(prefix="student")

    context = {
        'title': 'Create New Student',
        'forms': [person_form, student_form],
    }
    return render(request, 'form.html', context)

# the edit views are very similar to the create views
# and could probably be consolidated into a single view
# but my brain is too small to figure it out right now
def editStudentPageView(request, person_id):
    student = get_object_or_404(Student, pk=person_id)
    if(request.method=="POST"):
        person_form = PersonForm(request.POST, prefix="person", instance=student.person)
        student_form = StudentForm(request.POST, prefix="student", instance=student)
        if(person_form.is_valid() and student_form.is_valid()):
            person = person_form.save()
            student_form.instance.person_id = person.pk
            student = student_form.save()

            return redirect('index')
    else:
        person_form, student_form = PersonForm(prefix="person", instance=student.person), StudentForm(prefix="student", instance=student)

    context = {
        'title': 'Update Student',
        'forms': [person_form, student_form],
        'delete_url': f'/students/delete/{person_id}'
    }
    return render(request, 'form.html', context)

def deleteStudentPageView(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    person.delete()
    return redirect("index")

def createInstructorPageView(request):
    if(request.method=="POST"):
        person_form = PersonForm(request.POST, prefix="person")
        instructor_form = InstructorForm(request.POST, prefix="instructor")
        if(person_form.is_valid() and instructor_form.is_valid()):
            person = person_form.save()
            instructor_form.instance.person_id = person.pk
            instructor = instructor_form.save()
            return redirect('index')
    else:
        person_form, instructor_form = PersonForm(prefix="person"), InstructorForm(prefix="instructor")

    context = {
        'title': 'Create New Instructor',
        'forms': [person_form, instructor_form]
    }
    return render(request, 'form.html', context)

def editInstructorPageView(request, person_id):
    instructor = get_object_or_404(Instructor, pk=person_id)
    if(request.method=="POST"):
        person_form = PersonForm(request.POST, prefix="person", instance=instructor.person)
        instructor_form = InstructorForm(request.POST, prefix="instructor", instance=instructor)
        if(person_form.is_valid() and instructor_form.is_valid()):
            person = person_form.save()
            instructor_form.instance.person_id = person.pk
            instructor = instructor_form.save()
            return redirect('index')
    else:
        person_form, instructor_form = PersonForm(prefix="person", instance=instructor.person), InstructorForm(prefix="instructor", instance=instructor)

    context = {
        'title': 'Update Instructor',
        'forms': [person_form, instructor_form],
        'delete_url': f'/instructors/delete/{person_id}'
    }
    return render(request, 'form.html', context)

def deleteInstructorPageView(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    person.delete()
    return redirect("index")

def createEmploymentPageView(request):
    if(request.method == "POST"):
        employment_form = CreateEmploymentForm(request.POST, prefix="employment")
        if(employment_form.is_valid()):
            employment = employment_form.save()
            return redirect('index')
    else:
        employment_form = CreateEmploymentForm(prefix="employment")
    
    context = {
        'title': 'Create New Employment',
        'forms': [employment_form],
    }
    return render(request, 'form.html', context)

def editEmploymentPageView(request, employment_id):
    employment = get_object_or_404(Employment, pk=employment_id)
    if(request.method == "POST"):
        employment_form = UpdateEmploymentForm(request.POST, prefix="employment", instance=employment)
        if(employment_form.is_valid()):

            new_workauth_value = employment_form.cleaned_data['work_auth_received']
            previous_workauth_value = Employment.objects.get(pk=employment_id).work_auth_received

            employment = employment_form.save()

            # if previously NOT authorized but NOW authorized, send email
            if(new_workauth_value and not previous_workauth_value):
                send_email(
                    f'You are authorized to work',
                    f'{employment.student.person.full_name}, you are authorized to work as a {employment.position_type} for {employment.supervisor.person.full_name}. Have fun!',
                    'byu_information_systems_fake@fake.com',
                    [employment.student.person.email]
                )

            return redirect('index')
    else:
        employment_form = UpdateEmploymentForm(prefix="employment", instance=employment)
    
    context = {
        'title': 'Update Employment',
        'forms': [employment_form],
        'delete_url': f'/employments/delete/{employment_id}'
    }
    return render(request, 'form.html', context)

def deleteEmploymentPageView(request, employment_id):
    employment = get_object_or_404(Person, pk=employment_id)
    employment.delete()
    return redirect("index")