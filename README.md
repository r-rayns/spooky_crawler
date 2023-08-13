# spooky_crawler

## Install

1. Install the Python package manager pip.
    
```bash
  sudo apt install python3-pip
```
    
2. Install Python virtual environment support.
    
```bash
  sudo apt install python3-venv
```
    
3. Create a new directory in your home folder for your Python virtual environments and change directories into it.
    
```bash
  mkdir python-virtual-environments 
  cd python-virtual-environments
```
    
4. Create a new virtual environment
    
```bash
  python3 -m venv ~/venv/spooky
```
    
5. Activate the virtual environment. **Note**: *If you want to exit the virtual environment just type `deactivate`*.
    
```bash
  source ~/venv/spooky/bin/activate
```
6. Install the required packages.

```bash
  cd ~/spooky_crawler
  pip install -r requirements.txt
```

## .env
HOST - host to run under e.g. http://localhost:8080
API_TOKEN - token to access the spooky_kingdom API