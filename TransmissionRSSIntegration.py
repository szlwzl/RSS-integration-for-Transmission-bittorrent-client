#!/usr/bin/python
#define imports
import feedparser
import MySQLdb
import transmissionrpc
import logging
import sys
import shutil
import os
import subprocess
import smtplib

#set variables
dbhost=""
dbname=""
dbuser=""
dbpass=""
db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass,db=dbname)

#set transmission stuphs
transmission_client=""
transmission_port=9092
transmission_user=""
transmission_pass=""

download=0

#Where files are downloaded to initially
downloaddir="/var/lib/transmission-daemon/downloads/"#This is the current default for debian - must finish with a /
#Where the converted files shoud go to
convertedfolder=""#must finish with a /
#if testing is 1 then use a local rss file(saves hitting the provider)
testing=0
#Run =0 will clear up any old downloads - used for testing purposes only
run=1
rssfeed=""
FROMADDR = "VALID FROM ADDRESS"
TOADDRS  = ["VALID TO ADDRESS"]
smtpserver = "VALID MAIL SERVER"
smtpport = 25

#set logging
try:
	if sys.argv[1]=="debug":
		debug=1
	else:
		debug=0
except Exception:
	debug=0	

if debug==1:
	LOG_FILENAME = '/var/log/example.log'
	logging.getLogger('transmissionrpc').setLevel(logging.DEBUG)
	logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)


#setup transmission session

if run==0:
	tc = transmissionrpc.Client(transmission_client,port=transmission_port,user=transmission_user,password=transmission_pass)
	print tc.info()
	tc.remove(68)
        cursor2 = db.cursor()
        cursor2.execute("DELETE FROM log")
        cursor2.execute("UPDATE shows_table SET show_last_download_series=0,show_last_download_episode=0")	

def checkNew():
	download=0
	if testing==1:
        	d = feedparser.parse(r"/home/simon/eztv.rss")
	else:
	        d = feedparser.parse(rssfeed)

        #check each show
        for item in d['items']:
                description=item['description']
                #description looks like this: 
                #Show Name: The Office; Episode Title: N/A; Season: 7; Episode: 5       
                #get the show name
                show_name=description.split(";")
                show_name=show_name[0]
                show_name=show_name.split(": ")
                show_name=show_name[1]
                #get the series & episode
                #print description
                try:
                        series_no=description.split("Season: ",1)
                        series_no=series_no[1]
                        series_no=series_no.split("; ")
                        episode_no=series_no[1]
                        episode_no=episode_no.split(": ")
                        episode_no=int(episode_no[1])
                        series_no=int(series_no[0])
                except:
                        series_no=-1
                # connect
                # create a cursor
                cursor = db.cursor()
		cursor.execute("SELECT show_name,show_start_series,show_start_episode,show_finished_folder,show_last_download_series,show_last_download_episode,show_id FROM shows_table WHERE show_name='"+show_name+"'")
             # get the resultset as a tuple
                result = cursor.fetchall()
                # iterate through resultset
                for record in result:
#                       print record[0] , "-->", record[1], record[2]
                        if series_no > record[4]:
                        	download=1
                        if series_no == -1 or (series_no == record[4] and episode_no > record[5]):
                              	download=1
                        cursor2 = db.cursor()
                        number_of_results=cursor2.execute("SELECT log_status FROM log WHERE show_id="+str(record[6])+" AND show_torrent='"+item['link']+"' AND log_status=1")
                        result2 = cursor2.fetchall()
                        if number_of_results > 0:
                                download=0
		 	#is the torrent already added(check the api!)
                        if download==1:
				tc = transmissionrpc.Client(transmission_client,port=transmission_port,user=transmission_user,password=transmission_pass)
                                #update the db to show we're dling it
                                print "WOOHOO - we're going to download something"+show_name
                                download=0
#                                #very simple - just add this to tc(defined above) :)
				#this returns a dictionary that looks like this: {31: <Torrent 31 "Greys.Anatomy.S07E05.HDTV.XviD-LOL.avi">}
                                torrent_info=tc.add_uri(item['link'])
				torrent_id=torrent_info.keys()[0]				
				addedtorrent = tc.info(torrent_id)[torrent_id]
       	                        cursor2.execute("INSERT INTO log(show_id,show_torrent,log_status,show_hash) VALUES("+str(record[6])+",'"+item['link']+"',1,'"+addedtorrent.hashString+"')")
	        	        cursor2.execute("UPDATE shows_table SET show_last_download_series="+str(series_no)+",show_last_download_episode="+str(episode_no)+" WHERE show_id="+str(record[6]))
				#have to remove the torrent
#				if testing==1:
#					tc.remove(addedtorrent.hashString)
def checkOld():
	tc = transmissionrpc.Client(transmission_client,port=transmission_port,user=transmission_user,password=transmission_pass)
	#get all the torrents
  	torrents = tc.info()
        for tid, torrent in torrents.iteritems():		
                print('%s: %s %s %.2f%% %s' % (torrent.hashString, torrent.name, torrent.status, torrent.progress, torrent.eta))
                status=torrent.progress
		if status==100.0:
		        cursor = db.cursor()
        		cursor.execute("SELECT show_finished_folder FROM  shows_table A, log B WHERE A.show_id = B.show_id AND B.show_hash ='"+torrent.hashString+"'")
			result = cursor.fetchall()
	                for record in result:
				finishingfolder=record[0]
			tc.remove(torrent.hashString)
			completefile=downloaddir+torrent.name
			targetlocation=finishingfolder+torrent.name
			shutil.move(completefile,targetlocation)
			actualfilename=torrent.name[:-3]+"mp4"
	       	        cursor.execute("UPDATE log SET log_status=2 WHERE show_hash='"+torrent.hashString+"'")
			pid = subprocess.Popen(['/usr/local/bin/ffmpeg', '-i', targetlocation, '-s', '480x320', '-b', '384k', '-vcodec', 'libx264', '-flags', '+loop+mv4', '-cmp', '256', '-partitions', '+parti4x4+parti8x8+partp4x4+partp8x8+partb8x8', '-subq', '7', '-trellis', '1', '-refs', '5', '-bf', '0', '-flags2', '+mixed_refs', '-coder', '0', '-me_range', '16', '-g', '250', '-keyint_min', '25', '-sc_threshold', '40', '-i_qfactor', '0.71', '-qmin', '10', '-qmax', '51', '-qdiff', '4', '-acodec', 'libfaac', convertedfolder+actualfilename]).pid
			SUBJECT  = "File Downloaded "+torrent.name
			msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (FROMADDR, ", ".join(TOADDRS), SUBJECT) )
			msg += torrent.name+" completed download and is now on being converted\r\n"
			server = smtplib.SMTP(smtpserver, smtpport)
			if debug==1:	
				server.set_debuglevel(1)
			server.ehlo()
			server.sendmail(FROMADDR, TOADDRS, msg)
			server.quit()

if run==1:
	checkNew()				
	checkOld()
  


