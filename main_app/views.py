from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date

from django.contrib import messages
from django.contrib.auth.models import User , auth
from .models import patient , doctor , diseaseinfo , consultation ,rating_review
from chats.models import Chat,Feedback

import joblib as jb
model = jb.load('trained_model')


def home(request):

  if request.method == 'GET':
        
      if request.user.is_authenticated:
        return render(request,'homepage/index.html')

      else :
        return render(request,'homepage/index.html')



   

       


def admin_ui(request):

    if request.method == 'GET':

      if request.user.is_authenticated:

        auser = request.user
        Feedbackobj = Feedback.objects.all()

        return render(request,'admin/admin_ui/admin_ui.html' , {"auser":auser,"Feedback":Feedbackobj})

      else :
        return redirect('home')



    if request.method == 'POST':

       return render(request,'patient/patient_ui/profile.html')





def patient_ui(request):

    if request.method == 'GET':

      if request.user.is_authenticated:

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)

        return render(request,'patient/patient_ui/profile.html' , {"puser":puser})

      else :
        return redirect('home')



    if request.method == 'POST':

       return render(request,'patient/patient_ui/profile.html')

       


def pviewprofile(request, patientusername):

    if request.method == 'GET':

          puser = User.objects.get(username=patientusername)

          return render(request,'patient/view_profile/view_profile.html', {"puser":puser})




