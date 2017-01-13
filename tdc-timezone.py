#!/usr/bin/python
######################################################
# Copyright (C) 2017 by Teradata Corporation.
#
# All Rights Reserved.
#
# TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET
#######################################################
import sys
import subprocess
import logging

logger = logging.getLogger(__name__)
LOG_FILENAME = '/tmp/tdc-timezone.log'
LOG_FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILENAME, level=logging.INFO)

prefix = '/usr/share/zoneinfo/'


def execute_command(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = ''
    while True:
        line = p.stdout.readline()
        if len(line) == 0:
            break
        else:
            result += line

    return result


def validate_timezone(timezone):
    timezone_string = prefix + timezone
    cmd = "file " + timezone_string + " 2> /dev/null"
    result = execute_command(cmd)
    if 'timezone data' not in result:
        return False
    else:
        return True


def input_timezone():
    new_timezone = raw_input("Enter New Timezone: ")

    def confirm_continue(message):
        stop = False
        while True:
            answer = raw_input(message + ' [yes/no] ')
            if answer.upper() == 'YES' or answer.upper() == 'Y':
                break

            elif answer.upper() == 'NO' or answer.upper() == 'N':
                stop = True
                break
            else:
                print "Please answer yes or no."

        if stop:
            return False
        else:
            return True

    if not validate_timezone(new_timezone):
        if confirm_continue("Invalid timezone. Try again? "):
            return input_timezone()
        else:
            return None

    return new_timezone


def change_timezone(new_timezone):
    if new_timezone is not None:
        cmd = 'sed -i "s@TIMEZONE=\\"\(.*\)\\"@TIMEZONE=\\"' + new_timezone + '\\"@" /etc/sysconfig/clock'
        res = execute_command(cmd)
        logger.debug(res)

        cmd = '/usr/sbin/zic -l ' + new_timezone
        res = execute_command(cmd)
        logger.debug(res)

        cmd = '/opt/teradata/gsctools/bin/cronhwclock.sh'
        res = execute_command(cmd)
        logger.debug(res)

        cmd = '/opt/teradata/gsctools/bin/checktz -f'
        res = execute_command(cmd)
        logger.debug(res)
        logger.info("Timezone changed to " + new_timezone )
        print "Timezone successfully changed to " + new_timezone


def main():
    args = sys.argv
    if len(args) == 2:
        logger.info("Setting timezone in non-interactive mode.")
        new_timezone = args[1]
        if not validate_timezone(new_timezone):
            logger.error("Invalid timezone:" + new_timezone)
            print "Invalid timezone."
            return
    else:
        new_timezone = input_timezone()

    change_timezone(new_timezone)

if __name__ == "__main__":
    main()

