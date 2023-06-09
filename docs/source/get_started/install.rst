Install XGCN
======================


System requirements
------------------------

XGCN supports Linux systems. for Windows users, it's recommended to install a 
Windows Subsystem for Linux (`WSL <https://learn.microsoft.com/en-us/windows/wsl/install>`_).


Install dependencies
------------------------------

Python 3.8 (or later), torch 1.7.0 (or later), dgl 0.9 (or later), torch_geometric 2.0 (or later) 
are required.
If you want to use GPU for training, please first manually install torch, dgl, and torch_geometric 
according to their official documentation. 


Install XGCN from source
------------------------------

Download the source files from GitHub and install locally:

.. code:: bash

    git clone git@github.com:xiransong/XGCN_library.git -b dev
    cd XGCN_library
    python -m pip install -e .
