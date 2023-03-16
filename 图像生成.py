import struct
import numpy as np
import matplotlib.pyplot as plt


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


def getImgData(file_path):
    x = file_path  # 依次读文件
    ar = np.fromfile(x, dtype=np.float32).astype(np.float64)[:zsize]
    ar = np.reshape(ar, [4096, 3100])

    # ar = avg_pooling_forward(np.expand_dims(ar, [0, 1]), (20, 20), (5, 5))[0, 0]  # stride
    # ar = ar[5::10,5::10]

    # factor = 100
    # ar = ar[(factor//2)::factor, (factor//2)::factor]

    L = ar.shape[0]
    W = ar.shape[1]
    # ar=np.reshape(ar,[W,L]) #list 转 ndarray

    # 定义三维数据
    xx = np.arange(0, W, 1)  # 他这个拼接的方向不是文件顺序的那个维度
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


def set_axes_equal(ax, X, Y, Z):
    max_range = np.array(
        [np.nanmax(X) - np.nanmin(X), np.nanmax(Y) - np.nanmin(Y), np.nanmax(Z) - np.nanmin(Z)]).max() / 2.0

    mid_x = (np.nanmax(X) + np.nanmin(X)) * 0.5
    mid_y = (np.nanmax(Y) + np.nanmin(Y)) * 0.5
    mid_z = (np.nanmax(Z) + np.nanmin(Z)) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)


def getImg(file_path, output_path):
    X, Y, ar = getImgData(file_path)
    # print('done')

    fig = plt.figure()  # 定义新的三维坐标轴
    ax3 = plt.axes(projection='3d')
    # ax3.set_box_aspect([1,1,1])
    set_axes_equal(ax3, X, Y, ar)

    # print(X.shape)
    # print(Y.shape)
    # print(ar.shape)

    # #作图
    ax3.set_facecolor('#000000')
    ax3.plot_surface(X, Y, ar, cstride=8, rstride=8, cmap='viridis',antialiased=False)  # 模糊一点
    plt.gca().view_init(20, -30)  # 默认是30和-60
    plt.gca().dist = 7  # 默认是10
    plt.axis('off')
    # plt.show()
    fig.savefig(output_path, dpi=800, bbox_inches='tight')


file_path1 = "./2330203432_23.bin"
# file_path2 = "./2310178711_269.bin"

output_path = '23101787211.png'  # 绝对或相对路径

zsize = 3100 * 4096  # z值采样的长和宽
getImg(file_path1, output_path)
