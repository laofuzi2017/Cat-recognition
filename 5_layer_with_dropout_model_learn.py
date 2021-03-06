#coding:utf-8
__author__ = 'Administrator'

import h5py
import numpy as np
import matplotlib.pyplot as plt
from modelmanage import model
import os

def load_dataset():
    """
    # 加载数据集
    """
    train_dataset = h5py.File('datasets/train_catvnoncat.h5', "r")  # 读取H5文件

    # for t in train_dataset:
    #     print(t)
    # set_x=train_dataset["train_set_y"]
    # print(set_x.shape)
    # list_classes=train_dataset["list_classes"]
    # print(list_classes.shape)
    # for l in list_classes:
    #     print(l)
    train_set_x_orig = np.array(train_dataset["train_set_x"][:])  # your train set features
    train_set_y_orig = np.array(train_dataset["train_set_y"][:])  # your train set labels

    # print(train_set_x_orig.shape)
    # print(train_set_y_orig.shape)
    test_dataset = h5py.File('datasets/test_catvnoncat.h5', "r")
    test_set_x_orig = np.array(test_dataset["test_set_x"][:])  # your test set features
    test_set_y_orig = np.array(test_dataset["test_set_y"][:])  # your test set labels

    classes = np.array(test_dataset["list_classes"][:])  # the list of classes

    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))  # 对训练集和测试集标签进行reshape
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))


    #矩阵转置
    train_x=train_set_x_orig.reshape(train_set_x_orig.shape[0],-1).T
    test_x=test_set_x_orig.reshape(test_set_x_orig.shape[0],-1).T
    train_y=train_set_y_orig.reshape(train_set_y_orig.shape[1],1).T
    test_y=test_set_y_orig.reshape(test_set_y_orig.shape[1],1).T
    list_classes=classes.reshape(classes.shape[0],1).T
    return train_x, train_y, test_x, test_y, list_classes

def save_params(params):
    cur_filepath=os.path.basename(os.path.realpath(__file__))
    cur_file,ext=os.path.splitext(cur_filepath)
    filename=cur_file+".h5"
    f=h5py.File(filename,'w')
    for k,v in params.items():
        f.create_dataset(k,data=v)

def predict_y(x,params):
    W1=params["W1"]
    b1=params["b1"]
    W2=params["W2"]
    b2=params["b2"]
    W3=params["W3"]
    b3=params["b3"]
    W4=params["W4"]
    b4=params["b4"]
    #测试用例样本数
    test_m=x.shape[1]
    prediction_Y=np.zeros((1,test_m))
    #计算
    A1,Z1=model.l_layer_forward_model(x,W1,b1,acitvation="relu") #第1层
    A2,Z2=model.l_layer_forward_model(A1,W2,b2,acitvation="relu") #第2层
    A3,Z3=model.l_layer_forward_model(A2,W3,b3,acitvation="relu") #第3层
    A4,Z4=model.l_layer_forward_model(A3,W4,b4,acitvation="sigmoid") #第4层
    test_Y=A4
    # print(test_Y.shape)
    for i in range(test_Y.shape[1]):
        if test_Y[0][i]>0.5:
            prediction_Y[0][i]=1
        else:
            prediction_Y[0][i]=0

    return prediction_Y

def predict_y_with_load_params(x):
    cur_filepath=os.path.basename(os.path.realpath(__file__))
    cur_file,ext=os.path.splitext(cur_filepath)
    filename=cur_file+".h5"
    f=h5py.File(filename,'r')
    params={}
    for k in f.keys():
        params[k]=np.array(f[k][:])
    W1=params["W1"]
    b1=params["b1"]
    W2=params["W2"]
    b2=params["b2"]
    W3=params["W3"]
    b3=params["b3"]
    W4=params["W4"]
    b4=params["b4"]
    #测试用例样本数
    test_m=x.shape[1]
    prediction_Y=np.zeros((1,test_m))
    #计算
    A1,Z1=model.l_layer_forward_model(x,W1,b1,acitvation="relu") #第1层
    A2,Z2=model.l_layer_forward_model(A1,W2,b2,acitvation="relu") #第2层
    A3,Z3=model.l_layer_forward_model(A2,W3,b3,acitvation="relu") #第3层
    A4,Z4=model.l_layer_forward_model(A3,W4,b4,acitvation="sigmoid") #第4层
    test_Y=A4
    # print(test_Y.shape)
    for i in range(test_Y.shape[1]):
        if test_Y[0][i]>0.5:
            prediction_Y[0][i]=1
        else:
            prediction_Y[0][i]=0

    return prediction_Y

