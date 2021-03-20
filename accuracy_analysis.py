#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import scipy
import matplotlib
matplotlib.rcParams.update({'font.size': 16})


# In[2]:


# filename = "CogSci_Terry_Laia_Data_Export.tsv"
# tsv_read = pd.read_csv(filename, sep='\t')


# In[43]:


filename = "questionaire.csv"
df = pd.read_csv(filename, sep=",")


# In[44]:


len(df)


# In[45]:


df = df.drop([0, 1]) # drop the first 2 row (non-complete data)
df


# In[46]:


len(df)


# In[6]:


# Make a gender column
Gender = []
for i in range(2, len(df)+2):
    if df["Q01"][i] == 1:
        Gender.append("Male")
    else:
        Gender.append("Female")
df["Gender"] = Gender
        
# Make a expect_acc column
expect_acc = []
for i in df["Q02"]:
    expect_acc.append(i*10-5)
    
df["expect_acc"] = expect_acc

        
df = df.drop(["Q02"], axis = 1)
df = df.drop(["Q01"], axis = 1)
df.head()


# ## Calculate Expect ACC vs Actual ACC 

# In[7]:


## Create question list
questions = df.keys().drop(["Participant","Gender", "expect_acc"])
print(questions)

## Create an aswer sheet for comparison
answer = [2]*8 + [1]*8
print(answer)

## Calculate correctly-answered number
correct_number = []
for i in range(len(df)):
    correct = sum(list(answer == df[questions].iloc[i]))
    correct_number.append(correct)
    
##
df["actual_acc"] = correct_number
df["actual_acc_percent"] = (df["actual_acc"]/16)*100
df.head()


# In[8]:


print (df["actual_acc_percent"].mean())
print (df["actual_acc_percent"].std())
print (df["expect_acc"].mean())
print (df["expect_acc"].std())


# In[9]:


## Reorganize dataframe (easier for plotting)
# df_melted = acc_df.reset_index().melt(id_vars='index')
df_melt = pd.melt(df, id_vars=["Gender"], value_vars = ["expect_acc","actual_acc_percent"])


# In[10]:


max(df["actual_acc"])


# In[11]:


12/16


# In[13]:


plt.figure(figsize=(6, 6))
plt.style.use('seaborn-white')

sns.boxplot(x="variable", y="value", data=df_melt, width = 0.25)

plt.ylabel("Accuracy")
plt.xlabel("")
plt.xticks([0,1], ["Expect","Actual"])
sns.despine(left=False, bottom=False)

# plt.savefig("../result_graph/expect_actual.png",bbox_inches='tight', dpi = 300)


# In[14]:


# !!!! T-test results !!!!

scipy.stats.ttest_rel(df["actual_acc_percent"], df["expect_acc"])


# In[15]:


# Male Expect
me = df_melt[(df_melt["Gender"]=="Male") & (df_melt["variable"]=="expect_acc")]["value"]

# Female Expect
fe = df_melt[(df_melt["Gender"]=="Female") & (df_melt["variable"]=="expect_acc")]["value"]

# Male Actual
ma = df_melt[(df_melt["Gender"]=="Male") & (df_melt["variable"]=="actual_acc_percent")]["value"]

# Female Actual
fa = df_melt[(df_melt["Gender"]=="Female") & (df_melt["variable"]=="actual_acc_percent")]["value"]


# In[16]:


print(len(me))
print(len(fe))
print(len(ma))
print(len(fa))

print(scipy.stats.ttest_ind(me, fe))
print(scipy.stats.ttest_ind(ma, fa))


# In[18]:


plt.figure(figsize=(3, 3))
plt.style.use('seaborn-white')

sns.catplot(x="variable", y="value",hue = "Gender",
                capsize=.2, palette="tab10",
                kind="point", data=df_melt)

#plt.plot([51.333333,42.03701], color = "red")
plt.ylabel("Accuracy")
plt.xlabel("")
plt.xticks([0,1], ["Expect","Actual"])
# plt.savefig("../result_graph/gender_difference.png",bbox_inches='tight', dpi = 300)


# In[19]:


#sns.barplot(data=df_melted, x = "variable", y='value')


# In[20]:


# plt.figure(figsize=(3.5, 3.5))
# sns.catplot(x="variable", y="value",
#                 capsize=.2, palette="Paired",height = 8, aspect = 0.7,
#                 kind="point", data=df_melted)

# plt.plot([51.333333,42.03701], color = "red")
# plt.ylabel("Accuracy")
# plt.xlabel("")
# plt.xticks([0,1], ["Expect Accuracy","Actual Accuracy"])


# ## Calculate with_without audio

# In[21]:


pd.options.mode.chained_assignment = None  # default='warn'

audio_df = df[["Participant", "L1", "L2", "L3", "T4","T5","T6","L7","T8", "Gender"]]
audio_answer = [2,2,2,1,1,1,2,1]


# In[22]:


audio_correct_matrix = audio_df[["L1", "L2", "L3", "T4","T5","T6","L7","T8"]] == audio_answer


# In[23]:


audio_correct = []
for i in range(len(audio_correct_matrix)):
    audio_correct.append(np.sum(audio_correct_matrix.iloc[i]))


# In[24]:


audio_df["actual_acc"] = audio_correct
audio_df["actual_acc_percent"] = (audio_df["actual_acc"]/8)*100
audio_df["label"] = "audio"


# In[25]:


audio_df.head()


# In[26]:


mute_df = df[["Participant", "T9", "T10", "L11", "T12","L13","L14","L15","T16", "Gender"]]
mute_answer = [1,1,2,1,2,2,2,1]

mute_correct_matrix = mute_df[["T9", "T10", "L11", "T12","L13","L14","L15","T16"]] == mute_answer


# In[27]:


mute_correct = []
for i in range(len(mute_correct_matrix)):
    mute_correct.append(np.sum(mute_correct_matrix.iloc[i]))


# In[28]:


mute_df["actual_acc"] = mute_correct
mute_df["actual_acc_percent"] = (mute_df["actual_acc"]/8)*100
mute_df["label"] = "mute"
mute_df.head()


# In[29]:


audio_df.keys()


# In[30]:


print(audio_df.keys())
sound_effect = pd.concat([audio_df[['Participant', 'Gender', 'actual_acc_percent', 'actual_acc', 'label' ]], 
                          mute_df[['Participant', 'Gender', 'actual_acc_percent', 'actual_acc', 'label']]], axis = 0)


# In[31]:


sound_effect.head()


# In[32]:


audio_df_melt = pd.melt(audio_df, id_vars = ["Gender"], value_vars = ["actual_acc_percent"])
audio_df_melt.head()


# In[33]:


mute_df.head()


# In[34]:


len(sound_effect)


# In[35]:


print(len(sound_effect[sound_effect["label"] == "audio"]["actual_acc_percent"]))
print("Mean", np.mean(sound_effect[sound_effect["label"] == "audio"]["actual_acc_percent"]))
print("Std", np.std(sound_effect[sound_effect["label"] == "audio"]["actual_acc_percent"]))

print(len(sound_effect[sound_effect["label"] == "mute"]["actual_acc_percent"]))
print("Mean", np.mean(sound_effect[sound_effect["label"] == "mute"]["actual_acc_percent"]))
print("Std", np.std(sound_effect[sound_effect["label"] == "mute"]["actual_acc_percent"]))


# In[38]:


plt.figure(figsize=(6, 6))
plt.style.use('seaborn-white')

sns.boxplot(x="label", y="actual_acc_percent", data=sound_effect, width = 0.25)

plt.ylabel("Accuracy")
plt.xlabel("")
plt.xticks([0,1], ["Audio","Mute"])
sns.despine(left=False, bottom=False)

# plt.savefig("../result_graph/audio_expect_actual.png",bbox_inches='tight', dpi = 300)


# In[39]:


scipy.stats.ttest_rel(sound_effect[sound_effect["label"] == "audio"]["actual_acc_percent"],
                      sound_effect[sound_effect["label"] == "mute"]["actual_acc_percent"])


# In[40]:


max(sound_effect[sound_effect["label"] == "audio"]["actual_acc"])


# In[41]:


max(sound_effect[sound_effect["label"] == "mute"]["actual_acc"])


# In[42]:


df


# In[ ]:




