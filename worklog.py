#!/usr/bin/python
from optparse import OptionParser
from datetime import datetime
import sys
import os


# Configuration
directory   = os.path.expanduser('~') + '/Worklog/' # Change this to the destination of your choice
file_format = '%Y/Week %U/%Y-%m-%d.log'

# WorkLog class
class WorkLog:
    """ Small script to start and stop logging work with optional commenting. """

    # Private variables - do not touch
    __filename          = None
    __full_date_format  = '%Y-%m-%d %H:%M:%S'
    __chars             = {
        'start_char'    : 'S',
        'continue_char' : '|',
        'finish_char'   : 'F'
    }
    __options           = None
    __largs             = None

    def __init__(self, directory, file_format):
        # Prepare configuration
        self.__filename = directory + datetime.strftime(datetime.now(), file_format)
        parser          = self.__create_parser()
        self.__options  = parser.parse_args()[0]
        self.__largs    = parser.largs
        
        # Determine (last) times
        self.__touch_file()

        (last_line, last_time, last_is_end) = self.__get_last_breakpoint()
        total_worktime = self.__get_total_worktime(last_time, last_is_end)

        # Dump log file and exit
        if self.__options.dump:
            for line in open(self.__filename):
                sys.stdout.write(line)
            print(total_worktime)
            return

        # Output current status and exit
        if self.__options.status:
            print(last_line.strip())
            print(total_worktime)
            return

        # Force commenting
        if len(self.__largs) == 0:
            # print('Usage: ' + parser.usage)
            print('You forgot to comment. :)')
            return

        # Determine command and comment
        command = self.__determine_command(last_line)
        comment = ' '.join(self.__largs).strip().replace('\t', ' ')

        # Output log record
        self.__write_line(command, comment, total_worktime)
        self.__log_status(command, comment, total_worktime)

    def __create_parser(self):
        # CLI options
        parser = OptionParser(usage='Usage: worklog [-d] [-s] [-f] <comment>',
                              description='Small Python logging tool to make work and time management real easy.')

        parser.add_option('-d', '--dump',
                          action="store_true", dest="dump", default=False,
                          help="Dump log file.")

        parser.add_option('-s', '--status',
                          action="store_true", dest="status", default=False,
                          help="Print working status and total time.")

        parser.add_option('-f', '--finish',
                          action="store_true", dest="stop", default=False,
                          help="Finish working.")

        return parser

    def __touch_file(self):
        # Create the directory - if necessary
        directory = os.path.dirname(self.__filename)

        if not os.path.exists(directory):
            os.makedirs(directory)

        # Create file - if necessary
        with open(self.__filename, 'a') as log_file:
            log_file.close()

    def __get_last_breakpoint(self):
        line        = ''
        last_time   = ''
        last_is_end = False

        for line in open(self.__filename):
            try:
                # Find last starting record
                if line[20:21] == self.__chars['start_char']:
                    last_time = line[0:19]
                    last_is_end = False
            except ValueError:
                pass
            try:
                # Find last finishing record
                if line[20:21] == self.__chars['finish_char']:
                    last_time = line[0:19]
                    last_is_end = True
            except ValueError:
                pass

        return (line, last_time, last_is_end)

    def __get_total_worktime(self, last_time, get_mtbw):
        total = 'Error calculating working time.'

        if len(last_time) > 0:
            try:
                # Calculate time between last start/finish and now
                total = str(datetime.now()-datetime.strptime(last_time, self.__full_date_format))
                total = total[0:total.index('.')]
                total = ('MTBW ' if get_mtbw else 'Total of ') + total + '.' # MTBW = Mean Time Between Work
            except ValueError:
                pass

        return total

    def __determine_command(self, last_line):
        if self.__options.stop:
            return self.__chars['finish_char']
        
        command = self.__chars['start_char']

        try:
            # Continue if already started
            (self.__chars['start_char'] + self.__chars['continue_char']).index(last_line[last_line.index('\t')+1])
            command = self.__chars['continue_char']
        except ValueError:
            pass

        return command

    def __write_line(self, command, comment, total):
        # Write to file
        with open(self.__filename, 'a') as log_file:
            log_file.write(datetime.now().strftime(self.__full_date_format) +
                           '\t' + command +
                           '\t' + comment)
            if command == self.__chars['finish_char']:
                log_file.write(' ' if comment[len(comment)-1:] in ['.', ',', ':', ';', '!', '?'] else '. ') # Append dot to comment if sentence is not closed
                log_file.write(total)
            log_file.write('\n')

    def __log_status(self, command, comment, total):
        # Write to console
        if command == self.__chars['start_char']:
            print('Started.')
        elif command == self.__chars['continue_char']:
            print('Continuing. ' + total)
        elif command == self.__chars['finish_char']:
            print('Stopped. ' + total)

if __name__ == '__main__':
    log = WorkLog(directory, file_format)