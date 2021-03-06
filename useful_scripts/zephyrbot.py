#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import sys
import zephyr
import random

if __name__ == '__main__':
    cur_file = os.path.abspath(__file__)
    django_dir = os.path.abspath(os.path.join(os.path.dirname(cur_file), '..'))
    sys.path.append(django_dir)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'zscore.settings'

import django.contrib.auth.models
from django.core.exceptions import ValidationError

import sleep.models
import sleep.utils

def setup():
    zephyr.init()
    subs = zephyr.Subscriptions()
    subs.add(('message', '*', '%me%'))
    subs.add(('zscore', '*', '*'))

def fetch_user_from_zgram(zgram):
    if not zgram.auth:
        print "  -> Rejecting: unauthenticated"
        raise LookupError("You aren't authenticated.")
    user, at, domain = zgram.sender.partition('@')
    if domain == 'ATHENA.MIT.EDU':
        email = "%s@mit.edu" % (user, )
        try:
            user = django.contrib.auth.models.User.objects.get(email=email)
            return user
        except django.contrib.auth.models.User.DoesNotExist:
            raise LookupError("No user with email %s" % (email, ))
    else:
        raise LookupError("Don't know about the domain %s" % (domain, ))

def build_reply(zgram):
    z = zephyr.ZNotice()
    z.cls = zgram.cls
    z.instance = zgram.instance
    z.recipient = zgram.sender
    z.opcode = 'auto'
    z.fields = ['zscore bot: http://zscore.mit.edu/', '']
    return z

def handle_zgram(zgram):
    if zgram.cls == 'zscore':
        pass
    else:
        reply = build_reply(zgram)
        try:
            user = fetch_user_from_zgram(zgram)
            if 'gnight' in zgram.message or 'goodnight' in zgram.message:
                success = sleep.models.PartialSleep.create_new_for_user(user)
                if success:
                    msg = 'Sleep well!'
                else:
                    msg = "Hmm, I can't seem to record you as asleep."
            elif 'awake' in zgram.message or "mornin'" in zgram.message:
                try:
                    s = sleep.models.PartialSleep.finish_for_user(user)
                    tmpl = "Good morning!\nYou slept from %s to %s.\n(That's %s.)"
                    msg = tmpl % (s.start_time, s.end_time, s.length())
                except sleep.models.PartialSleep.DoesNotExist:
                    msg = "Sorry, you don't seem to have been asleep."
                except ValidationError as e:
                    msg = e.messages[0]
            elif 'help' in zgram.message:
                msg = "Hi! I'm the zscore zephyrbot.\n\nMessage me 'gnight' when you want to sleep\nand 'awake' when you wake up in the morning.\n\nFor stats, message me 'stats'"
            elif 'meow' in zgram.message.lower():
                msg = random.choice(['meow!', "purrrr", "*barks*"])
            elif 'stats' in zgram.message:
                try:
                    sleeper = sleep.models.Sleeper.objects.get(pk = user.pk)
                    usermetrics = sleeper.sleeperprofile.metrics.all()
                    msglist = []
                    if 'global' in zgram.message or 'all-time' in zgram.message:
                        msglist.append("Your All-Time stats\n" + sleep.utils.zephyrDisplay(sleeper.movingStats(), usermetrics))
                    if 'decaying' in zgram.message or (len(msglist)==0):
                        msglist.append("Your Stats (exponential decay)\n" + sleep.utils.zephyrDisplay(sleeper.decayStats(), usermetrics))
                    msg = '\n\n'.join(msglist)
                except all as e:
                    print e
                    msg = 'Something went wrong! Zephyr -c zscore for help!'
            elif 'bug' in zgram.message or 'bug' in zgram.instance:
                msg = """Sorry! daemon/zscore does not accept bug requests\nor feature reports! Feel free to message us on -c zscore,\nemail us at zscore@mit.edu, or create a new issue at\nhttps://github.com/sleepers-anonymous/zscore/issues/new"""
            else:
                msg = "I'm sorry -- I don't understand. Message me 'help' for more information."
        except LookupError as e:
            msg = "I'm sorry -- I can't find an account for you: %s" % (e.message, )
        reply.fields[1] = msg
        reply.send()

def main():
    setup()
    print "Waiting..."
    while True:
        zgram = zephyr.receive(True)
        if not zgram or zgram.opcode == 'PING':
            continue
        if zgram.opcode.lower() == 'kill':
            sys.exit(0)

        print '%s: [%s] -c %s -i "%s": %s -> %s' % (
            datetime.datetime.now(),
            zgram.opcode,
            zgram.cls, zgram.instance,
            zgram.sender, zgram.recipient,
        )
        if zgram.opcode.lower() == 'auto':
            print "  -> auto; ignoring"
            continue
        
        handle_zgram(zgram)

if __name__ == '__main__':
    main()