def checkdisease(request):

  diseaselist=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction','Peptic ulcer diseae','AIDS','Diabetes ',
  'Gastroenteritis','Bronchial Asthma','Hypertension ','Migraine','Cervical spondylosis','Paralysis (brain hemorrhage)',
  'Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
  'Hepatitis E', 'Alcoholic hepatitis','Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
  'Heart attack', 'Varicose veins','Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
  'Arthritis', '(vertigo) Paroymsal  Positional Vertigo','Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']


  symptomslist=['Ng???a','Ph??t ban da','Ph??t ban n???t s???n tr??n da','H???t h??i li??n t???c','R??ng m??nh','???n l???nh','??au kh???p',
  '??au d??? d??y','??? n??ng','Lo??t l?????i','Teo c??','N??n ??i','??i ti???u bu???t','??i ti???u ra m??u',
  'M???t m???i','T??ng c??n','Lo l???ng','Tay ch??n l???nh','T??m tr???ng thay ?????i th???t th?????ng','S???t c??n','B???n ch???n','Th??? ??',
  'N???i n???t ????? trong khoang mi???ng','M???c ???????ng b???t th?????ng','Ho','S???t cao','M???t tr??ng','Kh?? th???','????? m??? h??i',
  'M???t n?????c','Kh?? ti??u','??au ?????u','Da v??ng','N?????c ti???u s???m m??u','Bu???n n??n','Ch??n ??n','??au sau m???t',
  '??au l??ng','T??o b??n','??au b???ng','Ti??u ch???y','S???t nh???','N?????c ti???u v??ng',
  'V??ng m???t','Suy gan c???p t??nh','Qu?? t???i ch???t l???ng','S??ng d??? d??y',
  'N???t b???ch huy???t s??ng l??n','Kh?? ch???u','M??? v?? m??o m???t','?????m','K??ch ???ng c??? h???ng',
  '????? m???t','Nh???c xoang','Ch???y n?????c m??i','Ngh???t m??i','??au ng???c','Y???u tay ch??n',
  'Tim ?????p nhanh','??au ru???t khi di chuy???n','??au ??? v??ng h???u m??n','M??u trong ph??n',
  'K??ch ???ng h???u m??n','??au c???','Ch??ng m???t','Chu???t r??t','B???m t??m','B??o ph??','S??ng ch??n',
  'Ph?? m???ch m??u','S??ng m???t v?? m???t','Tuy???n gi??p to','M??ng tay d??? g??y',
  'S??ng c??nh tay v?? b??n tay','Th??m ??n','Ngo???i t??nh','Kh?? v?? n??? m??i',
  'Lo???n ng??n','??au ?????u g???i','??au kh???p h??ng','Y???u c??','C???ng c???','S??ng kh???p',
  'Di chuy???n kh??ng tho???i m??i','Ch??ng m???t','M???t th??ng b???ng','??i kh??ng v???ng',
  'Y???u m???t ph???n c?? th???','M???t m??i h??i','Kh?? ch???u b??ng quang','N?????c ti???u c?? m??i',
  '????i d???t','?????y h??i','Ng???a trong','Nh??n gi???ng b??? nhi???m ?????c(Ph??t ban)',
  'Tr???m c???m','C??u k???nh','??au c??','M???t t???p trung','?????m ????? tr??n c?? th???','??au c?? b???ng',
  'Kinh nguy???t b???t th?????ng','M???ng da ?????i m??u','Ch???y n?????c m???t','??n nhi???u','Ti???u nhi???u','Ti???n s??? gia ????nh','C?? ?????m',
  '?????m n??u','Thi???u t???p trung','R???i lo???n th??? gi??c','Truy???n m??u',
  'Kim ti??m kh??ng kh??? tr??ng','H??n m??','Ch???y m??u d??? d??y','Tr?????ng b???ng',
  'S??? d???ng th???c u???ng c?? c???n','T??ng th??? t??ch m??u','M??u trong ?????m','Gi??n t??nh m???ch',
  '????nh tr???ng ng???c','??au ?????n khi di chuy???n','M???n c?? m???','M???n ?????u ??en','S???o l??m','L???t da',
  'Ti???p x??c nhi???u v???i b???c','R??? m??ng tay','V???y n???n','M???n n?????c','Da ????? xung quanh m??i',
  'M???n ch???y d???ch v??ng']

  alphabaticsymptomslist = sorted(symptomslist)

  


  if request.method == 'GET':
    
     return render(request,'patient/checkdisease/checkdisease.html', {"list2":alphabaticsymptomslist})




  elif request.method == 'POST':
      
      inputno = int(request.POST["noofsym"])
      print(inputno)
      if (inputno == 0 ) :
          return JsonResponse({'predicteddisease': "none",'confidencescore': 0 })
  
      else :

        psymptoms = []
        psymptoms = request.POST.getlist("symptoms[]")
       
        print(psymptoms)

        testingsymptoms = []
        for x in range(0, len(symptomslist)):
          testingsymptoms.append(0)

        for k in range(0, len(symptomslist)):

          for z in psymptoms:
              if (z == symptomslist[k]):
                  testingsymptoms[k] = 1


        inputtest = [testingsymptoms]

        print(inputtest)
      

        predicted = model.predict(inputtest)
        print("predicted disease is : ")
        print(predicted)

        y_pred_2 = model.predict_proba(inputtest)
        confidencescore=y_pred_2.max() * 100
        print(" confidence score of : = {0} ".format(confidencescore))

        confidencescore = format(confidencescore, '.0f')
        predicted_disease = predicted[0]

        Rheumatologist = [  'Osteoarthristis','Arthritis']
       
        Cardiologist = [ 'Heart attack','Bronchial Asthma','Hypertension ']
       
        ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo','Hypothyroidism' ]

        Orthopedist = []

        Neurologist = ['Varicose veins','Paralysis (brain hemorrhage)','Migraine','Cervical spondylosis']

        Allergist_Immunologist = ['Allergy','Pneumonia',
        'AIDS','Common Cold','Tuberculosis','Malaria','Dengue','Typhoid']

        Urologist = [ 'Urinary tract infection',
         'Dimorphic hemmorhoids(piles)']

        Dermatologist = [  'Acne','Chicken pox','Fungal infection','Psoriasis','Impetigo']

        Gastroenterologist = ['Peptic ulcer diseae', 'GERD','Chronic cholestasis','Drug Reaction','Gastroenteritis','Hepatitis E',
        'Alcoholic hepatitis','Jaundice','hepatitis A',
         'Hepatitis B', 'Hepatitis C', 'Hepatitis D','Diabetes ','Hypoglycemia']
         
        if predicted_disease in Rheumatologist :
           consultdoctor = "Rheumatologist"
           
        if predicted_disease in Cardiologist :
           consultdoctor = "Cardiologist"
           

        elif predicted_disease in ENT_specialist :
           consultdoctor = "ENT specialist"
     
        elif predicted_disease in Orthopedist :
           consultdoctor = "Orthopedist"
     
        elif predicted_disease in Neurologist :
           consultdoctor = "Neurologist"
     
        elif predicted_disease in Allergist_Immunologist :
           consultdoctor = "Allergist/Immunologist"
     
        elif predicted_disease in Urologist :
           consultdoctor = "Urologist"
     
        elif predicted_disease in Dermatologist :
           consultdoctor = "Dermatologist"
     
        elif predicted_disease in Gastroenterologist :
           consultdoctor = "Gastroenterologist"
     
        else :
           consultdoctor = "other"


        request.session['doctortype'] = consultdoctor 

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)

        stt = 0
        patient = puser.patient
        for s in range(41):
            if (predicted_disease == diseaselist[s]):
               stt = s
        vietnam_diseaselist=['Nhi???m n???m','D??? ???ng','GERD','??? m???t m??n t??nh','Ph???n ???ng thu???c','B???nh lo??t d??? d??y','AIDS','Ti???u ???????ng ',
         'Vi??m d??? d??y ru???t','Hen ph??? qu???n','T??ng huy???t ??p ','Ch???ng ??au n???a ?????u','Tho??i h??a ?????t s???ng c???','B???i li???t (xu???t huy???t n??o)',
         'Vi??m gan','S???t r??t','Th???y ?????u','S???t xu???t huy???t','Th????ng h??n','Vi??m gan A', 'Vi??m gan B', 'Vi??m gan C', 'Vi??m gan D',
         'Vi??m gan E', 'Vi??m gan do r?????u','B???nh lao', 'C???m l???nh th??ng th?????ng', 'Vi??m ph???i', 'B???nh tr?? l?????ng h??nh',
         '??au tim', 'Gi??n t??nh m???ch','Suy gi??p', 'C?????ng gi??p', 'H??? ???????ng huy???t', 'B???nh tho??i h??a kh???p',
         'Vi??m kh???p', 'Ch??ng m???t t?? th??? l??nh t??nh','M???n tr???ng c??', 'Nhi???m tr??ng ???????ng ti???t ni???u', 'V???y n???n', 'B???nh ch???c']
        diseasename = vietnam_diseaselist[stt]
        no_of_symp = inputno
        symptomsname = psymptoms
        confidence = confidencescore

        diseaseinfo_new = diseaseinfo(patient=patient,diseasename=diseasename,no_of_symp=no_of_symp,symptomsname=symptomsname,confidence=confidence,consultdoctor=consultdoctor)
        diseaseinfo_new.save()
        
        request.session['diseaseinfo_id'] = diseaseinfo_new.id

        print("disease record saved sucessfully.............................")

        return JsonResponse({'predicteddisease': diseasename ,'confidencescore':confidencescore , "consultdoctor": consultdoctor})
   


   
    



   





