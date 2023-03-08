import struct
# from mayavi import mlab
import numpy as np
import matplotlib.pyplot as plt

fileCount = "27"
filename = ["./2310178721_248",
            "./2310178721_249",
            "./2310178721_250",
            ]  # 下划线前面的数一致的才是同一块钢板数据

# m=np.array([7,9,3,np.nan,2,6,np.nan,1])
# print(m[m==m])
# exit()

zsize = 3100 * 4096

zr = []
L = 0
W = 0

def avg_pooling_forward(z, pooling, strides=(2, 2), padding=(0, 0)):
    """
    平均池化前向过程
    :param z: 卷积层矩阵,形状(N,C,H,W)，N为batch_size，C为通道数
    :param pooling: 池化大小(k1,k2)
    :param strides: 步长
    :param padding: 0填充
    :return:
    """
    N, C, H, W = z.shape
    # 零填充
    padding_z = np.lib.pad(z, ((0, 0), (0, 0), (padding[0], padding[0]), (padding[1], padding[1])), 'constant',
                           constant_values=0)

    # 输出的高度和宽度
    out_h = (H + 2 * padding[0] - pooling[0]) // strides[0] + 1
    out_w = (W + 2 * padding[1] - pooling[1]) // strides[1] + 1

    pool_z = np.zeros((N, C, out_h, out_w))

    for n in np.arange(N):
        for c in np.arange(C):
            for i in np.arange(out_h):
                for j in np.arange(out_w):
                    pool_z[n, c, i, j] = np.mean(padding_z[n, c,
                                                           strides[0] * i:strides[0] * i + pooling[0],
                                                           strides[1] * j:strides[1] * j + pooling[1]])
    return pool_z

def getConZ():
    global L, W
    ar_list = []   # 他这个拼接的方向不是文件顺序的那个维度
    ar_last = None
    for x in filename:  # 依次读文件
        ar = []
        f = open(x + ".bin", "rb")
        for i in range(zsize):
            data = f.read(4)  # 一个z值
            elem = struct.unpack("f", data)[0]  # bin转数字
            # if(elem!=elem): #去掉nan
            #    pass
            # else:
            ar.append(elem)
        f.close()
        print('size')
        print(len(ar))  # 每加一张图片的像素个数
        ar = np.reshape(ar, [4096, 3100])

        # 好像每张图片的高度0点不一样 强行让上一张最后一行数据对其下一张第一行数据
        if ar_last is not None:
            ar_first = ar[1, :]
            bias = ar_first - ar_last
            bias = np.average(bias[~np.isnan(bias)])
            ar -= bias
        ar_last = ar[-1, :]
        ar_list.append(ar)

    ar = np.concatenate(ar_list, 0)

    ar = avg_pooling_forward(np.expand_dims(ar, [0, 1]), (30,30),(5,5))[0,0]

    # factor = 100
    # ar = ar[(factor//2)::factor, (factor//2)::factor]

    L = ar.shape[0]
    W = ar.shape[1]
    # ar=np.reshape(ar,[W,L]) #list 转 ndarray

    # 定义三维数据
    xx = np.arange(0, W, 1)   # 他这个拼接的方向不是文件顺序的那个维度
    yy = np.arange(0, L, 1)
    X, Y = np.meshgrid(xx, yy)

    # ar[np.isnan(ar)] = 0
    ar = np.reshape(ar, [L, W])

    # 裁掉离谱数据
    ar_mean = np.nanmean(ar)
    ar[ar > ar_mean + 15] = np.nan
    ar[ar < ar_mean - 15] = np.nan

    # mask = ~np.isnan(ar)
    # X, Y, ar = X.flatten()[mask], Y.flatten()[mask], np.array(ar)[mask]

    return X, Y, ar

    # ar=ar[ar==ar] #去nan,之后要重新划分图像
    # print('size without nan')
    # print(ar.shape)
    # L=4900
    # W=int(ar.shape[0]/L)
    # ar=ar[0:L*W]#重新划分为一个矩形，多余的像素舍弃掉。
    # ar=np.reshape(ar,[W,L])
    #
    # return ar
    # 还是不行，没解决前面的问题
    # nan是在把所有bin拼起来以后才去掉的


X, Y, ar = getConZ()
print('done')

# plt.hist(ar, bins=32)
fig = plt.figure()  # 定义新的三维坐标轴

ax3 = plt.axes(projection='3d')

# 定义三维数据
# xx = np.arange(0,L,1)
# yy = np.arange(0,W,1)
#
# X,Y = np.meshgrid(xx,yy)
# print(type(X))
print(X.shape)
print(Y.shape)
print(ar.shape)

# #作图
#plt.rcParams['axes.facecolor']='#000000'
ax3.set_facecolor('#000000')
ax3.plot_surface(X, Y, ar, cmap='viridis')  # 模糊一点
# #ax3.contour(X,Y,Z，zdim='z',offset=-2，cmap='rainbow) #等高线图，要设置offset，为Z的最小值
plt.gca().view_init(30, -10)    #默认是30和-60
plt.gca().dist=7 #默认是10
plt.axis('off')
plt.show()
fig.savefig('2310178721.png',dpi=800,bbox_inches='tight')
