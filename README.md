# multibox
This program is a frontend to the Dropbox Client for Linux that enables you to access **more than one Dropbox** at a time.
It can be executed with both Python 2.x and 3.x on Unix machines (although only tested on Linux).

## Getting started
### Download Dropbox Client 
First of all you need to install (or simply extract) the official Dropbox Client from https://www.dropbox.com/install?os=lnx .
This software contains a script called `dropboxd`. You need to make that command available by setting `$PATH` accordingly.

### Downloading and Installing multibox
Simply fetch the sources via git and install them by using `setup.py`:
```bash
$ cd  /tmp
$ git clone https://github.com/p-ho/multibox.git
[...]
$ cd multibox/
$ python setup.py install
```
You might need root permissions to execute the install command or you could use a virtual environment.
If - for whatever reason - you don't want to install you could simply use the bare module at  https://github.com/p-ho/multibox/blob/master/multibox.py .

### Using multibox
Now you can issue the command `multibox`:
```bash
$ multibox --version
multibox 0.2.1
```
So let's start to initialize a Dropbox location. First of all choose/create a folder preferably an empty one (_[myfolder]_).
Start by issuing:
```bash
$ multibox [myfolder]
```
Then, if you run a graphical environment, a window should appear asking for the credentials to access your Dropbox.
Enter them and sign in (or create a new account). Afterwards you can simply close the window. Now nautilus will pop up
displaying an error dialog. You can simply ignore it and close the windows.
If you run a non-graphical (e.g. headless) environment you will be presented an URL you need to follow.

When done with that an Dropbox icon should appear in your status bar (of course only in graphical envs) and the client
starts to synchronize your files from your Dropbox to `[myfolder]/Dropbox`.

You can terminate the process at any time by opening the context menu of the Dropbox icon and clicking _Quit_, by
issuing `Ctrl` + `C` in command line or sending an `SIGTERM` signal to the process.

The next time you execute `$ multibox [myfolder]` the synchronization will resume.

You can repeat these steps for each Dropbox you might want to connect to. Of course pick different folders for each of them.

### multibox Flags
The following flags can be added when executing multibox:
```bash
$ multibox --nogui --force --async [myfolder]
```
 - **nogui:** mimic an headless environment
 - **async:** fires off the Dropbox Client an returns immediately
 - **force:** disables various checks (NOT recommended)
 
## License
This program is licensed under [GNU General Public License v3 (GPLv3)](https://www.gnu.org/licenses/gpl.html)
