# -*- encoding:utf-8 -*-

import time
import urllib2
import json
import urllib

API_VERSION = '1.0.0-20130305'
class KanbanApiException(Exception):
    """Taobao API exception"""

    def __init__(self, message=None, code=None):
        self.message    = message
        self.code   = code

class KanbanRequest(object):
	def __init__(self,projectId,userId):
		self.projectId = projectId
		self.userId = userId
	def getApiName(self):
		pass
	def getTextParams(self):
		params = {}
		params['projectId'] = self.projectId
		params['userId'] = self.userId
		return params


class KanbanResponse(object):
    def __init__(self,requestParameters=None,resp=None):
    	if(resp!=None):
	        self.success = resp['success']
	        self.message = resp['message']
	        self.requestParameters = requestParameters

    def getMessage(self):
        return self.message

    def setMessage(self, message):
        self.message = message

    def isSucsess(self):
        return success

    def getRequestParameters(self):
        return self.requestParameters

    def setRequestParameters(self, requestParameters):
        self.requestParameters = requestParameters

    def setKanbanObject(self, object):
        self.kanbanObject = object
        
    def getKanbanObject(self):
        return self.kanbanObject
    

class AddAwardPointRequest(KanbanRequest):
    """KANBAN API: kanban.awardpoint.add"""

    # 需要奖励的用户id    
    awardUserId = int()
    remark = str()
    point = int()
    
    def __init__(self, projectId,userId,awardUserId,remark,point):
    	super(AddAwardPointRequest,self).__init__(projectId,userId)
        self.awardUserId = awardUserId;
        self.remark = remark;
        self.point = point;

    def setAwardUserId(self,awardUserId):
        self.awardUserId = awardUserId;

    def setRemark(self,remark):
        self.remark = remark;

    def setPoint(self,point):
        self.point = point;

    def getApiName(self):
        return "kanban.awardpoint.add"

    def getTextParams(self):
        params = super(AddAwardPointRequest,self).getTextParams()
        # setup text params
        params['awardUserId']  = self.awardUserId;
        params['remark'] = self.remark;
        params['point'] = self.point;
        return params

class AddAwardPointResponse(KanbanResponse):
	"""docstring for AddAwardPointResponse"""
	def __init__(self, requestParameters,resp):
		super(AddAwardPointResponse,self).__init__(requestParameters,resp)

class CreateTaskRequest(KanbanRequest):
	def __init__(self,projectId,userId,cardId,assignee,dueAt,title,awardPoint):
		super(CreateTaskRequest,self).__init__(projectId,userId)
		self.cardId = cardId
		self.assignee = assignee
		self.dueAt = dueAt
		self.title = title
		self.awardPoint = awardPoint
	def getApiName(self):
		return "kanban.task.create"

	def getTextParams(self):
		params = super(CreateTaskRequest,self).getTextParams()
		params['cardId'] = self.cardId;
		params['assignee'] = self.assignee
		params['dueAt'] = self.dueAt
		params['title'] = self.title
		params['awardPoint'] = self.awardPoint
		return params

class CreateTaskResponse(KanbanResponse):
	def __init__(self, requestParameters,resp):
		self.taskId = resp.get('taskId')
		super(CreateTaskResponse,self).__init__(requestParameters,resp)
	def getTaskId():
		return self.taskId

class KanbanRestClient():
	"""docstring for kanbanRestClient"""
	def __init__(self, appkey,appSecret,appUrl):
		self.appkey = appkey;
		self.appSecret = appSecret;
		self.apiUrl = appUrl;
	def execute(self,request):
		#get application level params
		textParams = request.getTextParams().copy();
		textParams['method'] = request.getApiName();
		textParams['version'] = API_VERSION;
		textParams['timestamp']   = time.strftime('%Y-%m-%d %X', time.localtime()) 
		textParams['appkey'] = self.appkey;
		textParams['secret'] = self.appSecret;

		# try to GET/POST rest request
		try:
			resp = self.doGet(self.apiUrl,textParams);
			return json.loads(resp);
		except Exception,e:
			return json.loads('{"success":false,"message":"network error!"}')

	def doGet(self,serverUrl, textParams):
	    """get message from server"""
	    form_data = urllib.urlencode(textParams)
	    # print form_data

	    # get data
	    rsp = urllib2.urlopen(serverUrl, form_data)
	    return rsp.read().decode('UTF-8');
