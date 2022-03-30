#importing packages
import boto3
import json
import smtplib
import win32com.client
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# filtering instence data
ec2_client=boto3.client("ec2")
x=ec2_client.describe_instances()
data=x["Reservations"][0]
data_instance=data["Instances"]

#created a empty list to store filterd data
l=[]
#using for loop to filter data and append to list
for i in range (len(data_instance)):
    datas = {}
    val = data_instance[i]['Tags']
    datas["instance Name"] = val[0]['Value']
    datas["instance ID "]= data_instance[i]['InstanceId']
    datas["instance Status "]= data_instance[i]['State']['Name']
    date = data_instance[i]['LaunchTime']
    mainDate = str(date).split(" ")
    datas["Lanch Date "] = mainDate[0]
    datas["Public Ip Address"] = data_instance[0]['PublicIpAddress']
    #here appending data filterd data to list
    l.append(datas)
    
#storing data in dict format
k = {"ec2-details":l}
print(k)

# upload data into json file
j = json.dumps(k)
with open('data.json', 'w') as f:
    f.write(j)
    f.close()
  
# to send mail
outlook = win32com.client.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'sagar.g03@infosys.com'
mail.Subject = 'output of ec2 instances'
mail.HTMLBody = '<h3>please find attached file below</h3>'
mail.Body = "output"
mail.Attachments.Add('C:\\Users\sagar.g03\Desktop\Projects\data.json')
mail.CC = 'manohari.chintaluri@infosys.com'
mail.Send()