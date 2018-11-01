import os;
class node:
    def __init__(self,value=-1,parent=None,score=(0,0)):
        self.score= score
        #self.maxScore=maxScore
        self.value=value
        self.parent=parent
        self.children=[]
        self.isSplaNode=True
        self.sdays=[]
        self.ldays=[]
        self.l=[]
        self.s=[]
        self.maxID=99999
        self.maxScore=(0,0)

def splaEligible(applicant):
    if applicant[11]=="Y" and applicant[12]=="Y" and applicant[10]=="N":
        return True
    else:
        return False
def lahsaEligible(applicant):
    if int(applicant[6:9])>17 and applicant[9]=="N" and applicant[5]=="F":
        return True
    else:
        return False
        
        
def getScore(root,currNode):
    count=0
    s=root.score
    if root.value==-1:
        s=(0,0)
    dayreq=allApplicants.get(currNode.value)[8:]
    for i in range(len(dayreq)):
        if dayreq[i] == '1':
            count += 1
    if currNode.isSplaNode:
        currNode.score= (s[0]+count,s[1])
    else:
        currNode.score =(s[0],s[1]+count)
        

def getSDays(parent,child):
    childDays=[]
    if child.isSplaNode:
        childDayRequirements=allApplicants.get(child.value)[8:]
        for i in range(len(childDayRequirements)):
            childDays.append(parent.sdays[i]-(int)(childDayRequirements[i]))
        return childDays
    elif not child.isSplaNode:
        return parent.sdays


def getLDays(parent,child):
    childDays=[]
    if not child.isSplaNode:
        childDayReq=allApplicants.get(child.value)[8:]
        for i in range(len(childDayReq)):
            childDays.append(parent.ldays[i]-(int)(childDayReq[i]))
        return childDays
    elif child.isSplaNode:
        return parent.ldays
        

def getl(parent,newNode):

    if parent.l and newNode.value in parent.l:
        a=list(parent.l)
        a.remove(newNode.value)
        return a
    else:
        return parent.l
        

def getS(parent,newNode):
    if parent.s and newNode.value in parent.s:
        a=list(parent.s)
        a.remove(newNode.value)
        return a
    else:
        return parent.s
        

def getPossibleChildren(child):#doesn't need parent.
    flag=0
    children=[]
    #childl=[]
    if child.isSplaNode:
        if not child.l:
            return child.l
        i=len(child.l)-1
        while(i>=0):
            dayreq=allApplicants.get(child.l[i])[8:]
            for j in range(len(dayreq)):
                if child.ldays[j]-(int)(dayreq[j]) < 0:
                    #flag=-1
                    child.l.remove(child.l[i])
                    break
                if j==6:
                    #and flag != -1:
                    children.append(child.l[i])
            i -= 1
        list.sort(children,key=int)
        return children
    else:
        if not child.s:
            return child.s
        i=len(child.s)-1
        while(i>=0):
            dayreq=allApplicants.get(child.s[i])[8:]
            for j in range(len(dayreq)):
                if child.sdays[j]-(int)(dayreq[j]) < 0:
                    #flag=-1
                    child.s.remove(child.s[i])
                    break
                if j==6:
                    #and flag != -1:
                    children.append(child.s[i])
            i -= 1
        list.sort(children, key=int)
        return children
        
        
def getDayCount(days):
    count=0
    for i in range(len(days)):
        if days[i]=='1':
            count+=1
    return count

def getChildrenScore(parent):
    count=0
    remApplicants=[]
    if parent.isSplaNode:
        remApplicants=parent.s
        for i in range(len(remApplicants)):
            dayreq = allApplicants.get(remApplicants[i])[8:]
            for i in range(len(dayreq)):
                if parent.sdays[i] - (int)(dayreq[i]) < 0:
                    count = 0
                    break
                else:
                    if dayreq[i] == '1':
                        count += 1
                        parent.sdays[i] -= 1
    else:
        remApplicants=parent.l
        for i in range(len(remApplicants)):
            dayreq = allApplicants.get(remApplicants[i])[8:]
            for i in range(len(dayreq)):
                if parent.ldays[i] - (int)(dayreq[i]) < 0:
                    count = 0
                    break
                else:
                    if dayreq[i] == '1':
                        count += 1
                        parent.ldays[i] -= 1
    return count

