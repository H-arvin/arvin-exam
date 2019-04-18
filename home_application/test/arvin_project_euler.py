# -*- coding: utf-8 -*-
#	coding practice: https://projecteuler.net/archives
import math


#	Multiples of number
def Multiples_add(multiple, maxnum):
    max = maxnum - maxnum % multiple
    sum = (multiple + max) * max / (multiple * 2)
    return sum


#	Even Fibonacci numbers
def Fibonacci_even_add(maxnum, f1=1, f2=1):
    fibonacci_list = [f1, f2]
    while fibonacci_list[-1] <= maxnum:
        fibonacci_list.append(fibonacci_list[-1] + fibonacci_list[-2])
    index = 1
    sum = 0
    while index < (len(fibonacci_list) - 1):
        sum += fibonacci_list[index]
        index += 2
    return sum


#	Largest prime factor
def largest_prime_factor(num):
    factor = []
    sqrt = int(math.sqrt(num))
    multiple = sqrt / 6 + 1
    include_factor = [2, 3]
    for i in range(1, multiple + 1):
        include_factor.append(6 * i - 1)
        include_factor.append(6 * i + 1)

    def has_factor(arg):
        for i in include_factor:
            if arg % i == 0:
                shang = arg / i
                return {"result": True, 'factor': i, 'shang': shang}
        return {'result': False, 'factor': arg}

    res = has_factor(num)
    while res['result']:
        factor.append(res['factor'])
        if res['shang'] == 1:
            break
        res = has_factor(int(res['shang']))
    if not res['result']:
        factor.append(res['factor'])
    return max(factor)


#	Largest palindrome product
def palindrome_bit(bit):
    maxnum = (10 ** bit - 1) ** 2
    number = str(maxnum)

    def factor_bit(bit, palindrome):
        divisor = 10 ** bit - 1
        dict = {'result': False, 'divisor': ''}
        while not dict['result']:
            if palindrome % divisor == 0:
                dict['result'] = True
                dict['divisor'] = divisor
                break
            else:
                divisor -= 1
                if (palindrome / float(divisor) > (10 ** bit - 1)):
                    break
        return dict

    if len(number) % 2 == 0:
        num1 = number[:bit]
        num2 = number[-bit:]
        if num2 > num1[::-1]:
            palindrome = int(num1 + num1[::-1])
            result = factor_bit(bit, palindrome)
            while not result['result']:
                num1 = str(int(num1) - 1)
                palindrome = int(num1 + num1[::-1])
                result = factor_bit(bit, palindrome)
        else:
            num1 = str(int(num1) - 1)
            palindrome = int(num1 + num1[::-1])
            result = factor_bit(bit, palindrome)
            while not result['result']:
                num1 = str(int(num1) - 1)
                palindrome = int(num1 + num1[::-1])
                result = factor_bit(bit, palindrome)

    else:
        num1 = number[0:bit]
        num2 = number[-bit:]
        middle = number[0:bit + 1]
        if num2 > num1[::-1]:
            palindrome = int(middle + middle[:-1][::-1])
            result = factor_bit(bit, palindrome)
            while not result['result']:
                middle = str(int(middle) - 1)
                palindrome = int(middle + middle[:-1][::-1])
                result = factor_bit(bit, palindrome)
        else:
            middle = str(int(middle) - 1)
            palindrome = int(middle + middle[:-1][::-1])
            while not result['result']:
                middle = str(int(middle) - 1)
                palindrome = int(middle + middle[:-1][::-1])
                result = factor_bit(bit, palindrome)

    return {"palindrome": palindrome, "factor": result['divisor']}


#	Smallest multiple
def Smallest_multiple(arg):
    x = arg / 6 + 1
    factor = []
    factor_include = [2, 3]
    for i in range(1, x):
        factor_include.append(6 * i - 1)
        factor_include.append(6 * i + 1)

    def is_pimme(num):
        for i in range(2, int(math.sqrt(num))):
            if num % i == 0:
                return False
        return True

    for i in factor_include:
        if is_pimme(i):
            factor.append(i)
    multiple = 1
    for i in factor:
        coun = int(math.log(arg, i))
        multiple = multiple * i ** coun
    return multiple