if __name__=="__main__":
    train_X, train_Y, test_x, test_y, list_classes=load_dataset()
    #归一化
    train_X=train_X/255
    test_x=test_x/255
    #参数初始化
    params=model.params_init_model(train_X.shape[0],4,[20,7,5,1],init_method="He")
    W1=params["W1"]
    b1=params["b1"]
    W2=params["W2"]
    b2=params["b2"]
    W3=params["W3"]
    b3=params["b3"]
    W4=params["W4"]
    b4=params["b4"]
    learning_rate=0.0075
    echo_num=1000
    for echo in range(echo_num):
        batches=model.mini_batch(train_X,train_Y)
        for batch in batches:
            train_x,train_y=batch
            #正向传播
            A1,Z1,D1=model.l_layer_forward_with_dropout_model(train_x,W1,b1,keep_prob=0.9,acitvation="relu",seed=0) #第1层
            A2,Z2,D2=model.l_layer_forward_with_dropout_model(A1,W2,b2,keep_prob=1,acitvation="relu",seed=1) #第2层
            A3,Z3,D3=model.l_layer_forward_with_dropout_model(A2,W3,b3,keep_prob=1,acitvation="relu",seed=2) #第3层
            A4,Z4,D4=model.l_layer_forward_with_dropout_model(A3,W4,b4,keep_prob=1,acitvation="sigmoid",seed=3) #第4层

            #计算代价
            J,dJ=model.cost_model(A4,train_y)
            #反向传播
            dA4_prew,dW4,db4=model.l_layer_backward_with_dropout_model(A3,D4,W4,Z4,dJ,keep_prob=1,acitvation="sigmoid")#第4层
            dA3_prew,dW3,db3=model.l_layer_backward_with_dropout_model(A2,D3,W3,Z3,dA4_prew,keep_prob=1,acitvation="relu")#第3层
            dA2_prew,dW2,db2=model.l_layer_backward_with_dropout_model(A1,D2,W2,Z2,dA3_prew,keep_prob=1,acitvation="relu")#第2层
            dA1_prew,dW1,db1=model.l_layer_backward_with_dropout_model(train_x,D1,W1,Z1,dA2_prew,keep_prob=0.9,acitvation="relu")#第1层
            #更新参数权值
            # print("w",W.shape)
            # print("dw",dW.shape)
            W1=W1-learning_rate*dW1
            b1=b1-learning_rate*db1

            W2=W2-learning_rate*dW2
            b2=b2-learning_rate*db2

            W3=W3-learning_rate*dW3
            b3=b3-learning_rate*db3

            W4=W4-learning_rate*dW4
            b4=b4-learning_rate*db4

            print("echo {0} cost:{1}".format(echo,J))

    params["W1"]=W1
    params["b1"]=b1
    params["W2"]=W2
    params["b2"]=b2
    params["W3"]=W3
    params["b3"]=b3
    params["W4"]=W4
    params["b4"]=b4
    save_params(params)
    # train_Y_hat=predict_y(train_x,params)
    train_Y_hat=predict_y_with_load_params(train_X)
    print("train_Y_hat:",train_Y_hat.shape)
    print("train_y:",train_Y.shape)
    print("train accuracy: {} %".format(100 - np.mean(np.abs(train_Y_hat-train_Y)) * 100))

    # test_Y_hat=predict_y(test_x,params)
    test_Y_hat=predict_y_with_load_params(test_x)
    print("prediction_Y:",test_Y_hat.shape)
    print("test_y:",test_y.shape)
    print("test accuracy: {} %".format(100 - np.mean(np.abs(test_Y_hat-test_y)) * 100))
    #
    from scipy import ndimage,misc
    from function import imagefunc
    image_path="/my_image.jpg"
    frame="images"+image_path
    my_image_x=np.array(ndimage.imread(frame,flatten=False))
    print(my_image_x.shape)
    my_image_x=misc.imresize(my_image_x,size=(64,64))
    plt.imshow(my_image_x)
    print(my_image_x.shape)
    my_image_x=my_image_x/255
    my_image_x=imagefunc.image2vector(my_image_x)
    print(my_image_x.shape)

    # my_image_y=predict_y(my_image_x,params)
    my_image_y=predict_y_with_load_params(my_image_x)
    print(my_image_y)
    # plt.plot(cost)
    # plt.xlabel('iter times')
    # plt.ylabel('cost')
    plt.show()


