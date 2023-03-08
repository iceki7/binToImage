import struct
from mayavi import mlab
import numpy as np
import matplotlib.pyplot as plt

fileCount = "27"
filename = "./2310178711_269.bin"
f = open(filename, "rb")

nx = 3100
nz = 4096
pz = np.zeros(nx * nz)
px = np.zeros(nx * nz)
py = np.zeros(nx * nz)
for i in range(nx * nz):
    data = f.read(4)
    elem = struct.unpack("f", data)[0]
    pz[i] = elem
f.close()
pz[np.isnan(pz)] = 0

for i in range(nx):
    px[i * nz:(i + 1) * nz] = np.linspace(30, 1721, 3980)

for i in range(nz):
    py[i * nz:(i + 1) * nz] = 30 + i * 0.2

fig = mlab.figure(bgcolor=(0, 0, 0), size=(1024, 995))  # 指定图片背景和尺寸
mlab.points3d(px, py, pz, pz, mode="point", colormap='jet')
mlab.show()

# px = px.reshape(nx, nz)
# py = py.reshape(nx, nz)
# pz = pz.reshape(nx, nz)

# print(pz[2000:2300, 1600:1630])
# print("\n")
# print("############")
# print(px[2000:2300, 1600:1630])
# print("\n")
# print("############")
# print(py[2000:2300, 1600:1630])
# print("\n")
# print("############")

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(px, py, pz, c=pz, cmap='rainbow', marker="x")
# ax.axis()
# plt.show()