#	Sum square difference
def Sum_square(n):
    square_sum = n * (n + 1) * (2 * n + 1) / 6
    sum_square = ((1 + n) * n / 2) ** 2
    return sum_square - square_sum


#	10001st prime
def prime_ofn(n):
    prime = [2, 3]
    if n <= 2:
        return prime[n - 1]

    def is_pimme(num):
        for i in range(2, int(math.sqrt(num))):
            if num % i == 0:
                return False
        return True

    num_difference = n - 2
    i = 1
    while num_difference > 0:
        if is_pimme(6 * i - 1):
            prime.append(6 * i - 1)
            num_difference -= 1
        if is_pimme(6 * i + 1):
            prime.append(6 * i + 1)
            num_difference -= 1
        i += 1
    if num_difference == 0:
        return prime[-1]
    else:
        return prime[-2]


# Largest product in a series
def Largest_product(arg, s):
    a = s.split('0')
    b = s.split('0')
    max_product = 0
    for i in b:
        if len(i) < arg:
            a.remove(i)
        else:
            product = 1
            for j in range(arg):
                product = product * int(i[j])
            if product > max_product:
                max_product = product
    little = max_product / (9 ** (arg - 1)) + 1
    for i in a:
        length = len(i)
        for j in range(length - arg + 1):
            if int(i[j]) >= little:
                product = 1
                for k in range(arg):
                    product = product * int(i[j + k])
                if product > max_product:
                    max_product = product
    return max_product


#	Special Pythagorean triplet
def Pythagorean_triplet(num):
    min_c = math.sqrt(2) * num - num
    max_c = num / 2
    for c in range(int(min_c) + 1, max_c):
        a_add_b = num - c
        ab = num * (num - 2 * c) / 2.0
        a = math.sqrt(a_add_b ** 2 / 4.0 - ab) + a_add_b / 2.0
        if a == int(a):
            b = num - a - c
            if a ** 2 + b ** 2 == c ** 2:
                if a != b:
                    return {'result': True, 'a': int(a), 'b': int(b), 'c': c}
    return {'result': False, 'message': 'not exist'}


#	Summation of primes
def Summation_primes(max_num):
    n = max_num / 6
    primes = []
    include_primes = [2, 3]
    i = 1
    while i <= n:
        include_primes.append(6 * i - 1)
        include_primes.append(6 * i + 1)
        i += 1

    def is_pimme(num, primeslist):
        sqrt = math.sqrt(num)
        for i in primeslist:
            if i <= sqrt:
                if num % i == 0:
                    return False
            else:
                return True

    for prime in include_primes:
        if is_pimme(prime, include_primes):
            primes.append(prime)
    if primes[-1] > max_num:
        primes.pop()
    return sum(primes)


#	Largest product in a grid
def Largest_product_grid(arg, grid_file):
    arry = []
    try:
        for line in open(grid_file):
            arry.append(line.strip('\n').split(' '))
    except Exception, e:
        print e
    grid = len(arry[0])
    max_product = {'row': 0, 'column': 0, 'diagonal_right': 0, 'diagonal_left': 0}
    # diagonal of right
    for i in range(grid - arg + 1):
        for j in range(grid - arg + 1):
            product_four = int(arry[i][j]) * int(arry[i + 1][j + 1]) * int(arry[i + 2][j + 2]) * int(arry[i + 3][j + 3])
            if product_four > max_product['diagonal_right']:
                max_product['diagonal_right'] = product_four
    # diagonal of left
    for i in range(arg - 1, grid):
        for j in range(grid - arg + 1):
            product_four = int(arry[i][j]) * int(arry[i - 1][j + 1]) * int(arry[i - 2][j + 2]) * int(arry[i - 3][j + 3])
            if product_four > max_product['diagonal_left']:
                max_product['diagonal_left'] = product_four
    # row
    for i in range(grid):
        for j in range(grid - arg + 1):
            product_four = int(arry[i][j]) * int(arry[i][j + 1]) * int(arry[i][j + 2]) * int(arry[i][j + 3])
            if product_four > max_product['row']:
                max_product['row'] = product_four
    # column
    for i in range(grid - arg + 1):
        for j in range(grid):
            product_four = int(arry[i][j]) * int(arry[i + 1][j]) * int(arry[i + 2][j]) * int(arry[i + 3][j])
            if product_four > max_product['column']:
                max_product['column'] = product_four
    return max_product