def pconsultation_history(request):

    if request.method == 'GET':

      patientusername = request.session['patientusername']
      puser = User.objects.get(username=patientusername)
      patient_obj = puser.patient
        
      consultationnew = consultation.objects.filter(patient = patient_obj)
      
    
      return render(request,'patient/consultation_history/consultation_history.html',{"consultation":consultationnew})


def dconsultation_history(request):

    if request.method == 'GET':

      doctorusername = request.session['doctorusername']
      duser = User.objects.get(username=doctorusername)
      doctor_obj = duser.doctor
        
      consultationnew = consultation.objects.filter(doctor = doctor_obj)
      
    
      return render(request,'doctor/consultation_history/consultation_history.html',{"consultation":consultationnew})



def doctor_ui(request):

    if request.method == 'GET':

      doctorid = request.session['doctorusername']
      duser = User.objects.get(username=doctorid)

    
      return render(request,'doctor/doctor_ui/profile.html',{"duser":duser})



      


def dviewprofile(request, doctorusername):

    if request.method == 'GET':

         
         duser = User.objects.get(username=doctorusername)
         r = rating_review.objects.filter(doctor=duser.doctor)
       
         return render(request,'doctor/view_profile/view_profile.html', {"duser":duser, "rate":r} )








       
def  consult_a_doctor(request):


    if request.method == 'GET':

        
        doctortype = request.session['doctortype']
        print(doctortype)
        dobj = doctor.objects.all()
        #dobj = doctor.objects.filter(specialization=doctortype)


        return render(request,'patient/consult_a_doctor/consult_a_doctor.html',{"dobj":dobj})

   


