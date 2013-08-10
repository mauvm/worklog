## Worklog

As a freelancer administrative work is a necessary evil. This little Python script allows you to log your work very easily - through the usage of a CLI.

### What It Does

Logging your work - and especially the time you spent working - should be easy and time inexpensive. _Worklog_ lets you log your work (duh) in a very straightforward way. Starting and continuing your work is done by calling the executable with a comment:

    $ worklog <comment>

This comment should hold information about the project your currently working on and what you are doing at that specific moment. But ofcourse, this is up to you.
Every time you log your work, the total working time is outputted to the console:

    $ worklog Refactoring shitty code from the previous developer..
    Continuing. Total of 0:03:45.

When you are done, finish logging with the `-f` flag:

    $ worklog -f Rounding up and committing work.
    Stopped. Total of 0:13:37.

This is how the actual log file looks like:

    2013-08-10 11:56:40    S    It's a lovely saturday!
    2013-08-10 12:00:25    |    Refactoring shitty code from the previous developer..
    2013-08-10 12:06:09    |    Doing some other work for some other client.
    2013-08-10 12:10:17    F    Rounding up and committing work. Total of 0:13:37.

The file is placed in a date formatted directory (see configuration options):

    <worklog path>/2013/Week 31/2013-08-10.txt

### Installation

#### Mac OSX / Linux

Open your terminal application. Navigate to your [bin directory](http://www.linuxnix.com/2012/10/linux-directory-structure-explained-bin-folder.html):

    $ cd /usr/bin

**NOTE:** Change this to `cd ~/.bin` to use the bin directory of your profile on Linux. When doing this, putting `sudo` in front of every command is not necesarry.

Clone the repository into **worklog_bin** and make the application executable:

    $ sudo git clone https://github.com/mauvm/worklog worklog_bin
    $ sudo chmod +x worklog_bin/worklog.py
    $ sudo ln -sf ${PWD}/worklog_bin/worklog.py worklog

And voilà, _Worklog_ is installed!

**NOTE:** Updating _Worklog_ is easy:

    $ sudo cd /usr/bin/worklog_bin
    $ sudo git pull
    $ sudo chmod +x worklog.py

#### Windows

First, make sure [Python is in your PATH environment variable](http://docs.python.org/2/faq/windows) and [git is installed](http://msysgit.github.io/).

Then open the command prompt (`Windows+R > cmd > Enter`) and run the following commands:

    > cd %SYSTEMDRIVE%\Users\%USERNAME%\
    > mkdir Worklog
    > cd Worklog
    > git clone https://github.com/mauvm/worklog.git

To wrap it up, add `%SYSTEMDRIVE%\Users\%USERNAME%\Worklog\worklog\lib\` to your ["Path" _user variable_](http://www.nextofwindows.com/how-to-addedit-environment-variables-in-windows-7/) to be able to run `> worklog <comment>` directly from the command prompt.

**NOTE:** The linked tutorial adds it to the _system variable_, dont do this - it installs _Worklog_ systemwide.

And your done!

**NOTE:** Updating _Worklog_ is easy:

    $ cd %SYSTEMDRIVE%\Users\%USERNAME%\Worklog\worklog
    $ git pull

### Usage

Starting (and continuing) work is easily done with the `$ worklog <comment>` command. At the end you only have to finish working by running `$ worklog -f <comment>`.

_Worklog_ also allows you to show the status (and dump) your working log:

    $ worklog --help
    Usage: worklog [options]

    Options:
      -h, --help    show this help message and exit
      -d, --dump    Dump log file.
      -s, --status  Print working status and total time.
      -f, --finish  Finish working.

### Files

The logged records are stored per line, with the data in a tab separated format - to make parsing the data real easy.
By default, the log file is placed in your profile directory (`~/Worklog/%Y/Week %U/%Y-%m-%d.txt` which translates into):

    Mac OSX / Linux    /home/<your username>/Worklog/2013/Week 31/2013-08-10.txt
    Windows            C:\Users\<your username>\Worklog\2013\Week 31\2013-08-10.txt

### Configuration

Configuration options:

    date_format    %Y-%m-%d
    time_format    %H:%M:%S
    directory      path of the worklog executable
    filename       %Y/Week %U/%Y-%m-%d.txt (2013/Week 31/2013-08-10.txt)
    start_char     S
    continue_char  |
    stop_char      F

**NOTE:** Be careful altering the _directory_ and _filename_ options, since it wil create a new folder with each / (or \ in Windows). Avoid using `..`.

### To Do

- Improve code structure (I do not master the Python philosophy yet);
- Create simplistic GUI;
- Periodic pop-up (to remind you of logging your work);
- Logging focused window titles (to recall/prove what you did)
- API for exporting the data;
- Website for statistics (upload export file, enter format, view working time graphs)
- Test on multiple platforms.

### License

                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                        Version 2, December 2004
    
     Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
    
     Everyone is permitted to copy and distribute verbatim or modified
     copies of this license document, and changing it is allowed as long
     as the name is changed.
    
                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
       TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
    
      0. You just DO WHAT THE FUCK YOU WANT TO.