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
        
        ##############################
        # get all accounts one by one to sync
        testCnt = 0  
        for thisLoginUser in LoginPair.objects.all():
            
            ##############################
            # get this account info. 
            
            ##############################
            # imapsync and its parameters   
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
        
            ##############################
            # monitor tx error or success
            oneAccSyncErrFlag = True
            while (oneAccSyncErrFlag):
             
                ##############################
                # do a imapsync dry connection and chk how many msg to sync 
                proc = subprocess.Popen(argu, stdout=subprocess.PIPE, cwd="/opt/MigrateEmailServer/")
            
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
                # find sucessful tx or not 
                detectStr = "Detected"
                buf = StringIO.StringIO(stdoutdata)
                for oneLine in buf.readlines():
                    if detectStr in oneLine:
                        txCntArr = oneLine.split( );
                        if txCntArr[2] == "errors":
                            if txCntArr[1] == '0' :
                                oneAccSyncErrFlag = False
                                
            #testCnt += 1
            #if testCnt >=3:
            #    break
                            
        txCnt = "all done"
        return render(request, 'getlogin/progress.html', {
                                                          'txCnt' : txCnt,
                                                          })

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
