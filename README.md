# [Meet-U](http://www.meet-u.org/) 2018-2019: Team 8

## Team

We are all students of [BIM Master](http://www.lgm.upmc.fr/BIM/index.html) at [Sorbonne University](https://www.sorbonne-universite.fr/):

- [Antoine Gagelin](https://github.com/agagelin) (M2 - BIM)
- [André Lanrezac](https://github.com/Joffrin) (M2 - BIM)
- [Gaspar Roy](https://github.com/GasRoy) (M2 - BIM)
- [Florian Specque](https://github.com/fspecque) (M2 - BIM)
- [Yvan Sraka](https://github.com/yvan-sraka) (M2 - Info)

We use GitHub [Project View](https://github.com/meetU-MasterStudents/2018---2019-Equipe-8/projects/1) to organize our Product Management needs.

## Getting Started

### First Setup

```shell
# Install virtualenv package
sudo pip install virtualenv
# Create virtual environment
virtualenv ENV
# Activate virtual environment
source ENV/bin/activate
# Install project dependencies
pip install -r requirements.txt
```

### Run Tests

```shell
# Pyre type check (https://pyre-check.org/)
pyre check
```

## Technical Roadmap

### During the project, the following subjects must be explorated

- Scoring methods (DOPE, Rosetta, etc...)
- Reranking methods: which ML method is used? Which scores are used? Read the papers of CASP winners might be a good idea
- Threading improvement: can we introduce the side-chains? Can we insert residues which are not in the model?

### [v0.1.0](https://github.com/meetU-MasterStudents/2018---2019-Equipe-8/milestone/2) - Deadline: October 22, 2018

- [ ] Parser PDB
- [ ] Parser Foldrec
- [x] Create data structures for atoms, residues and proteins

### [v0.2.0](https://github.com/meetU-MasterStudents/2018---2019-Equipe-8/milestone/1) - Deadline: November 09, 2018

- [ ] Threading method
- [ ] Dope method
