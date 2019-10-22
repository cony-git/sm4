from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from PIL import Image,ImageDraw

#初始化CryptSM4
key = b'1901210540aaa123' #秘钥
iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' #  bytes类型
crypt_sm4 = CryptSM4()


#读取图片RGB信息到array列表
im = Image.open("pkulogo.jpg")
w,h=im.size
print(w,h)
im = im.convert('RGB')
array = []
for x in range(w):
    for y in range(h):
        r, g, b = im.getpixel((x,y))
        rgb = (r, g, b)
        array.append(rgb)
# print(array)

#将rgb信息转为byte类型以便加密
rgb_int_list=[]
for tup in array:
    for i in range(0,3):
        # print(tup[i])
        rgb_int_list.append(tup[i])
rgb_bytes=bytes(rgb_int_list)

# print(rgb_bytes)

#ecb模式用key加密,加密后值一定在0-255之间
crypt_sm4.set_key(key, SM4_ENCRYPT)
encrypt_value_ecb = crypt_sm4.crypt_ecb(rgb_bytes) #  bytes类型
# print(encrypt_value)

#cbc模式加密
crypt_sm4.set_key(key, SM4_ENCRYPT)
encrypt_value_cbc = crypt_sm4.crypt_cbc(iv , rgb_bytes)

#处理rgb集合使得结果可以被3整除
rgb_crypto_ecb=[]
rgb_crypto_cbc=[]
for b in encrypt_value_ecb:
    rgb_crypto_ecb.append(b)
for b in encrypt_value_cbc:
    rgb_crypto_cbc.append(b)

n1=len(rgb_crypto_ecb)
if n1%3==0:
    pass
elif n1%3==1:
    rgb_crypto_ecb.append(255)
    rgb_crypto_ecb.append(255)
elif n1%3==2:
    rgb_crypto_ecb.append(255)

n2=len(rgb_crypto_cbc)
if n2%3==0:
    pass
elif n2%3==1:
    rgb_crypto_cbc.append(255)
    rgb_crypto_cbc.append(255)
elif n2%3==2:
    rgb_crypto_cbc.append(255)

#3个分一组RGB
tu_list_ecb=[]
for i in range(0,len(rgb_crypto_ecb),3):
    tu_list_ecb.append((rgb_crypto_ecb[i],rgb_crypto_ecb[i+1],rgb_crypto_ecb[i+2]))

tu_list_cbc=[]
for i in range(0,len(rgb_crypto_cbc),3):
    tu_list_cbc.append((rgb_crypto_cbc[i],rgb_crypto_cbc[i+1],rgb_crypto_cbc[i+2]))


#创建图片对象
image_ecb = Image.new('RGB', (w, h), (255, 255, 255))
image_cbc = Image.new('RGB', (w, h), (255, 255, 255))
# 创建Draw对象:
draw_ecb = ImageDraw.Draw(image_ecb)
draw_cbc = ImageDraw.Draw(image_cbc)

i=0
# 填充每个像素:
for x in range(w):
    for y in range(h):
        draw_ecb.point((x, y), fill=tu_list_ecb[i])
        i=i+1
image_ecb.save('new_ecb.jpg', 'jpeg')

i=0
# 填充每个像素:
for x in range(w):
    for y in range(h):
        draw_cbc.point((x, y), fill=tu_list_cbc[i])
        i=i+1
image_cbc.save('new_cbc.jpg', 'jpeg')



