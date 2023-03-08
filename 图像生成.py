import struct
#from mayavi import mlab
import numpy as np
import matplotlib.pyplot as plt

fileCount = "27"
filename =["./2310178711_269",
           "./2310178711_270",
           "./2310178711_271",
           
            "./2310178721_248",
            "./2310178721_249",
            "./2310178721_250",
           ]

# m=np.array([7,9,3,np.nan,2,6,np.nan,1])
# print(m[m==m])
# exit()

zsize=3100*4096

zr=[]
L=0
W=0
def getConZ():
    global L,W
    ar=[]
    for x in filename:#依次读文件
        f = open(x+".bin", "rb")
        for i in range(zsize):
            data = f.read(4)    #一个z值
            elem = struct.unpack("f", data)[0]#bin转数字
            #if(elem!=elem): #去掉nan
            #    pass
            #else:
            ar.append(elem)
        f.close()
        print('size')
        print(len(ar))#每加一张图片的像素个数
    L=4096
    W=int(len(ar)/L)
    ar=np.reshape(ar,[W,L]) #list 转 ndarray
    
    ar=ar[ar==ar] #去nan,之后要重新划分图像
    print('size without nan')
    print(ar.shape)
    L=4900
    W=int(ar.shape[0]/L)
    ar=ar[0:L*W]#重新划分为一个矩形，多余的像素舍弃掉。
    ar=np.reshape(ar,[W,L])
    
    return ar
    #还是不行，没解决前面的问题
    #nan是在把所有bin拼起来以后才去掉的
                


    


ar=getConZ()
print('done')
   
   
fig = plt.figure() #定义新的三维坐标轴

ax3 = plt.axes(projection='3d')

#定义三维数据
xx = np.arange(0,L,1)
yy = np.arange(0,W,1)

X,Y = np.meshgrid(xx,yy)
# print(type(X))
print(X.shape)
print(Y.shape)
print(ar.shape)

# #作图
ax3.plot_surface(X,Y,ar,cmap='rainbow')
# #ax3.contour(X,Y,Z，zdim='z',offset=-2，cmap='rainbow) #等高线图，要设置offset，为Z的最小值
# #plt.axis('off')
plt.show()
# fig.savefig(filename+'.png')


