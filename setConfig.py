#!/usr/bin/python
import os
import ConfigParser
#This file will write our config to a file which we'll then read later on

config = ConfigParser.RawConfigParser()
#DB details for storing content
config.add_section('DB')
config.set('DB', 'dbhost', '')
config.set('DB', 'dbname', '')
config.set('DB', 'dbuser', '')
config.set('DB', 'dbpass', '')
#how to connect to the transmission daemon
config.add_section('transmission')
config.set('transmission', 'transmission_client', '')
config.set('transmission', 'transmission_port', 9091)
config.set('transmission', 'transmission_user', '')
config.set('transmission', 'transmission_pass', '')
#filesystem details
config.add_section('filesystem')
#Where the downloads are stored - this is the debian default - must end with a /
config.set('filesystem', 'downloaddir', '/var/lib/transmission-daemon/downloads/')
#Where the converted files are stored - must end with a /
config.set('filesystem', 'convertedfolder', '')
#our RSS details
config.add_section('rss')
config.set('rss', 'rssfeed', '')
#how to notify of a succesful download
config.add_section('notification')
config.set('notification', 'FROMADDR', '')
config.set('notification', 'TOADDRS', '')
config.set('notification', 'smtpserver', '')
config.set('notification', 'smtpport', 25)
#some misc stuff
config.add_section('misc')
#if testing is 0 then use a local file as the feed instead of the remote one
config.set('misc', 'testing', 0)
#if run is 0 then cleanup after the last problematic run - cleans up DB etc
config.set('misc', 'run', 1)
#sets our default for downloading
config.set('misc','download',0)
config.set('misc','logfile','/var/log/transmission-rss.log')
config.set('misc','high_def',0)

# Writing our configuration file to 'example.cfg'
with open('Transmission-RSS.cfg', 'wb') as configfile:
    config.write(configfile)
