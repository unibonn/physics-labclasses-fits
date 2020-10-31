## This are the updated versions of the scripts `chiFit.py` and `chi2FitXYErr.py` used in physics at University of Bonn.

## Requirements / How to install
Those scrips need to be executed usnig a terminal (Windows PowerShell, MacOS Terminal or Linux).  
You'll need an installation of [Python3](https://www.python.org/downloads/) on your System as well as some additional packages  
_Needed packages:_  
* numpy
* matplotlib
* scipy  

Use `pip3 install -r requirements.txt` to install all packages at once recursively.  
Please consider using a [*virtual environment*](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) when installing python packages on your system.  
Otherwise you're installing those packages globaly on your system which is a potential security flaw!  

### More Information
For more information on how to install packages using pythons own package manager `pip` and a terminal read the official [documentation](https://docs.python.org/3/installing/index.html#basic-usage)   
It's highly recommended to use a linux terminal, please have in mind that Windows added support for the Linux Kernel with Windows-Subsystem for Linux [WSL](https://docs.microsoft.com/de-de/windows/wsl/install-win10).  
Install python3 on linux: `apt-get install python3`    
Please have in mind that you may need `sudo` rights and the package manager might vary depending on your distro. 

#### Troubleshooting
There is a common mistake when installing python3:  
Set the checkmark on `add python to PATH` on the first dialogue page of the python3 installer. Otherwise pip will not work as expected.  
If you didn't set that checkmark or get some errors with pip anyways, try the following commands:  
`py -m pip install --upgrade pip`  
`py -m pip install SomePackage`  
_Notice:_ When using a Linux or macOS you need to use `python3 {...}` instead of `py {...}`  
   
`Matplotlib` isn't available for `python 3.9` yet (current date: 31.10.2020), please keep this in mind when choosing your version of python3.


## How to use 
* Navigate inside the terminal to the folder your python scripts are loacated in `cd {directory}` works in all terminals mentioned above.
* Execute the script by using `py {script}` or `python3 {script}`  
* If you don't know how to use them try `python3 {script} -h` this should give you all needed information.

There is also an example file `values.txt` included that shows how to format your data for correct usage.  

**Please don't forget to read and understand the code eventhough it's from an official source and easy to use!   
You can't trust any code you on the internet if you don't understand whats going on!**  

Contibutors:  
[Thomas Erben](https://github.com/terben)  
[Christoph Geron](https://github.com/nonchris)
[pbechtle](https://github.com/pbechtle)
