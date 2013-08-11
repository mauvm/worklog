#!/usr/bin/env python
""" Small Python logging tool to make work and time management real easy. """

import os
from sys import stdout
from optparse import OptionParser
from datetime import datetime




# Change this to the destination of your choice
# Be careful though, every slash will create a new directory.
directory   = os.path.expanduser('~') + '/Worklog/'
file_format = '%Y/Week %U/%Y-%m-%d.log'

# Logging magic
class WorkLog:
    # Private variables - do not touch
    __filename          = None
    __options           = None
    __largs             = None
    __parser            = None
    __full_date_format  = '%Y-%m-%d %H:%M:%S'
    __chars             = {
        'start_char'    : 'S',
        'continue_char' : '|',
        'finish_char'   : 'F'
    }
    __last_breakpoint    = None
        
    def get_log_filename(self):
        if not self.__filename:
            raise ValueError('Log file not set.')
        
        return self.__filename

    def set_log_filename(self, filename):
        self.__filename = filename

    def log_file_exists(self):
        try:
            with open(self.get_log_filename()):
                pass
            return True
        except IOError:
            return False

    def log_file_empty(self):
        return not self.log_file_exists() or os.path.getsize(self.get_log_filename()) == 0

    def get_options(self):
        return self.__options

    def get_largs(self):
        return self.__largs

    def get_arg_parser(self):
        if not self.__parser:
            # CLI options
            parser = OptionParser(usage='Usage: worklog [-d] [-s] [-f] <comment>',
                                  description='Small Python logging tool to make work and time management real easy.')
            parser.add_option('-d', '--dump',
                              action="store_true", dest="dump", default=False,
                              help="Dump log file.")
            parser.add_option('-s', '--status',
                              action="store_true", dest="status", default=False,
                              help="Print working status and total time.")
            parser.add_option('-r', '--remove-record',
                              action="store_true", dest="remove_record", default=False,
                              help="Remove last record from the log.")
            parser.add_option('-f', '--finish',
                              action="store_true", dest="stop", default=False,
                              help="Finish working.")
            self.__parser = parser

        return self.__parser

    def get_full_date_format(self):
        return self.__full_date_format

    def get_char(self, key):
        return self.__chars[key]

    def get_last_breakpoint(self):
        if not self.__last_breakpoint:
            line            = ''
            last_start_stop = ''
            last_is_end     = False
            start_char      = self.get_char('start_char')
            finish_char     = self.get_char('finish_char')

            self.touch_log_file()

            for line in open(self.get_log_filename()):
                try:
                    char = line[20:21]

                    # Find last starting record
                    if char == start_char:
                        last_start_stop = line[0:19]
                        last_is_end = False
                    # Find last finishing record
                    elif char == finish_char:
                        last_start_stop = line[0:19]
                        last_is_end = True
                except ValueError:
                    pass

            self.__last_breakpoint = (line.strip(), last_start_stop, last_is_end)

        return self.__last_breakpoint

    def get_last_record(self):
        return self.get_last_breakpoint()[0]

    def get_last_time_str(self):
        return self.get_last_breakpoint()[1]

    def get_last_is_end(self):
        return self.get_last_breakpoint()[2]

    def get_worktime_str(self):
        last_time_str = self.get_last_time_str()

        try:
            # Calculate time between last start/finish and now
            total = str(datetime.now()-datetime.strptime(last_time_str, self.get_full_date_format()))
            total = total[0:total.index('.')] # Remove floating point
            if self.get_last_is_end():
                return 'Avoiding work since ' + total + '.'
            else:
                return 'Total of ' + total + '.'
        except ValueError:
            return 'Error calculating total working time.'

    def get_command(self):
        if self.get_options().stop:
            return self.get_char('finish_char')

        start_char = self.get_char('start_char')

        try:
            last_line = self.get_last_record()
        except IOError:
            return start_char

        if len(last_line) < 23:
            return start_char

        last_command = last_line[20:21]

        if last_command == self.get_char('finish_char'):
            return start_char
        
        return self.get_char('continue_char')

    def parse_args(self):
        parser          = self.get_arg_parser()
        self.__options  = parser.parse_args()[0]
        self.__largs    = parser.largs

    def process_request(self):
        log.parse_args()

        self.handle_dump() \
        or self.handle_status() \
        or self.handle_remove_record() \
        or self.handle_comment()

    def handle_dump(self):
        if not self.get_options().dump:
            return False
        if self.log_file_empty():
            print('No work logged today.')
            return True

        for line in open(self.get_log_filename()):
            stdout.write(line)
        print(self.get_worktime_str())
        return True
        
    def handle_status(self):
        if not self.get_options().status:
            return False
        if self.log_file_empty():
            print('No work logged today.')
            return True

        print(self.get_last_record())
        print(self.get_worktime_str())
        return True

    def handle_remove_record(self):
        if not self.get_options().remove_record:
            return False
        if self.log_file_empty():
            print('No work logged today.')
            return True

        filename = self.get_log_filename()

        with open(filename, 'r') as log_file:
            lines = log_file.readlines()
            log_file.close()
        if len(lines) == 1:
            try:
                os.remove(self.get_log_filename()) # Remove log file
            except IOError:
                pass
            print('Removed the log (since it was empty).')
        else:
            with open(filename, 'w+') as log_file:
                log_file.writelines(lines[:-1])
                log_file.close()
            print('Removed last record from the log.')
        
        return True
    
    def handle_comment(self):
        if len(self.get_largs()) == 0:
            print('You forgot to comment. :)')
            return True

        # Determine command and comment
        command         = self.get_command()
        comment         = ' '.join(self.get_largs()).strip().replace('\t', ' ')
        worktime_str    = self.get_worktime_str()

        # Output log record
        self.write_line(command, comment, worktime_str)
        self.log_status(command, comment, worktime_str)

        return True

    def touch_log_file(self):
        # Create the directory - if necessary
        directory = os.path.dirname(self.get_log_filename())

        if not os.path.exists(directory):
            os.makedirs(directory)

        # Touch log file
        with open(self.get_log_filename(), 'a') as log_file:
            log_file.close()

    def write_line(self, command, comment, worktime_str):
        # Write record to file
        with open(self.get_log_filename(), 'a') as log_file:
            log_file.write(datetime.now().strftime(self.get_full_date_format()) +
                           '\t' + command +
                           '\t' + comment)
            if command == self.get_char('finish_char'):
                log_file.write(' ' if comment[len(comment)-1:] in ['.', ',', ':', ';', '!', '?'] else '. ') # Append dot to comment if sentence is not closed
                log_file.write(worktime_str)
            log_file.write('\n')

    def log_status(self, command, comment, worktime_str):
        # Write to console
        if command == self.get_char('start_char'):
            print('Started.')
        elif command == self.get_char('continue_char'):
            print('Continuing. ' + worktime_str)
        elif command == self.get_char('finish_char'):
            if self.get_last_is_end():
                print('Already stopped. ' + worktime_str)
            else:
                print('Stopped. ' + worktime_str)

if __name__ == '__main__':
    log = WorkLog()
    log.set_log_filename(directory + datetime.strftime(datetime.now(), file_format))
    log.process_request()

__author__     = "Maurits van Mastrigt"
__license__    = "DWTFYWTPL"
__version__    = "0.1"
__maintainer__ = "Maurits van Mastrigt"
__email__      = "info@mauvm.nl"
__status__     = "Production"