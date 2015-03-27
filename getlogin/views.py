from django.shortcuts import render
from .forms import LoginPairForm 
from django.shortcuts import redirect
import subprocess
from subprocess import CalledProcessError
from .models import LoginPair
from django.core.exceptions import ObjectDoesNotExist 
import shlex
import StringIO 

def home(request):

    ##############################
    # user already login and save its login info.  
    if request.method == "POST":
        form = LoginPairForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
             
            ##############################
            # check the existing account from old email server 
            try:
                thisLoginUser = LoginPair.objects.get(email=post.email)
                
            ##############################
            # no this user fr. old server, let user know you are invalid
            #    may be someone want to hack this system 
            except ObjectDoesNotExist as odne:
                return render(request, 'getlogin/main.html', {
                                                              'form': form,
                                                              'statusMsg': "your login email or password wrong, please try again !!!",
                                                              })
                
            ##############################
            # yes fr. old server, prepare the migration and let user know i will send you back a email when completed
    
            ##############################
            # keep its login info.
            thisLoginUser.pw = post.pw 
            thisLoginUser.save()
            
            ##############################
            # do the migration or send email to yan for manually migration
              
            ##############################
            # do a imapsync dry connection and chk how many msg to sync 
            oldHost = "202.177.26.104"
            oldUserName = thisLoginUser.email
            oldPw = thisLoginUser.pw
            newHost = "127.0.0.1"
            newUserName = thisLoginUser.email   
            newPw = thisLoginUser.newPw
            cmd = "imapsync --syncinternaldates --sep1 / --prefix1 / --nofoldersizes --skipsize" \
		+ " --useuid --usecache --subscribe_all" \
                + " --host1 " + oldHost +" --authmech1 LOGIN --user1 " + oldUserName + " --password1 " + oldPw \
                + " --host2 " + newHost + " --authmech2 LOGIN --user2 " + newUserName + " --password2 " + newPw 
            argu = shlex.split(cmd) 
        
            proc = subprocess.Popen(argu, stdout=subprocess.PIPE, cwd="/opt/MigrateEmailServer/")
        
            #while proc.poll() == None:
                # We can do other things here while we wait
                #time.sleep(1)
                #print "."
            
            stdoutdata = proc.communicate()[0]
            
            ##############################
            # find err.  
            loginAuthFailure = "Failure: error login on"
            if loginAuthFailure in stdoutdata:
                return render(request, 'getlogin/main.html', {
                                                              'form': form,
                                                              'statusMsg': "your login email or password wrong, please try again.",
                                                              })
                
            ##############################
            # find how many email records
            msgTxCnt = "Messages transferred"
            msgDryMode = "dry mode"
            buf = StringIO.StringIO(stdoutdata)
            for oneLine in buf.readlines():
                if msgTxCnt in oneLine:
                    txCntArr = oneLine.split( );
                    if msgDryMode in oneLine:
                        txCnt = txCntArr[6]
                    else:
                        txCnt = txCntArr[3]
                    return render(request, 'getlogin/progress.html', {
                                                                      'txCnt' : txCnt,
                                                                      })
                
            return render(request, 'getlogin/err.html', {'errMsg':"Cannot Find how many Messages transferred"})
            #return render(request, 'getlogin/test.html', {'testStr':p.returncode})
            #return redirect('getlogin.views.migrating', proc)
                
            ##############################
            # tell the imapsync dry result to user, let user know i will send you back a email when completed   
        
            #return redirect('getlogin.views.migrating', pk=thisLoginUser.pk)
	else: 
    	    return render(request, 'getlogin/err.html', {'errMsg':"Form Data Invalid"})

    ##############################
    # fresh load this page, show the form to let the user to input his/her login info. 
    else:
        form = LoginPairForm()
    	return render(request, 'getlogin/main.html', {
                                                      'form': form,
                                                      'statusMsg': "",
                                                      })

def list(request):
    lp = LoginPair.objects.filter(pw="null")
    return render(request, 'getlogin/list.html', {'unDidloginPairs':lp})
