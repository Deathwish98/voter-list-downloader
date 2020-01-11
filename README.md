# Voter List Downloader

Downloads voter lists from ceodelhi website by specifying AC no.

## Setting up environment

- Install virtual environment
```
pip install virtualenv
```
- Create a virtual environment named env using the following command
```
virtualenv env
```
- Run the following command to install the dependencies
```
pip install -r requirements.txt
```

## Notes

- The repo contains chrome driver for chrome version 79. If your chrome version is not 79, download chrome driver for your respective version and replace chromedriver.exe in project
## Running

```
python downloader.py
```