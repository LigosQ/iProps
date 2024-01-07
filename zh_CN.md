# iProps: A comprehensive software tool for protein classification and analysis with automatic machine learning capabilities and model interpretation capabilities.

# 功能描述
- 使用手册:[Manual PDF](./manual.pdf)    
- 对于两种不同类型的Fasta文件，该软件具有提取22 种蛋白质数值特征的能力（考虑到氨基酸序列长度常有差异，有序列等长要求的数值特征暂未能提取）。该软件也支持评估568种候选约化方案中具有更好分类能力的前N个方案，然后计算这N个方案对应的数值特征。为了增强iProps的灵活性和可扩展性，特征评估阶段允许用户上传其他数值特征文件用于比较和组合。  
- 为了在分类任务中充分利用各种类型的蛋白质数值特征，iProps提供了一种特征组合策略。该策略可以在一个特征向量中组合多达四个单一特征。此外，该软件使用机器学习分类器对每个计算特征的分类性能进行初始评估。等待所有特征被评估后，iProps会依据识别准确率排序，以确定具有最佳分类性能的数值特征。
- iProps提供了一个自动机器学习工具来搜索适应上述最佳数值特征的分类器。获得最佳分类器后，iProps提供模型解释模块来可视化蛋白质类别预测的过程。该解释模块可以生成23个图表，从多个角度解释蛋白质分类的决策过程。此外，iProps是一个可免费访问的开源计算平台。它提供了一个用户友好的界面设计，允许轻松导航，即使没有编程经验的人也可以无缝使用它。


# Features
- 跨平台软件工具：Windows、Mac OS
- 用户友好的界面和操作
- 多达23种通用功能计算
- 全面支持多达568种氨基酸约化方案
- 最全面的支持减少信息
- 能够搜索数以千计的候选组合特征
- 自动机器学习能力
- 分类模型的解释能力
# 操作示例
![Work on Ubuntu](example.gif)

# 其他代码仓库
- [Gitee](https://gitee.com/zam1024t/LocalizedMenu)

# 安装
  1. 基础支持环境安装  
     - 首先现在并安装Anaconda
  2. 按住其他 Python 库 
     - 在 Mac OS 的终端中输入以下命令：
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
     - 在Windows系统的 CMD 窗口中输入以下命令:
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

# 使用方法
- 进入项目所在的目录
	- 通过 "cd" 命令进入 iProps所在的目录
- 输入 Python命令启动主窗口
	- `python main_Plus.py`

# 引用
- 我们的论文正在审稿. 如需引用请引用如下我们的早期论文：  
	> Feng Changli, Wu Jin, Wei Haiyan, Xu Lei, Zou Quan*. CRCF: A Method of Identifying Secretory Proteins of Malaria Parasites. IEEE/ACM Trans Comput Biol Bioinform. 2022 Jul-Aug;19(4):2149-2157. doi: 10.1109/TCBB.2021.3085589. Epub 2022 Aug 8. PMID: 34061749.

# 其他
- 在 iProps 中我们引用了如下的工作:
    - iFeature *by [Chen](https://pubmed.ncbi.nlm.nih.gov/29528364/)*:  
        >Zheng L, Huang S, Mu N, Zhang H, Zhang J, Chang Y, Yang L, Zuo Y. RAACBook: a web server of reduced amino acid alphabet for sequence-dependent inference by using Chou's five-step rule. Database (Oxford). 2019 Jan 1;2019:baz131.
    - RAACBook *by [Zuo](https://pubmed.ncbi.nlm.nih.gov/31802128/)*
		> Chen Z, Zhao P, Li F, Leier A, Marquez-Lago TT, Wang Y, Webb GI, Smith AI, Daly RJ, Chou KC, Song J. iFeature: a Python package and web server for features extraction and selection from protein and peptide sequences. Bioinformatics. 2018 Jul 15;34(14):2499-2502.
    - Pse-in-One *by [Liu](https://pubmed.ncbi.nlm.nih.gov/25958395/)*
		> Liu B, Liu F, Wang X, Chen J, Fang L, Chou KC. Pse-in-One: a web server for generating various modes of pseudo components of DNA, RNA, and protein sequences. Nucleic Acids Res. 2015 Jul 1;43(W1):W65-71. doi: 10.1093/nar/gkv458. Epub 2015 May 9. PMID: 25958395; PMCID: PMC4489303.

# 许可
[Apache v2.0](LICENSE)

