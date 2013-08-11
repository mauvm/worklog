# Worklog

As a freelancer administrative work is a necessary evil. This little Python script allows you to log your work very easily - through the usage of a CLI.

 - [What It Does](#what-it-does)
 - [Usage](#usage)
 - [Files](#files)
 - [Installation](#installation)
 - [Uninstallation](#uninstallation)
 - [Configuration](#configuration)
 - [Coming Up](#coming-up)
 - [License](#license)

## What It Does

Logging your work - and especially the time you spent working - should be easy and time inexpensive. _Worklog_ lets you log your work (dûh) in a very straightforward way.
Starting and continuing your work is done by calling the executable with a comment:

    $ worklog <comment>

This comment should hold information about the project your currently working on and what you are doing at that specific moment. But ofcourse, this is up to you.
Every time you log your work, the total working time is outputted to the console:

    $ worklog Refactoring shitty code from the previous developer..
    Continuing. Total of 0:03:45.

When you are done, finish logging with the `-f` flag:

    $ worklog -f Rounding up and committing work.
    Stopped. Total of 0:13:37.

This is what the actual log file will look like:

    2013-08-11 11:56:40    S    It's a lovely saturday!
    2013-08-11 12:00:25    |    Refactoring shitty code from the previous developer..
    2013-08-11 12:06:09    |    Doing some other work for some other client.
    2013-08-11 12:10:17    F    Rounding up and committing work. Total of 0:13:37.

The file is placed in a date formatted directory (see [configuration options](#configuration)):

    <worklog path>/2013/Week 31/2013-08-11.log

## Usage

Starting (and continuing) work is easily done with the `$ worklog <comment>` command. At the end you only have to finish working by running `$ worklog -f <comment>`.

**Note:** To use special characters in your comment, escape them (`\|`, `\"`, `\>`) or surround your comment in quotations (`worklog "<comment>"`).

_Worklog_ also allows you to show the status (and dump) your working log:

    $ worklog --help
    Usage: worklog [-d] [-s] [-r] [-f] <comment>

    Small Python logging tool to make work and time management real easy.

    Options:
      -h, --help           Show this help message and exit.
      -d, --dump           Dump log file.
      -s, --status         Print working status and total time.
      -r, --remove-record  Remove last record from the log.
      -f, --finish         Finish working.

## Files

The logged records are stored per line, with the data in a tab separated format - to make parsing the data real easy.
By default, the log file is placed in your profile directory (`~/Worklog/%Y/Week %U/%Y-%m-%d.log`, which translates into):

    Mac OSX   /Users/Maurits/Worklog/2013/Week 31/2013-08-11.log
    Linux     /home/Maurits/Worklog/2013/Week 31/2013-08-11.log
    Windows   C:\Users\Maurits\Worklog\2013\Week 31\2013-08-11.log

## Installation

### Mac OSX / Linux

Open your terminal application. Navigate to your [bin directory](http://www.linuxnix.com/2012/10/linux-directory-structure-explained-bin-folder.html):

    $ cd /usr/bin

**Note:** Change this to `cd ~/.bin` (for Linux) or `cd ~/bin` (for Mac OSX) to install _Worklog_ for your account only. When doing this, putting `sudo` in front of every command is not necessary.

#### A) Installation with Git:

Make sure [git is installed](http://git-scm.com/downloads). Then clone the repository into **worklog_bin**:

    $ sudo git clone https://github.com/mauvm/worklog worklog_bin --depth=1

**Note:** Update _Worklog_ by running `cd /usr/bin/worklog_bin; sudo git pull; sudo chmod +x worklog.py`.

#### B) Manual installation:

[Download this repository](https://github.com/mauvm/worklog/archive/master.zip) as `worklog-master.zip` and extract it to `/usr/bin/worklog_bin`:

    $ sudo unzip ~/Downloads/worklog-master.zip -d .
    $ sudo rm -rf worklog_bin
    $ sudo mv worklog-master worklog_bin

**Note:** Update _Worklog_ by repeating the __entire__ installation process again.

#### Finally:

Make the application executable:

    $ sudo chmod +x worklog_bin/worklog.py
    $ sudo ln -sf $PWD/worklog_bin/worklog.py worklog

And voilà, _Worklog_ is installed!

-----

### Windows

First, make sure [Python is in your PATH environment variable](http://docs.python.org/2/faq/windows).

Then open the command prompt (`Windows+R > "cmd" > Enter`) and run the following commands:

    > cd %USERPROFILE%
    > mkdir Worklog
    > cd Worklog

#### A) Installation with Git:

Make sure [git is installed](http://git-scm.com/downloads). Then clone this repository into the current working directory:

    > git clone https://github.com/mauvm/worklog.git worklog --depth=1

**Note:** Update _Worklog_ by repeating the installation process, but instead of `git clone https://git...` run `git pull`.

#### B) Manual installation:

[Download this repository](https://github.com/mauvm/worklog/archive/master.zip) as `worklog-master.zip` and extract it to the current working directory:

    > unzip ../Downloads/worklog-master.zip -d .
    > rm -rf worklog
    > rename worklog-master worklog

**Note:** Update _Worklog_ by repeating the __entire__ installation process again.

#### Finally:

To wrap it up, add `%USERPROFILE%\Worklog\worklog\lib\Windows\` to your ["Path" environment variable](http://www.nextofwindows.com/how-to-addedit-environment-variables-in-windows-7/) to be able to run `worklog <comment>` directly from the command prompt.

**Note:** The linked tutorial adds it to the _system variables_, which installs _Worklog_ systemwide. Add it to the _user variables_ section to install _Worklog_ for your account only.

And your done!

## Uninstallation

### Mac OSX / Linux

Uninstalling _Worklog_ can be done by simply deleting the bin folder and the symlink:

    $ sudo rm -rf /usr/bin/worklog_bin
    $ sudo rm -f /usr/bin/worklog

Optionally you can delete the log files too:

    $ rm -rf ~/Worklog

### Windows

First navigate to your profile directory:

    > cd %USERPROFILE%

To keep the log files but delete the _Worklog_ application, simply run:

    > rm -rf Worklog\worklog

Optionally you can uninstall _Worklog_ and delete the log files in one go:

    > rm -rf Worklog

## Configuration

Configuration options:

Option      | Default                 | Note
----------- | ----------------------- | -----------
directory   | ~/Worklog/              | `~` expands to your [home directory](http://en.wikipedia.org/wiki/Home_directory)
file_format | %Y/Week %U/%Y-%m-%d.log | 2013/Week 31/2013-08-11.log

**Note:** Be careful altering the _directory_ and _file_format_ options, since it wil create a new folder with each `/` (or `\` in Windows). Avoid using `..`.

## Coming Up

Some features I will be working on:

- Find a better name (I'm open for suggestions);
- Periodic pop-ups (to remind you of logging your work);
- Logging focused window titles (to recall/prove what you did);
- Option to export the log data;
- Website for statistics (upload export file, enter format, view working time graphs).

## License

                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                        Version 2, December 2004
    
     Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
    
     Everyone is permitted to copy and distribute verbatim or modified
     copies of this license document, and changing it is allowed as long
     as the name is changed.
    
                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
       TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
    
      0. You just DO WHAT THE FUCK YOU WANT TO.