# Highly divisible triangular number
def triangle_number(num):
    if num % 2 == 0:
        return (num + 1) * num / 2
    else:
        return (num + 1) / 2 * num


def divisors_count(num):
    i = 2
    count = 0
    while i * i < num:
        if num % i == 0:
            count += 2
            i += 1
        else:
            i += 1
    if i * i == num:
        count += 1
    return count + 2


def first_divisors_over(n):
    num = 1
    while True:
        triangle_num = triangle_number(num)
        divisors = divisors_count(triangle_num)
        if divisors > n:
            return triangle_num
        else:
            num += 1


# Largesum 13
digits = """37107287533902102798797998220837590246510135740250
46376937677490009712648124896970078050417018260538
74324986199524741059474233309513058123726617309629
91942213363574161572522430563301811072406154908250
23067588207539346171171980310421047513778063246676
89261670696623633820136378418383684178734361726757
28112879812849979408065481931592621691275889832738
44274228917432520321923589422876796487670272189318
47451445736001306439091167216856844588711603153276
70386486105843025439939619828917593665686757934951
62176457141856560629502157223196586755079324193331
64906352462741904929101432445813822663347944758178
92575867718337217661963751590579239728245598838407
58203565325359399008402633568948830189458628227828
80181199384826282014278194139940567587151170094390
35398664372827112653829987240784473053190104293586
86515506006295864861532075273371959191420517255829
71693888707715466499115593487603532921714970056938
54370070576826684624621495650076471787294438377604
53282654108756828443191190634694037855217779295145
36123272525000296071075082563815656710885258350721
45876576172410976447339110607218265236877223636045
17423706905851860660448207621209813287860733969412
81142660418086830619328460811191061556940512689692
51934325451728388641918047049293215058642563049483
62467221648435076201727918039944693004732956340691
15732444386908125794514089057706229429197107928209
55037687525678773091862540744969844508330393682126
18336384825330154686196124348767681297534375946515
80386287592878490201521685554828717201219257766954
78182833757993103614740356856449095527097864797581
16726320100436897842553539920931837441497806860984
48403098129077791799088218795327364475675590848030
87086987551392711854517078544161852424320693150332
59959406895756536782107074926966537676326235447210
69793950679652694742597709739166693763042633987085
41052684708299085211399427365734116182760315001271
65378607361501080857009149939512557028198746004375
35829035317434717326932123578154982629742552737307
94953759765105305946966067683156574377167401875275
88902802571733229619176668713819931811048770190271
25267680276078003013678680992525463401061632866526
36270218540497705585629946580636237993140746255962
24074486908231174977792365466257246923322810917141
91430288197103288597806669760892938638285025333403
34413065578016127815921815005561868836468420090470
23053081172816430487623791969842487255036638784583
11487696932154902810424020138335124462181441773470
63783299490636259666498587618221225225512486764533
67720186971698544312419572409913959008952310058822
95548255300263520781532296796249481641953868218774
76085327132285723110424803456124867697064507995236
37774242535411291684276865538926205024910326572967
23701913275725675285653248258265463092207058596522
29798860272258331913126375147341994889534765745501
18495701454879288984856827726077713721403798879715
38298203783031473527721580348144513491373226651381
34829543829199918180278916522431027392251122869539
40957953066405232632538044100059654939159879593635
29746152185502371307642255121183693803580388584903
41698116222072977186158236678424689157993532961922
62467957194401269043877107275048102390895523597457
23189706772547915061505504953922979530901129967519
86188088225875314529584099251203829009407770775672
11306739708304724483816533873502340845647058077308
82959174767140363198008187129011875491310547126581
97623331044818386269515456334926366572897563400500
42846280183517070527831839425882145521227251250327
55121603546981200581762165212827652751691296897789
32238195734329339946437501907836945765883352399886
75506164965184775180738168837861091527357929701337
62177842752192623401942399639168044983993173312731
32924185707147349566916674687634660915035914677504
99518671430235219628894890102423325116913619626622
73267460800591547471830798392868535206946944540724
76841822524674417161514036427982273348055556214818
97142617910342598647204516893989422179826088076852
87783646182799346313767754307809363333018982642090
10848802521674670883215120185883543223812876952786
71329612474782464538636993009049310363619763878039
62184073572399794223406235393808339651327408011116
66627891981488087797941876876144230030984490851411
60661826293682836764744779239180335110989069790714
85786944089552990653640447425576083659976645795096
66024396409905389607120198219976047599490197230297
64913982680032973156037120041377903785566085089252
16730939319872750275468906903707539413042652315011
94809377245048795150954100921645863754710598436791
78639167021187492431995700641917969777599028300699
15368713711936614952811305876380278410754449733078
40789923115535562561142322423255033685442488917353
44889911501440648020369068063960672322193204149535
41503128880339536053299340368006977710650566631954
81234880673210146739058568557934581403627822703280
82616570773948327592232845941706525094512325230608
22918802058777319719839450180888072429661980811197
77158542502016545090413245809786882778948721859617
72107838435069186155435662884062257473692284509516
20849603980134001723930671666823555245252804609722
53503534226472524250874054075591789781264330331690"""


