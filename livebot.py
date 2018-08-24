#! /usr/bin/python3

import logging
import mysql
from telegram.ext import Updater
from telegram.ext import CommandHandler

updater = Updater(token='token')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text='If you want some help,please use /help')

def helpmsg(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text = 'send or reply /id to search one\'s LiveID\n/change to set your LiveID')

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
	bot.sendMessage(chat_id=update.message.chat_id, reply_to_message_id = update.message.message_id, text = str(whose) + str(liveid))

def changeid(bot, update, args):
	userid = update.message.from_user.id
	username = update.message.from_user.username
	msg = ''.join(args)
	if(len(msg) <= 0):
		bot.sendMessage(chat_id=update.message.chat_id, reply_to_message_id = update.message.message_id, text = 'Please tell me your new id')
		return
	if(mysql.searchindb(userid) != -1):
		mysql.changeondb(userid, msg, username)
		bot.sendMessage(chat_id=update.message.chat_id, reply_to_message_id = update.message.message_id, text = 'updated')
	else:
		mysql.inserttodb(userid, msg, username)
		bot.sendMessage(chat_id=update.message.chat_id, reply_to_message_id = update.message.message_id, text = 'changed')

start_handler = CommandHandler('start',start)
search_handler = CommandHandler('id',searchid, pass_args = True)
change_handler = CommandHandler('change',changeid, pass_args = True)
help_handler = CommandHandler('help',helpmsg)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(search_handler)
dispatcher.add_handler(change_handler)
dispatcher.add_handler(help_handler)

updater.start_polling()