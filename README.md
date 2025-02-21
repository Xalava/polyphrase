# PolyPhrase Password Generator

PolyPhrase generates memorable yet secure passwords by combining words from multiple languages. 

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

### Optional script
For Unix users:
```bash
cp polyphrase.sh ~/.local/bin/
chmod +x ~/.local/bin/polyphrase.sh
polyphrase.sh 
```
Additionally, you can now create a global shortcut for it. (On gnome settings> keyboard> global shortcut)

### Graphical Interface

Run the GUI version:
```bash
python polyphrase_gui.py
```

### Command Line Interface

Generate passwords from the command line:
```bash
python polyphrase.py -n 3 -w 4 -l poly
```

Options:
- `-n, --num-passwords`: Number of passwords to generate (default: 3)
- `-w, --words`: Number of words per password (default: 4)
- `-l, --language`: Language choice ['english', 'french', 'spanish', 'latin', 'poly'] (default: poly)
- `-p, --password`: Check strength of an existing password

## Requirements

- Python 3.8 or higher
- NLTK
- zxcvbn
- pyperclip
- tkinter (included with Python)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Ideas:
- bundle dictionnaries
- cross-platform testing
- bundle as a command line
- More advance graphical interface

## Known Issues
- Only tested on Linux systems for the moment
- On Linux systems, `xclip` must be installed for clipboard functionality