# def large_sum(digits):
#     digits_str = digits.replace('\n', '')
#     sum = 0
#     for i in range(10):
#         before_len = len(digits_str)
#         digits_str = digits_str.replace(str(i), '')
#         now_len = len(digits_str)
#         sum += (before_len - now_len) * i
#     return sum
def large_sum(digits):
    digits_list = digits.split('\n')
    sum = 0
    for i in digits_list:
        sum += int(i[:15])
    sum_list = list(str(sum)[:10])
    sum = 0
    for i in sum_list:
        sum += int(i)
    return sum


# Longest Collatz sequence 14
def collatz_sequence(scope):
    if scope < 2:
        return '输入大于1的数'
    a = [[0, 0], [1, 1]]
    i = 2
    most = 1
    while i <= scope:
        count = 1
        next_coll = i
        while next_coll != 1:
            next_coll = next_collatz(next_coll)
            if next_coll < i:
                count = a[next_coll][1] + count
                a.append([i, count])
                if most < count:
                    most = count
                break
            count += 1
        i += 1
    return most


def next_collatz(num):
    if num % 2 == 0:
        num = num / 2
    else:
        num = 3 * num + 1
    return num


# lattice paths 15
import copy


def lattice_paths(num):
    grid = num + 1
    grids = []
    grids.append([1] * grid)
    line = [1] + [0] * (grid - 1)
    for i in range(grid - 1):
        grids.append(copy.deepcopy(line))
    grids[0][0] = 0
    for i in range(1, grid):
        for j in range(1, grid):
            grids[i][j] = grids[i - 1][j] + grids[i][j - 1]
    print grids
    return grids[grid - 1][grid - 1]


# power digit sum 16
def digit_sum(num):
    return sum(int(i) for i in str(2 ** num))


# Number letter cpounts 17
def number_letter_counts():
    return 'borring'


# Maximum path sum 18
triangle = """75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23"""
def maximum_path_sum(triangle):
    triangle_list = triangle.split('\n')
    triangle_grid = []
    for i in triangle_list:
        triangle_grid.append(i.split(" "))
    for i in range(len(triangle_grid)):
        for j in range(len(triangle_grid[i])):
            triangle_grid[i][j] = int(triangle_grid[i][j])
    length = len(triangle_list)
    for i in range(1, length):
        for j in range(length - i):
            left = triangle_grid[-i - 1][j] + triangle_grid[-i][j]
            right = triangle_grid[-i - 1][j] + triangle_grid[-i][j + 1]
            if left > right:
                triangle_grid[-i - 1][j] = left
            else:
                triangle_grid[-i - 1][j] = right
    return triangle_grid[0][0]

if __name__ == '__main__':
    print maximum_path_sum(triangle)
