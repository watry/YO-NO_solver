import os
import time
testcase = {
    't' : '''
oxox
oxox
xxxo
oxoo
''',
    'h' : '''aa
aa
c
a''',
    'v' : '''a
d
a
b''',
}

q1 = {
    'h':'''a
n
nn
na
ae
nyn
nyn
ea
an
nn
n
a''',
    'v':'''n
ma
w
n
yn
xn
nx
ny
n
w
am
n'''
}

q2 = {
    'h':'''a
n
nn
an
ea
nyn
nyn
ae
na
nn
n
a''',
    'v':'''n
am
w
n
ny
nx
xn
yn
n
w
ma
n'''
}

class State:
    def __init__(self, parent = None, new_line = [], d = {}, rd = {}):
        if parent:
            assert(new_line)
            self.parent = parent
            self.size = parent.size
            self.exp_h = parent.exp_h
            self.exp_v = parent.exp_v
            self.dots = parent.dots.copy()
            self.numl = parent.numl + 1
            self.d = parent.d.copy()
            self.d.update(d)
            self.rd = parent.rd.copy()
            self.rd.update(rd)


            c1 = 0
            c2 = 0
            for item in new_line:
                c1 += 1
                c2 += item
                self.dots += [c1%2==0] * item
            self.dots += [False] * (self.size - c2)


        else:
            self.parent = parent
            self.size = 0
            self.exp_h = ''
            self.exp_v = ''
            self.dots = []
            self.numl = 0
            self.d = d.copy()
            self.rd = rd.copy()

    def setup(self, size, h, v):
        self.size = size
        self.exp_h = h.split()
        self.exp_v = v.split()

    def next_line_exp(self):
        return self.exp_h[self.numl]

    def is_complete(self):
        return self.size == self.numl

    def valid(self):
        for n1 in range(self.size):
            p = 0
            c = 0
            mark = False
            for n2 in range(self.numl):
                last = mark
                mark = self.dots[n2 * self.size + n1]
                if not last and mark:
                    p += 1
                    c = 1
                    if p > len(self.exp_v[n1]):
                        return False
                elif last and mark:
                    c += 1
                elif last and not mark:
                    if not self.mark(self.exp_v[n1][p-1], c):
                        return False
                    c = 0
            else:
                if self.numl == self.size:
                    if p != len(self.exp_v[n1]):
                        return False
                    elif mark:
                        if not self.mark(self.exp_v[n1][p-1], c):
                            return False
        return True



    def mark(self, sym, n):
        if self.d.get(n, sym) != sym or self.rd.get(sym, n) != n:
            return False
        self.d[n] = sym
        self.rd[sym] = n
        return True


    def next(self):
        result = []
        if self.is_complete():
            return result
        t = self.next_line_exp()
        stack = [(t, 0, [], self.d, self.rd)]
        while stack:
            exp,count,seq,tdic,trdic = stack.pop(0)
            #input()
            if not exp:
                t = State(self,seq,tdic,trdic)
                if not t.valid():
                    continue
                result.append(t)
                continue
            for t1 in range(1, self.size - count + 1):
                # t1 = length of blanks(ahead of c) + marks(of c)
                for t2 in range(t1):
                    dic = tdic.copy()
                    rdic = trdic.copy()
                    # t2 = length of blanks(ahead of c)
                    if t2==0 and count!=0:
                        # blank is necessary except for initial place
                        #print(' -1 ' + self.seq2str(seq + [t2, t1 - t2])+'|'+exp[1:])
                        continue
                    if exp[1:] and count+t1+2 > self.size:
                        # leave room for after syms
                        #print(' -2 ' + self.seq2str(seq + [t2, t1 - t2])+'|'+exp[1:])
                        continue
                    if dic.get(t1 - t2, exp[0]) != exp[0]:
                        # print((t1 - t2, exp[0]),dic)
                        continue
                    if rdic.get(exp[0], t1 - t2) != t1 - t2:
                        # print((exp[0], t1 - t2),rdic)
                        continue
                    dic[t1 - t2] = exp[0]
                    rdic[exp[0]] = t1 - t2
                    # print(' >  ' + self.seq2str(seq + [t2, t1 - t2])+'|'+exp[1:], tdic, dic)
                    stack.append((exp[1:], count + t1, seq + [t2, t1 - t2], dic, rdic))
        return result

    def solute(self):
        results = []
        stack = [self]
        count = 0
        while stack:
            temp = stack.pop()
            count += 1
            if count%5000==0:
                os.system('cls')
                print(count)
                temp.show(True)
            if temp.is_complete():
                results.append(temp)
            else:
                stack += temp.next()
        return results

    def manual(self):
        choice = []
        next = None
        l = [self.parent] + self.next()
        print('----------------------')
        for i in range(len(l)):
            if i==0 and not self.parent:
                continue
            choice.append(i)
            print(i,id(l[i]), l[i].d)
            l[i].show()
        print('input:')
        while True:
            n = input()
            if n == 'p':
                next = self.parent
                break
            elif n == 'a':
                break
            elif n.isnumeric() and int(n) in choice:
                next = l[int(n)]
                break
            else:
                print('Abort/Parent/num')
                continue
        if next:
            next.manual()


    def check(self):
        return True

    def seq2str(self, l, sym=['x','o']):
        result = ""
        c = 0
        for num in l:
            c += 1
            result += sym[c%2] * num
        return result

    def show(self, show_dic=False):
        c = 0
        e = False
        while True:
            for t in self.exp_v:
                if c<len(t):
                    print(t[c], end='')
                    e = True
                else:
                    print(' ', end='')
            print()
            c += 1
            if not e:
                break
            e = False
        print(' '*self.size)

        c = 0
        l = len(self.dots)
        while c < self.size**2:
            try:
                print('x' if self.dots[c] else ' ' , end='')
            except IndexError:
                print('_', end='')
            c += 1
            if c % self.size == 0:
                print(' ' + self.exp_h[(c-1)//self.size])
        print()
        if show_dic:
            for i in range(self.size):
                print("%3s %s" % (i, self.d.get(i,'')))

        # for i in range(self.size):
        #     if i < self.numl:
        #         for j in range(self.size):
        #             print('x' if self.dots[i*self.size + j] else 'o', end='' )
        #         print()
        #     else:
        #         print('_'*self.size)
        # print()


def find(base, manual=False):
    if manual:
        base.manual()
    else:
        c = 0
        for item in base.solute():
            c += 1
            print(c, item.d)
            item.show()

target = q2
base = State()
base.setup(len(target['h'].split()), target['h'], target['v'])

find(base,0)