def getBestScore(newNode, root):
    if root.isSplaNode or root.value==-1:
        if(newNode.maxScore[0]>root.maxScore[0]) or root.maxID==99999:
            root.maxID=newNode.value
            root.maxScore=newNode.maxScore
    else:
        if(newNode.maxScore[1]>root.maxScore[1]) or root.maxID==99999:
            root.maxID=newNode.value
            root.maxScore=newNode.maxScore

def constructTree(root):
    if not root.children:
        if root.isSplaNode and  root.s:
            count=getChildrenScore(root)
            root.score=(root.score[0]+count,root.score[1])
            #root.maxScore=root.score
        elif not root.isSplaNode and root.l:
            count=getChildrenScore(root)
            root.score =(root.score[0],root.score[1]+count)
        root.maxScore = root.score
        return root.score
    for i in range(len(root.children)):
        newNode=node(value=root.children[i],parent=root)
        newNode.isSplaNode= not root.isSplaNode
        getScore(root,newNode)
        newNode.sdays = getSDays(root, newNode)
        newNode.ldays = getLDays(root, newNode)
        newNode.l = getl(root, newNode)
        newNode.s = getS(root, newNode)
        newNode.children = getPossibleChildren(newNode)
        score=constructTree(newNode)
        getBestScore(newNode,root)

path = os.getcwd();
inputFileName = path + "/input.txt"
with open(inputFileName, 'r') as ifp:
    nbeds = int(ifp.readline().strip())
    nspots = int(ifp.readline().strip())
    nL = int(ifp.readline().strip())
    lApplicants = set()
    for i in range(nL):
        lApplicants.add(ifp.readline().strip())
    nS = int(ifp.readline().strip())
    sApplicants = set()
    for i in range(nS):
        sApplicants.add(ifp.readline().strip())
    nApplicantPool = int(ifp.readline().strip())
    maxScore = -1
    maxScoreNode = node()
    #allApplicants is a dictionary
    allApplicants = {}
    #splaApplicants is a list
    splaApplicants = []
    #lahsaApplicants is a set
    lahsaApplicants = set()

    for i in range(nApplicantPool):
        applicant = ifp.readline().strip()
        applicantID= applicant[:5]
        allApplicants[applicantID] = applicant[5:]
        if applicantID not in lApplicants and applicantID not in sApplicants:
            if splaEligible(applicant) and lahsaEligible(applicant):
                splaApplicants.append(applicant[:5])
                lahsaApplicants.add(applicant[:5])
            elif splaEligible(applicant):
                splaApplicants.append(applicant[:5])
            elif lahsaEligible(applicant):
                lahsaApplicants.add(applicant[:5])
    root = node()
    list.sort(splaApplicants, key=int)
    root.children = splaApplicants
    root.isSplaNode = False
    root.sdays = [nspots  for i in range(7)]
    root.ldays = [nbeds for i in range(7)]
    spApplicants = list(sApplicants)
    laApplicants = list(lApplicants)
    for i in range(len(sApplicants)):
        sdayreq=allApplicants.get(spApplicants[i])[8:]
        for j in range(len(sdayreq)):
            root.sdays[j] -= (int)(sdayreq[j])
    for i in range(len(laApplicants)):
        ldayreq=allApplicants.get(laApplicants[i])[8:]
        for j in range(len(ldayreq)):
            root.ldays[j] -= (int)(ldayreq[j])
    root.l = list(lahsaApplicants)
    root.s = splaApplicants
    constructTree(root)
    ifp.close()
    outputFilePath = os.getcwd() + "/output.txt"
    ofp = open(outputFilePath, "w")
    ofp.write(str(root.maxID))
