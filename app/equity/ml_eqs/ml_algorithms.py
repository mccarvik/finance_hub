import sys, datetime, pdb, time
sys.path.append('/usr/share/doc')
sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/usr/local/lib/python3.4/dist-packages")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
sys.path.append("/home/ubuntu/workspace/finance")
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from app import app
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import Perceptron as perceptron_skl
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import Imputer, LabelEncoder, OneHotEncoder, MinMaxScaler, StandardScaler
from app.equity.ml_eqs.perceptron import Perceptron
from app.equity.ml_eqs.adalinegd import AdalineGD
from app.equity.ml_eqs.adalinesgd import AdalineSGD
from app.equity.ml_eqs.ml_utils import plot_decision_regions, standardize

IMG_PATH = '/home/ubuntu/workspace/finance/app/static/img/ml_imgs/'

def run_perceptron(df, eta=0.1, n_iter=10):
    ''' Takes the pruned dataframe and runs it through the perceptron class
    
        Parameters
        ==========
        df : dataframe
            dataframe with the inputs and target
        eta : float
            learning rate between 0 and 1
        n_iter : int
            passes over the training dataset
        
        Return
        ======
        NONE
    '''
    t0 = time.time()
    y = df['target']
    X = df[['divYield','priceToBook']]
    
    buy = df[df['target'] > 0][list(X.columns)].values
    sell = df[df['target'] < 0][list(X.columns)].values
    plt.figure(figsize=(7,4))
    plt.scatter(buy[:, 0], buy[:, 1], color='blue', marker='x', label='Buy')
    plt.scatter(sell[:, 0], sell[:, 1], color='red', marker='s', label='Sell')
    plt.xlabel(list(X.columns)[0])
    plt.ylabel(list(X.columns)[1])
    plt.legend()
    ppn = Perceptron(eta, n_iter)
    ppn.fit(X.values, y.values)
    # pdb.set_trace()
    plot_decision_regions(X.values, y.values, classifier=ppn)
    plt.savefig(IMG_PATH + "scatter.png")
    plt.close()
    
    # print('Accuracy: %.2f' % accuracy_score(y_test, y_pred))
    
    plt.plot(range(1,len(ppn.errors_) + 1), ppn.errors_,marker='o')
    plt.xlabel('Iterations')
    plt.ylabel('Number of misclassifications')
    plt.savefig(IMG_PATH + "misclassifications.png")
    plt.close()
    
    t1 = time.time()
    app.logger.info("Done training data and creating charts, took {0} seconds".format(t1-t0))
    print("Done training data and creating charts, took {0} seconds".format(t1-t0))
    
def run_perceptron_multi(df, eta=0.1, n_iter=15):
    t0 = time.time()
    y = df['target']
    X = df[['returnOnEquity','currentRatio']]
    
    # Split up the training and test data and standardize inputs
    X_train, X_test, y_train, y_test = \
          train_test_split(X, y, test_size=0.3, random_state=0)
    X_train_std, X_test_std = standardize(X_train, X_test)

    # pdb.set_trace()
    strong_buy = df[df['target'] == 3][list(X.columns)].values
    buy = df[df['target'] == 2][list(X.columns)].values
    sell = df[df['target'] == 1][list(X.columns)].values
    strong_sell = df[df['target'] == 0][list(X.columns)].values
    
    plt.figure(figsize=(7,4))
    plt.scatter(buy[:, 0], buy[:, 1], color='blue', marker='x', label='Buy')
    plt.scatter(sell[:, 0], sell[:, 1], color='red', marker='s', label='Sell')
    plt.scatter(strong_buy[:, 0], strong_buy[:, 1], color='blue', marker='*', label='Strong Buy')
    plt.scatter(strong_sell[:, 0], strong_sell[:, 1], color='red', marker='^', label='Strong Sell')
    plt.xlabel(list(X.columns)[0])
    plt.ylabel(list(X.columns)[1])
    plt.legend()
    
    ppn = perceptron_skl(n_iter=40, eta0=0.1, random_state=0)
    ppn.fit(X_train_std, y_train)
    y_pred = ppn.predict(X_test_std)

    print('Accuracy: %.2f' % accuracy_score(y_test, y_pred))
    plot_decision_regions(X.values, y.values, classifier=ppn)
    plt.savefig(IMG_PATH + "scatter.png")
    plt.close()
    
    t1 = time.time()
    app.logger.info("Done training data and creating charts, took {0} seconds".format(t1-t0))
    print("Done training data and creating charts, took {0} seconds".format(t1-t0))

def adalinegdLearningExample(df, eta=0.1, n_iter=10):
    # Learning rate too high - overshoot global min
    y = df['target']
    X = df[['trailingPE','priceToBook']]
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
    ada1 = AdalineGD(n_iter=20, eta=0.01).fit(X, y)
    ax[0].plot(range(1, len(ada1.cost_) + 1), np.log10(ada1.cost_), marker='o')
    ax[0].set_xlabel('Epochs')
    ax[0].set_ylabel('log(Sum-squared-error)')
    ax[0].set_title('Adaline - Learning rate 0.01')
    
    # Learning rate too low - takes forever
    ada2 = AdalineGD(n_iter=20, eta=0.0001).fit(X, y)
    ax[1].plot(range(1, len(ada2.cost_) + 1), ada2.cost_, marker='o')
    ax[1].set_xlabel('Epochs')
    ax[1].set_ylabel('Sum-squared-error')
    ax[1].set_title('Adaline - Learning rate 0.0001')
    
    plt.tight_layout()
    plt.savefig(IMG_PATH + "adaline_1.png", dpi=300)
    plt.close()
    # plt.show()
    
