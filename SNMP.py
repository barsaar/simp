import sqlite3 as sql
from pysnmp.hlapi import *
import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def create_table001():
    try:
        if os.path.exists("Monitor_DB.db")==False:
            con = sql.connect("Monitor_DB.db")

            sql_command = """
                CREATE TABLE Monitor_Table (
                UID INTEGER  PRIMARY KEY,
                IPorDNS NVARCHAR(50),
                PORT INTEGER(5),
                PING NVARCHAR(1),
                SNMP NVARCHAR(1));"""
            con.execute(sql_command)

            #sql_command1 = f"INSERT INTO UsersDB (EMAIL, FN, LN, PASSWD, ISREGISTER)\
                  #  VALUES ('a@a.com', 'AB', 'CD', 'ABCD', 0);"
            #cursor.execute(sql_command1)

            con.commit()
            con.close()
            write_to_log002("Database Has Been Created!")
        else:
            write_to_log002("Database Already Exist!")
    except Exception as e:
        write_to_log002(f"Fail Error: 001 -- {e}")
        send_email003()
def write_to_log002(log):
    try:
        with open("log.log", "a") as f:
            a = datetime.datetime.now()
            f.write(f"{a} - {log}\n")
    except Exception as e:
        with open("log.log", "a") as f:
            a = datetime.datetime.now()
            f.write(f"{a} - Fail Error: 002 -- {e}")
            send_email003()
def send_email003(sub="Something went wrong", bod="Something went wrong"):
    try:
        fromaddr = SenderEmailAddress@mail.com
        toaddr = YourEmailAddress@mail.com

        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = sub

        body = bod

        msg.attach(MIMEText(body, 'plain'))

        filename = "log.log"
        attachment = open("log.log", "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, YourPassword)
        text = msg.as_string()
        write_to_log002("Sending email...")
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
    except Exception as e:
        print(e)
        write_to_log002("Fail Error: 003")
def SNMP004(host,port):
    try:
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in bulkCmd(SnmpEngine(),
                CommunityData('public'),
                UdpTransportTarget((host, port)),
                ContextData(),
                0, 25,  # fetch up to 25 OIDs one-shot
                    ObjectType(ObjectIdentity('1.3.6.1.2.1.1'))):
            if errorIndication or errorStatus:
                print(errorIndication or errorStatus)
                break
            else:
                for varBind in varBinds:
                    #with open("Meraki.txt", "a") as f:
                    #    f.write(' = '.join([x.prettyPrint() for x in varBind])+"\n")
                    print(' = '.join([x.prettyPrint() for x in varBind]))
    except Exception as e:
        write_to_log002(f"Fail Error: 004 -- {e}")
        send_email003()
def Ping005(host):
    try:
        hostname = host  # example
        response = os.system("ping -n 1 " + hostname)

        # and then check the response...
        if response == 0:
            write_to_log002(f"Hostname {hostname} is up!")
            return 0
        else:
            write_to_log002(f"Hostname {hostname} is down!")
            sub = f"{hostname} is Down"
            bod = f"{hostname} is Down"
            send_email003(sub, bod)
    except Exception as e:
        write_to_log002(f"Fail Error: 005 -- {e}")
        send_email003()
def Monitor006():
    try:
        con = sql.connect("Monitor_DB.db")
        cursor = con.cursor()
        cursor.execute("SELECT IPorDNS, PORT, PING, SNMP FROM Monitor_Table")
        a = cursor.fetchall()

        con.commit()
        con.close()

        for i in a:
            if i[2] == "1":
                Ping005(i[0])

            if i[3] == "1":
                SNMP004(i[0], i[1])
    except Exception as e:
        write_to_log002(f"Fail Error: 006 -- {e}")
        send_email003()
create_table001()