def  make_consultation(request, doctorusername):

    if request.method == 'POST':
       

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        patient_obj = puser.patient
        
        
        #doctorusername = request.session['doctorusername']
        duser = User.objects.get(username=doctorusername)
        doctor_obj = duser.doctor
        request.session['doctorusername'] = doctorusername


        diseaseinfo_id = request.session['diseaseinfo_id']
        diseaseinfo_obj = diseaseinfo.objects.get(id=diseaseinfo_id)

        consultation_date = date.today()
        status = "active"
        
        consultation_new = consultation( patient=patient_obj, doctor=doctor_obj, diseaseinfo=diseaseinfo_obj, consultation_date=consultation_date,status=status)
        consultation_new.save()

        request.session['consultation_id'] = consultation_new.id

        print("consultation record is saved sucessfully.............................")

         
        return redirect('consultationview',consultation_new.id)



def  consultationview(request,consultation_id):
   
    if request.method == 'GET':

   
      request.session['consultation_id'] = consultation_id
      consultation_obj = consultation.objects.get(id=consultation_id)

      return render(request,'consultation/consultation.html', {"consultation":consultation_obj })

   #  if request.method == 'POST':
   #    return render(request,'consultation/consultation.html' )





def rate_review(request,consultation_id):
   if request.method == "POST":
         
         consultation_obj = consultation.objects.get(id=consultation_id)
         patient = consultation_obj.patient
         doctor1 = consultation_obj.doctor
         rating = request.POST.get('rating')
         review = request.POST.get('review')

         rating_obj = rating_review(patient=patient,doctor=doctor1,rating=rating,review=review)
         rating_obj.save()

         rate = int(rating_obj.rating_is)
         doctor.objects.filter(pk=doctor1).update(rating=rate)
         

         return redirect('consultationview',consultation_id)





def close_consultation(request,consultation_id):
   if request.method == "POST":
         
         consultation.objects.filter(pk=consultation_id).update(status="closed")
         
         return redirect('home')






#-----------------------------chatting system ---------------------------------------------------


def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)

        consultation_id = request.session['consultation_id'] 
        consultation_obj = consultation.objects.get(id=consultation_id)

        c = Chat(consultation_id=consultation_obj,sender=request.user, message=msg)

        #msg = c.user.username+": "+msg

        if msg != '':            
            c.save()
            print("msg saved"+ msg )
            return JsonResponse({ 'msg': msg })
    else:
        return HttpResponse('Request must be POST.')



def chat_messages(request):
   if request.method == "GET":

         consultation_id = request.session['consultation_id'] 

         c = Chat.objects.filter(consultation_id=consultation_id)
         return render(request, 'consultation/chat_body.html', {'chat': c})


#-----------------------------chatting system ---------------------------------------------------


