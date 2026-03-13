# class Solution:
#     def mergeAlternately(self, word1: str, word2: str) -> str:
#         maxi = max(len(word1),len(word2))
#         mini = min(len(word1),len(word2))
#         anu = maxi - mini
#         output = ''
#         if len(word1) > len(word2):
#             temp = word1[-anu:]
#         elif len(word2) > len(word1):
#             temp = word2[-anu:]
#         else:
#             temp=''
#         for i in range(mini):
#             tambah = word1[i] + word2[i]
#             output += tambah
#         hasil = output + temp
#         return hasil
            

# sol = Solution.mergeAlternately(self=Solution,word1='abcde',word2='qwrty')
# print(sol)

# class Solution:
#     def findTheDifference(self, s: str, t: str) -> str:
#         diff = max(len(s),len(t)) - min(len(s),len(t))
#         if len(s) > len(t):
#             temp = s[-diff:]
#         elif len(s) < len(t):
#             temp = t[-diff:]
#         else:
#             temp = ''
#         hasil = ''
#         for i in range(min(len(s),len(t))):
#             if s[i] != t[i]:
#                 hasil += s[i] + t[i]
#         return hasil + temp

# s = "ymbgaraibkfmvocpizdydugvalagaivdbfsfbepeyccqfepzvtpyxtbadkhmwmoswrcxnargtlswqemafandgkmydtimuzvjwxvlfwlhvkrgcsithaqlcvrihrwqkpjdhgfgreqoxzfvhjzojhghfwbvpfzectwwhexthbsndovxejsntmjihchaotbgcysfdaojkjldprwyrnischrgmtvjcorypvopfmegizfkvudubnejzfqffvgdoxohuinkyygbdzmshvyqyhsozwvlhevfepdvafgkqpkmcsikfyxczcovrmwqxxbnhfzcjjcpgzjjfateajnnvlbwhyppdleahgaypxidkpwmfqwqyofwdqgxhjaxvyrzupfwesmxbjszolgwqvfiozofncbohduqgiswuiyddmwlwubetyaummenkdfptjczxemryuotrrymrfdxtrebpbjtpnuhsbnovhectpjhfhahbqrfbyxggobsweefcwxpqsspyssrmdhuelkkvyjxswjwofngpwfxvknkjviiavorwyfzlnktmfwxkvwkrwdcxjfzikdyswsuxegmhtnxjraqrdchaauazfhtklxsksbhwgjphgbasfnlwqwukprgvihntsyymdrfovaszjywuqygpvjtvlsvvqbvzsmgweiayhlubnbsitvfxawhfmfiatxvqrcwjshvovxknnxnyyfexqycrlyksderlqarqhkxyaqwlwoqcribumrqjtelhwdvaiysgjlvksrfvjlcaiwrirtkkxbwgicyhvakxgdjwnwmubkiazdjkfmotglclqndqjxethoutvjchjbkoasnnfbgrnycucfpeovruguzumgmgddqwjgdvaujhyqsqtoexmnfuluaqbxoofvotvfoiexbnprrxptchmlctzgqtkivsilwgwgvpidpvasurraqfkcmxhdapjrlrnkbklwkrvoaziznlpor"
# t = "qhxepbshlrhoecdaodgpousbzfcqjxulatciapuftffahhlmxbufgjuxstfjvljybfxnenlacmjqoymvamphpxnolwijwcecgwbcjhgdybfffwoygikvoecdggplfohemfypxfsvdrseyhmvkoovxhdvoavsqqbrsqrkqhbtmgwaurgisloqjixfwfvwtszcxwktkwesaxsmhsvlitegrlzkvfqoiiwxbzskzoewbkxtphapavbyvhzvgrrfriddnsrftfowhdanvhjvurhljmpxvpddxmzfgwwpkjrfgqptrmumoemhfpojnxzwlrxkcafvbhlwrapubhveattfifsmiounhqusvhywnxhwrgamgnesxmzliyzisqrwvkiyderyotxhwspqrrkeczjysfujvovsfcfouykcqyjoobfdgnlswfzjmyucaxuaslzwfnetekymrwbvponiaojdqnbmboldvvitamntwnyaeppjaohwkrisrlrgwcjqqgxeqerjrbapfzurcwxhcwzugcgnirkkrxdthtbmdqgvqxilllrsbwjhwqszrjtzyetwubdrlyakzxcveufvhqugyawvkivwonvmrgnchkzdysngqdibhkyboyftxcvvjoggecjsajbuqkjjxfvynrjsnvtfvgpgveycxidhhfauvjovmnbqgoxsafknluyimkczykwdgvqwlvvgdmufxdypwnajkncoynqticfetcdafvtqszuwfmrdggifokwmkgzuxnhncmnsstffqpqbplypapctctfhqpihavligbrutxmmygiyaklqtakdidvnvrjfteazeqmbgklrgrorudayokxptswwkcircwuhcavhdparjfkjypkyxhbgwxbkvpvrtzjaetahmxevmkhdfyidhrdeejapfbafwmdqjqszwnwzgclitdhlnkaiyldwkwwzvhyorgbysyjbxsspnjdewjxbhpsvj"
# sol = Solution.findTheDifference(Solution,s,t)
# print(sol)
# evenNumber = [i for i in range(0,501) if i % 2 == 0]
# print(evenNumber)

# var_array = [i for i in range(101)]

# TODO: Silakan buat kode Anda di bawah ini.
# hasil = sum(var_array) / len(var_array)
# print(hasil)
  
# var_mat = [[5, 0],
#           [1, -2],
#           [10,7],
#           [0,-0]]
# def_mat = [[0 for j in range(len(var_mat[0]))]for i in range(len(var_mat))]
# for i in range(len(var_mat)):
#     for j in range(len(var_mat[0])):
#         def_mat[i][j] = var_mat[i][j]*2

# print(def_mat)


# class Calculator:
#     def __init__(self,n1,n2):
#         self.n1 = n1
#         self.n2 = n2
#         self.run_calculator()
    
#     def run_calculator(self):
#         while True:
#             print('Welcome To Calculator Menu')
#             print('1. Tambah')
#             print('2. Kurang')
#             print('3. Kali')
#             print('4. Bagi')
#             print('5. Selesai')
#             opsi = input('Select Menu: ')
#             if opsi.isdigit():
#                 opsi = int(opsi)
#                 if opsi > 0 and opsi < 6:
#                     match opsi:
#                         case 1:
#                             self.run_tambah()
#                         case 2:
#                             self.run_kurang()
#                         case 3:
#                             self.run_kali()
#                         case 4:  
#                             self.run_bagi()      
#                         case 5:
#                             break
#                 else:
#                     print('Pilih angka 1-5')
#             else:
#                 print('Input Harus berupa angka')
    
#     def run_tambah(self):
#         print(self.n1 + self.n2)
    
#     def run_kurang(self):
#         print(self.n1 - self.n2)
    
#     def run_kali(self):
#         print(self.n1 * self.n2)
    
#     def run_bagi(self):
#         try:
#             print(self.n1 / self.n2)
#         except:
#             print('Tidak bisa dibagi 0')

# if __name__ == '__main__':
#     calc = Calculator(10,0)
#     calc

x = {'name':'dicoding','age':18}
x['name'] =  'code'
print(x)
