#! /usr/bin/python3
import _thread
import threading
import time
import logging
import mysql
from Roll import Roll
from telegram.ext import Updater
from telegram.ext import CommandHandler

admins = []
rolllist = []
rollid = 100
updater = Updater(token='Token')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def replyMsg(bot, update, msg):
    bot.sendMessage(chat_id=update.message.chat_id, reply_to_message_id = update.message.message_id, text = msg)

def sendMsg(bot, update, msg):
    bot.sendMessage(chat_id=update.message.chat_id, text = msg)

def delmsg(bot, update):
    time.sleep(10)
    try:
        bot.delete_message(update.message.chat_id, update.message.message_id + 1)
    except:
        pass

def setAdmins(bot, update):
    if(update.message.from_user.id == 472877242):  #Bot Admin's userid
        adm = update.message.chat.get_administrators()
        for a in adm:
            admins.append(a.user.id)
        sendMsg(bot, update, 'done')
    else:
        sendMsg(bot, update, "You don't hava permission")


def isAdmin(bot, update):
    if(update.message.from_user.id in admins):
        return 1
    else:
        sendMsg(bot, update, "You don't hava permission")
        return 0

def start(bot, update):
    sendMsg(bot, update, 'If you want some help,please use /help')

def helpmsg(bot, update):
    sendMsg(bot, update, 'send or reply /id to search one\'s LiveID\n/change to set your LiveID')

def searchid(bot, update, args):
        try:
                msg = ''.join(args)
                if(len(msg) > 0):
                        msg = msg[1:]
                        liveid = mysql.searchname(msg)
                else:
                        user = update.message.reply_to_message.from_user
                        liveid = mysql.searchindb(user.id)
                whose = 'ID: '
        except:
                user = update.message.from_user
                liveid = mysql.searchindb(user.id)
                whose = 'Your ID: '
        if(liveid == -1):
                liveid = 'Not define'
        msgid = update.message.message_id
        replyMsg(bot, update, str(whose) + str(liveid))
#        delmsg(bot, update)
        _thread.start_new_thread(delmsg,(bot,update) )

def changeid(bot, update, args):
        userid = update.message.from_user.id
        msgid = update.message.message_id
        username = update.message.from_user.username
        msg = ' '.join(args)
        if(len(msg) <= 0):
                replyMsg(bot, update, 'Please tell me your new id')
                return
        if(mysql.searchindb(userid) != -1):
                mysql.changeondb(userid, msg, username)
                replyMsg(bot, update, 'updated')
        else:
                mysql.inserttodb(userid, msg, username)
                replyMsg(bot, update, 'changed')
#        delmsg(bot, update)
        _thread.start_new_thread(delmsg,(bot,update) )

def createRoll(bot, update, args):
    global rolllist
    global rollid
    if(isAdmin(bot, update)):
        if(len(args) < 2):
            sendMsg(bot, update, 'Input error')
        else:
            try:
                rolllist.append(Roll(rollid, args[0], float(args[1])))
                sendMsg(bot, update, 'All done, /rolllist to see roll list')
                rollid = rollid + 1
                rolllist[-1].start()
            except:
                sendMsg(bot, update, 'Failed with unknown error!')
            


def rollList(bot, update):
    global rolllist
    global rollid
    Rlist = 'Rollid\t\t\tTitle\t\t\tWinner'
    for rollobj in rolllist:
        Rlist += '\n' + str(rollobj.rollid) + '\t' + rollobj.title + '\t' + rollobj.closetime + '\t' + rollobj.winner
    sendMsg(bot, update ,Rlist)

def joinRoll(bot, update, args):
    for a in rolllist:
        if(str(a.rollid) == args[0]):
            if(update.message.from_user.username != ''):
                a.user.append(update.message.from_user.username)
                sendMsg(bot, update, "You've joined")
                return 0
            else:
                sendMsg(bot, update, "Seems you don't hava a username")
                return -1
    sendMsg(bot, update, 'Error code')

start_handler = CommandHandler('start',start)
createRoll_handler = CommandHandler('createRoll',createRoll, pass_args = True)
rollList_handler = CommandHandler('RollList',rollList)
joinRoll_handler = CommandHandler('join',joinRoll, pass_args = True)
search_handler = CommandHandler('id',searchid, pass_args = True)
change_handler = CommandHandler('change',changeid, pass_args = True)
help_handler = CommandHandler('help',helpmsg)
setAdmins_handler = CommandHandler('setadmins', setAdmins)

dispatcher.add_handler(joinRoll_handler)
dispatcher.add_handler(setAdmins_handler)
dispatcher.add_handler(rollList_handler)
dispatcher.add_handler(createRoll_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(search_handler)
dispatcher.add_handler(change_handler)
dispatcher.add_handler(help_handler)

updater.start_polling()

