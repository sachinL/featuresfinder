#!/usr/bin/env python
# coding: utf-8

# In[12]:


from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from lightgbm import LGBMClassifier
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from sqlalchemy import create_engine
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def features(X1,y1):
            
            X = X1
            y = y1
            
            feature_name = list(X1.columns)
            num_feats = len(X.columns)
    
            cor_list = []
            feature_name = X.columns.tolist()
            # calculate the correlation with y for each feature
            for i in X.columns.tolist():
                cor = np.corrcoef(X[i], y)[0, 1]
                cor_list.append(cor)
            # replace NaN with 0
            cor_list = [0 if np.isnan(i) else i for i in cor_list]
            # feature name
            cor_feature = X.iloc[:,np.argsort(np.abs(cor_list))[-num_feats:]].columns.tolist()
            # feature selection? 0 for not select, 1 for select
            cor_support = [True if i in cor_feature else False for i in feature_name]
            
            print(str(len(cor_feature)), 'features are selected using Pearson correlation')


            X_norm = MinMaxScaler().fit_transform(X)
            chi_selector = SelectKBest(chi2, k=num_feats)
            chi_selector.fit(X_norm, y)
            chi_support = chi_selector.get_support()
            chi_feature = X.loc[:,chi_support].columns.tolist()
            print(str(len(chi_feature)), 'features are selected using Chi-Square Features')



            rfe_selector = RFE(estimator=LogisticRegression(), n_features_to_select=num_feats, step=10, verbose=5)
            rfe_selector.fit(X_norm, y)
            rfe_support = rfe_selector.get_support()
            rfe_feature = X.loc[:,rfe_support].columns.tolist()
            print(str(len(rfe_feature)), 'features are selected using Recursive Feature Elimination')



            embeded_lr_selector = SelectFromModel(LogisticRegression(penalty="l1"), max_features=num_feats)
            embeded_lr_selector.fit(X_norm, y)

            embeded_lr_support = embeded_lr_selector.get_support()
            embeded_lr_feature = X.loc[:,embeded_lr_support].columns.tolist()
            print(str(len(embeded_lr_feature)), 'features are selected using LogisticRegression')




            embeded_rf_selector = SelectFromModel(RandomForestClassifier(n_estimators=100), max_features=num_feats)
            embeded_rf_selector.fit(X, y)

            embeded_rf_support = embeded_rf_selector.get_support()
            embeded_rf_feature = X.loc[:,embeded_rf_support].columns.tolist()
            print(str(len(embeded_rf_feature)), 'features are selected using SelectFromModel-RandomForestClassifier')



            lgbc=LGBMClassifier(n_estimators=500, learning_rate=0.05, num_leaves=32, colsample_bytree=0.2,
                        reg_alpha=3, reg_lambda=1, min_split_gain=0.01, min_child_weight=40)

            embeded_lgb_selector = SelectFromModel(lgbc, max_features=num_feats)
            embeded_lgb_selector.fit(X, y)

            embeded_lgb_support = embeded_lgb_selector.get_support()
            embeded_lgb_feature = X.loc[:,embeded_lgb_support].columns.tolist()
            print(str(len(embeded_lgb_feature)), 'features are selected using SelectFromModel-LightGBM')

    
            # put all selection together
            feature_selection_df = pd.DataFrame({'Feature':feature_name, 'Pearson':cor_support, 'Chi-2':chi_support, 'RFE':rfe_support, 'Logistics':embeded_lr_support,
                                                'Random Forest':embeded_rf_support, 'LightGBM':embeded_lgb_support})
            # count the selected times for each feature
            feature_selection_df['Total'] = np.sum(feature_selection_df, axis=1)
            # display the top 100
            feature_selection_df = feature_selection_df.sort_values(['Total','Feature'] , ascending=False)
            feature_selection_df.index = range(1, len(feature_selection_df)+1)
            return feature_selection_df


# In[ ]:




