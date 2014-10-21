# -*- encoding:utf-8 -*-

from KanbanRestClient import *
import time

class KanbanClient(KanbanRestClient):
	"""docstring for KanbanClient"""
	def __init__(self, appkey,appSecret,appUrl):
		self.client = KanbanRestClient(appkey,appSecret,appUrl);
	
	def AddAwardPoint(self,projectId,userId,awardUserId,remark,point):
		request = AddAwardPointRequest(projectId,userId,awardUserId,remark,point)
		resp = self.client.execute(request);
		return AddAwardPointResponse(request,resp);
	def CreateTask(self,projectId,userId,cardId,assignee,dueAt,title,awardPoint):
		request = CreateTaskRequest(projectId,userId,cardId,assignee,dueAt,title,awardPoint)
		resp = self.client.execute(request)
		return CreateTaskResponse(request,resp);
	def UpdateTask(self):
		request = CreateTaskRequest(projectId,userId,cardId,assignee,dueAt,title,awardPoint)
		resp = self.client.execute(request)
		return CreateTaskResponse(request,resp);
	def DeleteTask(self):
		pass

if __name__ == "__main__":
	client = KanbanClient('100001','osn4icnp1dgwg7z6w97b0w7b33qyvqxo','http://localhost:8080/api/call');
	resp = client.AddAwardPoint(1,1,1,'test',10)
	if(resp.success):
		print '调用成功!'
	else:
		print '调用失败，错误为：',resp.message
	client.CreateTask(1,1,4,1,long(time.time()*1000),'测试用的task',10)