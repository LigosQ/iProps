# iProps: A comprehensive software tool for protein classification and analysis with automatic machine learning capabilities and model interpretation capabilities.

# 中文版本
- zh_CN [简体中文](zh_CN.md)

# Dscription
- Detailed User manual:[Manual PDF](./manual.pdf)  
- iProp is a one-stop analysis software for protein binary classification. For two different types of Fasta files, This software has the capability to extract 22 types of individual features and supports the extraction of the top N primary individual features corresponding to 568 reduction schemes.  To enhance the flexibility and scalability of iProps, the feature extraction stage allows users to upload additional numerical feature files.  
- For the utilization of various types of protein numerical features in single-instance classification tasks, iProps offers a feature combination strategy that can combine up to four individual features.  Moreover, the software includes a classifier to provide an initial assessment of the classification performance for each computed feature.  Once all features are calculated, iProps sorts performance indicator data to identify numerical features with the best classification prediction performance.  
- iProps offers an automatic machine learning tool to search for the optimal classifier corresponding to the best predictive numerical features.  Lastly, iProps' model interpretation module can explain the process of confirming protein category using the user-defined classifier.  This module generates 23 diagrams that explain the decision-making process of the classifier from multiple perspectives.  Additionally, iProps features a user-friendly software interface, enabling semi-automated computation and analysis for users without a programming background. 

# Features
- Cross-platform software tools: Windows, Mac OS
- User-friendly interface and operation
- Up to 23 types of general feature calculations
- Supports up to 568 amino acid reduction schemes
- The most comprehensive support for reduced information
- Able to search for features of candidate combinations numbering in the thousands
- Automatic Machine Learning Ability
- Explanatory ability of the classification model
# Operation Example
![Work on Ubuntu](example.gif)

# This project is also hosted at
- [Gitee](https://gitee.com/zam1024t/LocalizedMenu)

# Installation
  1. Basic supporting environmentic  
     - install Anaconda
  2. Install other packages manually  
     - Enter the following command in the terminal of MacOS：
        ```
             pip install applescript==2021.2.9  
             pip install FLAML==2.0.2  
             pip install flet==0.11.0  
             pip install imbalanced_learn==0.10.1  
             pip install lazypredict==0.2.12  
             pip install nest_asyncio==1.5.6  
             pip install nicegui  
             pip install prettytable==3.9.0  
             pip install shap==0.42.1  
             pip install sweetviz==2.2.1  
             pip install TPOT==0.12.1  
             pip install umap-learn==0.5.3  
             pip install xgboost==1.7.6  
             pip install yellowbrick==1.5  
             pip install pywebview==4.4.1  
             conda install -c conda-forge lightgbm
        ```
     - Enter the following command in the cmd window of Windows:
        ```
            pip install applescript==2021.2.9  
            pip install FLAML==2.0.2  
            pip install flet==0.11.0  
            pip install imbalanced_learn==0.10.1  
            pip install lazypredict==0.2.12  
            pip install nest_asyncio==1.5.6  
            pip install nicegui  
            pip install prettytable==3.9.0  
            pip install shap==0.42.1  
            pip install sweetviz==2.2.1  
            pip install TPOT==0.12.1  
            pip install umap-learn==0.5.3  
            pip install xgboost==1.7.6  
            pip install yellowbrick==1.5  
            pip install pywebview==4.4.1  
            pip install lightgbm  
            pip install pypiwin32  
            python -m pip install --user --upgrade pywin32  
        ```

# Usage
- Go to the directory where iProps is located
	- via "cd" command in the terminal or cmd window
- Enter the Python command to launch the main window
	- `python main_Plus.py`, then you can see the main window of iProps

# Cite us
- Our papers are being submitted. Please quote our previous papers if you need to quote them.  
	> Feng Changli, Wu Jin, Wei Haiyan, Xu Lei, Zou Quan*. CRCF: A Method of Identifying Secretory Proteins of Malaria Parasites. IEEE/ACM Trans Comput Biol Bioinform. 2022 Jul-Aug;19(4):2149-2157. doi: 10.1109/TCBB.2021.3085589. Epub 2022 Aug 8. PMID: 34061749.

# Others
- All images generated in iProps are saved in local files as high-quality PNG images with a resolution of 300 DPI. These images are also saved as corresponding PDF files. Users can directly apply these images in their papers.   
	 - Images related to feature evaluation are stored in the **iProps/Results/**  directory.
	 - Files and images related to automated machine learning and model interpretation are stored in the **iProps/interpReport/** directory.
- Our references:
    - iFeature *by [Chen](https://pubmed.ncbi.nlm.nih.gov/29528364/)*:  
        >Zheng L, Huang S, Mu N, Zhang H, Zhang J, Chang Y, Yang L, Zuo Y. RAACBook: a web server of reduced amino acid alphabet for sequence-dependent inference by using Chou's five-step rule. Database (Oxford). 2019 Jan 1;2019:baz131.
    - RAACBook *by [Zuo](https://pubmed.ncbi.nlm.nih.gov/31802128/)*
		> Chen Z, Zhao P, Li F, Leier A, Marquez-Lago TT, Wang Y, Webb GI, Smith AI, Daly RJ, Chou KC, Song J. iFeature: a Python package and web server for features extraction and selection from protein and peptide sequences. Bioinformatics. 2018 Jul 15;34(14):2499-2502.
    - Pse-in-One *by [Liu](https://pubmed.ncbi.nlm.nih.gov/25958395/)*
		> Liu B, Liu F, Wang X, Chen J, Fang L, Chou KC. Pse-in-One: a web server for generating various modes of pseudo components of DNA, RNA, and protein sequences. Nucleic Acids Res. 2015 Jul 1;43(W1):W65-71. doi: 10.1093/nar/gkv458. Epub 2015 May 9. PMID: 25958395; PMCID: PMC4489303.

# License
[Apache v2.0](LICENSE)

