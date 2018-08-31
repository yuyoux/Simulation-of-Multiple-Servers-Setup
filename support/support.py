import matplotlib.pyplot as plt
import numpy as np

s = np.random.uniform(0,1,1000)
count, bins, ignored = plt.hist(s, 15, normed=True)
# plt.plot(bins, np.ones_like(bins), linewidth=2, color='r')
# plt.show()
## reference: https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.random.uniform.html

#compute confidence interval
#group = [5.828507487520803,5.252321131447595,4.981790349417643,5.515306156405986,5.0593128119800355]
#group = [4.492497504159735,3.963129783693854,4.016835274542437,4.257374376039931,4.062978369384358]
#group = [3.3892179700499185,3.3723094841930252,3.418089850249592,3.4092312811980054,3.3980765391014884]
group = [3.2300931780366082,3.2820682196339575,3.3473494176372753,3.313151414309486,3.3852845257903392]
a = np.array(group)
n = 5
t = 2.776
meang = np.mean(a)
sdg = np.std(a)
pg = sdg/(np.sqrt(n))*t
print('mean: {}'.format(meang))
print('std: {}'.format(sdg))
print('lower:{}'.format(meang-pg))
print('upper:{}'.format(meang+pg))
print('confidence interval: [{}, {}]'.format((meang-pg),(meang+pg)))