def adalineSGD(df, eta=0.1, n_iter=10):
    y = df['target']
    X = df[['trailingPE','priceToBook']]
    
    # standardize features
    X_std = np.copy(X.values)
    # X_std[:,0] = (X.values[:,0] - X.values[:,0].mean()) / X.values[:,0].std()
    # X_std[:,1] = (X.values[:,1] - X.values[:,1].mean()) / X.values[:,1].std()
    
    ada = AdalineSGD(n_iter=15, eta=0.001, random_state=1)
    # pdb.set_trace()
    ada.fit(X_std, y.values)
    # pdb.set_trace()
    # ada.partial_fit(X_std, y.values)
    
    plot_decision_regions(X_std, y.values, classifier=ada)
    plt.title('Adaline - Gradient Descent')
    plt.xlabel(list(X.columns)[0])
    plt.ylabel(list(X.columns)[1])
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(IMG_PATH + 'adalinesgd.png', dpi=300)
    plt.close()
    
    plt.plot(range(1, len(ada.cost_) + 1), ada.cost_, marker='o')
    plt.xlabel('Epochs')
    plt.ylabel('Sum-squared-error')
    plt.tight_layout()
    plt.savefig(IMG_PATH + 'adalinesgd_gd.png', dpi=300)
    plt.close()

def adalineGD(df, eta=0.1, n_iter=10):
    y = df['target']
    X = df[['returnOnEquity','debtToEquity']]
    
    # standardize features
    X_std = np.copy(X.values)
    # X_std[:,0] = (X.values[:,0] - X.values[:,0].mean()) / X.values[:,0].std()
    # X_std[:,1] = (X.values[:,1] - X.values[:,1].mean()) / X.values[:,1].std()
    
    ada = AdalineGD(n_iter=15, eta=0.00001)
    ada.fit(X_std, y)
    
    plot_decision_regions(X_std, y.values, classifier=ada)
    plt.title('Adaline - Gradient Descent')
    plt.xlabel(list(X.columns)[0])
    plt.ylabel(list(X.columns)[1])
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(IMG_PATH + 'adaline_2.png', dpi=300)
    plt.close()
    
    plt.plot(range(1, len(ada.cost_) + 1), ada.cost_, marker='o')
    plt.xlabel('Epochs')
    plt.ylabel('Sum-squared-error')
    plt.tight_layout()
    plt.savefig(IMG_PATH + 'adaline_3.png', dpi=300)
    plt.close()
    
def logisticRegression(df, cols):
    # Need this in case cols is tuple for timing purposes
    cols = list(cols)
    pdb.set_trace()
    y = df['target']
    X = df[cols]
    X_train, X_test, y_train, y_test = \
          train_test_split(X, y, test_size=0.3, random_state=0)
    
    # Normalization of the data
    mms = MinMaxScaler()
    X_train_norm = mms.fit_transform(X_train)
    X_test_norm = mms.transform(X_test)
    
    # Standardization of the data
    stdsc = StandardScaler()
    X_train_std = stdsc.fit_transform(X_train)
    X_test_std = stdsc.transform(X_test)
    
    pdb.set_trace()
    lr = LogisticRegression(penalty='l1', C=0.1)
    lr.fit(X_train_std, y_train)
    print('Training accuracy:', lr.score(X_train_std, y_train))
    print('Test accuracy:', lr.score(X_test_std, y_test))
    print(lr.intercept_)
    print(lr.coef_)
    
    fig = plt.figure()
    ax = plt.subplot(111)
      
    colors = ['blue', 'green', 'red', 'cyan', 
           'magenta', 'yellow', 'black', 
            'pink', 'lightgreen', 'lightblue', 
            'gray', 'indigo', 'orange']
    
    pdb.set_trace()
    weights, params = [], []
    for c in np.arange(-4, 6):
      lr = LogisticRegression(penalty='l1', C=10**c, random_state=0)
      lr.fit(X_train_std, y_train)
      weights.append(lr.coef_[0])
      params.append(10**c)
    
    weights = np.array(weights)
    
    for column, color in zip(range(weights.shape[1]), colors):
        plt.plot(params, weights[:, column],
               label=df.columns[column+1],
               color=color)
    plt.axhline(0, color='black', linestyle='--', linewidth=3)
    plt.xlim([10**(-5), 10**5])
    plt.ylabel('weight coefficient')
    plt.xlabel('C')
    plt.xscale('log')
    plt.legend(loc='upper left')
    ax.legend(loc='upper center', 
            bbox_to_anchor=(1.38, 1.03),
            ncol=1, fancybox=True)
    plt.savefig(IMG_PATH + 'l1_path.png', dpi=300)
    plt.close()