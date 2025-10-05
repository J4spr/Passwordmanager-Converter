# KeepassXC to Proton

A python script that lets you import your exported passwords from KeePassXC into Proton pass

# Prerequisites

Requirements for the software and other tools to build, test and push

- [Python 3.12](https://www.python.org/downloads/release/python-3126/)
- [Git](https://git-scm.com)
- [passwords exported as csv](https://keepassxc.org/docs/KeePassXC_UserGuide#_exporting_databases)

# Installing

 1. Clone this repository

 ```bash
 git clone https://github.com/J4spr/Passwordmanager-Converter.git 
 ```

 2. run:

  ```bash
 python keepass_to_proton.py --source your-passwords.csv --out proton_ready.csv
 ```

## Authors

- **Billie Thompson** - *Provided README Template* -
    [PurpleBooth](https://github.com/PurpleBooth)
- **Jasper Vebruggen** - *built this python script*

## License

This project is licensed under the [WTFPL](LICENCE) License - see the [LICENSE.md](LICENCE.md) file for
details

## Acknowledgments

Feel free to open pull request because in the future I want to convert more password managers to other password managers
