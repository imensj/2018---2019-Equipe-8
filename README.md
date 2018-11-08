# [Meet-U](http://www.meet-u.org/) 2018-2019: Team 8 [![CircleCI](https://circleci.com/gh/meetU-MasterStudents/2018---2019-Equipe-8.svg?style=svg)](https://circleci.com/gh/meetU-MasterStudents/2018---2019-Equipe-8)

## Team

We are all students of [BIM Master](http://www.lgm.upmc.fr/BIM/index.html) at [Sorbonne University](https://www.sorbonne-universite.fr/):

- [Antoine Gagelin](https://github.com/agagelin) (M2 - BIM)
- [André Lanrezac](https://github.com/Joffrin) (M2 - BIM)
- [Gaspar Roy](https://github.com/GasRoy) (M2 - BIM)
- [Florian Specque](https://github.com/fspecque) (M2 - BIM)
- [Yvan Sraka](https://github.com/yvan-sraka) (M2 - Info)

We use GitHub [Project View](https://github.com/meetU-MasterStudents/2018---2019-Equipe-8/projects/1) to organize our Product Management needs.

## Getting Started

### Prerequisites

1. Install [Git LFS](https://git-lfs.github.com/) and [pypy3](https://pypy.org/) on your computer

2. Clone this repository
    ```shell
    git clone https://github.com/meetU-MasterStudents/2018---2019-Equipe-8.git ~/meetU-2018-2019-Equipe-8
    ```

3. Setup Python [virtual environment](https://virtualenv.pypa.io/en/latest/)
    ```shell
    # Install virtualenv package
    sudo pypy3 -m pip install virtualenv
    # Go inside the repository
    cd ~/meetU-2018-2019-Equipe-8
    # Create virtual environment
    pypy3 -m virtualenv -p $(which pypy3) venv
    ```

### Running

1. Enter virtual environment and install python dependencies
    ```shell
    # Go inside the repository
    cd ~/meetU-2018-2019-Equipe-8
    # Activate virtual environment
    source venv/bin/activate
    # Install project dependencies
    pip install -r requirements.txt
    ```

2. Run tests
    ```shell
    # Pytest (https://docs.pytest.org/en/latest/getting-started.html)
    pytest TEST_*.py
    # Pyre type check (https://pyre-check.org/)
    pyre check
    ```

## Technical Roadmap

### During the project, the following subjects must be explorated

- Scoring methods (DOPE, Rosetta, co-evolution, etc...)
- Reranking methods: which ML method is used? Which scores are used? Read the papers of CASP winners might be a good idea
- Threading improvement: can we introduce the side-chains? Can we insert residues which are not in the model?
  - Re-weighting scores: Sequence coverage, gaps in query, etc.
  - ...

### [v0.1.0](https://github.com/meetU-MasterStudents/2018---2019-Equipe-8/milestone/2) - Deadline: October 22, 2018

- [x] Parser PDB
- [x] Parser Foldrec
- [x] Create data structures for atoms, residues and proteins

### [v0.2.0](https://github.com/meetU-MasterStudents/2018---2019-Equipe-8/milestone/1) - Deadline: November 09, 2018

- [x] Threading method
- [x] Dope method
