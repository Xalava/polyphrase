# PolyPhrase Password Generator

PolyPhrase generates secure and somewhat memorable passwords by combining words from multiple languages.

Typical output:
```console
~/polyphrase$ python polyphrase.py

PolyPhrase 1: 
conduce }0R pluvia muesli
Strength: 4/4           Crack time: centuries           length: 25
(Copied to clipboard)

PolyPhrase 2: 
lutteur gelare ovum 9#G
Strength: 4/4           Crack time: centuries           length: 23

PolyPhrase 3: 
@K7 raer audire deseo
Strength: 4/4           Crack time: centuries           length: 21
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/xalava/polyphrase.git
cd polyphrase
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
### Using a virtual environment
```bash
sudo apt install python3-venv || pip install python3-venv

python -m venv polyphrase-env
source polyphrase-env/bin/activate

pip install -r requirements.txt
```
(On visual code, ctrl+shift+P>"select python intepreter" to fix module missing messages)
### Optional script
For Unix users. **Adapt the path in polyphrase.sh.** Then:
```bash
cp polyphrase.sh ~/.local/bin/
chmod +x ~/.local/bin/polyphrase.sh
polyphrase.sh 
```
Additionally, you can now create a global shortcut for it. (On gnome settings> keyboard> global shortcut)

## Usage

### Command Line Interface

```bash
python polyphrase.py --language latin
```

Common options:
- `-l, --language`: Language choice [english, french, spanish, latin, poly] (default: poly)
- `-p, --password`: Check strength of an existing password

## Requirements

- Python 3.8 or higher
- NLTK
- zxcvbn
- pyperclip
- tkinter

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Ideas:
- bundle dictionnaries
- cross-platform testing
- bundle as a command line
- More advanced graphical interface
- Convert as a module (serving as library / commandline)

## Known Issues
- Only tested on Linux systems for the moment