class OrdinalNumber: #順序数を扱うクラス
    # __add__, __sub__,__mul__,__floordiv__,__mod__,__power__, を実装予定
    # 参考文献) https://www.behounek.online/logic/papers/ordcalc/index.html
    # 昔、順序数を扱うライブラリを作ってpipに上げたことがあるが、バグが見つかってずっと放置しているので、新しく作り直したいという欲望がある
    
    def iszore(self):
        return len(self.exp) == 0
    
    def isfinit(self):
        return self.iszore() or len(self.exp) == 1 and self.exp[0][1] == 0
    
    def toint(self):
        if self.iszore():
            return 0
        elif self.isfinit():
            return self.exp[0][0]
        else:
            raise ValueError("Cannot convert an infinite ordinal to an integer.")

    def isterm(self):
        return len(self.exp) <= 1
    
    def isomegapower(self):
        return len(self.exp) == 1 and self.exp[0][0] == 1 and self.exp[0][1] != 0
    
    
    def __init__(self,exp):
        if type(exp) == int and exp >= 0:    
            if exp == 0:
                self.exp = []
            else:
                self.exp = [(exp,0)]  # value = sum(ω**p*c for c,p in self.exp), sort(key=lambda x: x[1],reverse = True)
        elif exp == "omega" or exp == "ω":
            self.exp = [(1,1)]
        elif type(exp) == list:
            self.exp = sorted([((x[0],x[1].toint()) if type(x[1]) == OrdinalNumber and x[1].isfinit() else x) for x in exp if  x[0] != 0 ] ,key=lambda x: x[1], reverse=True)  # value = sum(ω**p*c for c,p in self.exp), sort(key=lambda x: x[1],reverse = True)
        else:
            raise TypeError("exp should be list ,non-negetive int ,'omega' or 'ω'.")


    def __add__(self,other):
        if type(other) == int and other >= 0:
            if other >= 0:
                return self + OrdinalNumber(other)
            else:
                raise ValueError("Cannot add a non-negative integer to an infinite ordinal.")
        elif type(other) == OrdinalNumber:
            if other.iszore():
                return self
            new_exp = other.exp.copy()
            for c, p in reversed(self.exp):
                c0, p0 = new_exp[0]
                if p == p0:
                    new_exp[0] = (c + c0, p0)
                elif p > p0:
                    new_exp.insert(0, (c, p))
                else:
                    pass  # p < p0, do nothing
            return OrdinalNumber(new_exp)
        else:
            raise TypeError("other should be non-negative int or OrdinalNumber")
    
    def __radd__(self,other):
        if type(other) == int and other >= 0:
            if other >= 0:
                return OrdinalNumber(other) + self
            else:
                raise ValueError("Cannot add a non-negative integer to an infinite ordinal.")
        elif type(other) == OrdinalNumber:
            return other + self
        else:
            raise TypeError("other should be non-negative int or OrdinalNumber")
    
    def __sub__(self,other):  #definition: x = a - b \iff b + x = a
        if type(other) == int and other >= 0:
            if other >= 0:
                return self - OrdinalNumber(other)
            else:
                raise ValueError("Cannot subtract a non-negative integer from an infinite ordinal.")
        elif type(other) == OrdinalNumber:
            if self < other:
                #print(self, other)
                raise ValueError("Cannot subtract a larger ordinal from a smaller one.")
            if other.iszore():
                return self
            flag = 0
            for i, ((c1,p1),(c2,p2)) in enumerate(zip(self.exp,other.exp)):
                if p1 > p2:
                    flag = 1
                    break
                elif c1 > c2:
                    flag = 2
                    break
            if flag == 0:
                if len(self.exp) == len(other.exp):
                    return OrdinalNumber(0)
                elif len(self.exp) > len(other.exp):
                    return OrdinalNumber(self.exp[len(other.exp):])
                elif len(self.exp) < len(other.exp):
                    raise ValueError("Cannot subtract a larger ordinal from a smaller one.")
            elif flag == 1:
                new_exp = []
                for c, p in self.exp[i:]:
                    new_exp.append((c, p))
                return OrdinalNumber(new_exp)
            elif flag == 2:
                new_exp = []
                for c, p in self.exp[i:]:
                    if p == p2:
                        new_exp.append((c - c2, p))
                    else:
                        new_exp.append((c, p))
                return OrdinalNumber(new_exp)
    
    def __rsub__(self,other):
        if type(other) == int and other >= 0:
            if other >= 0:
                return OrdinalNumber(other) - self
            else:
                raise ValueError("Cannot subtract a non-negative integer from an infinite ordinal.")
        elif type(other) == OrdinalNumber:
            return other - self
        else:
            raise TypeError("other should be non-negative int or OrdinalNumber")
    
    def __mul__(self,other):
        if type(other) == int and other >= 0:
            if other > 0:
                return self * OrdinalNumber(other)
            if other == 0:
                return OrdinalNumber(0)
            else:
                raise ValueError("Cannot multiply a non-negative integer with an infinite ordinal.")
        elif type(other) == OrdinalNumber:
            if other.iszore() or self.iszore():
                return OrdinalNumber(0)
            m = None
            if other.exp[-1][1] == 0:
                m = other.exp[-1][0]
            if m is not None:
                # sum{j=1..q-1} omega^{a1+bj}*mj + omega^{a1}*n1*m + sum{i=2..k} omega^{ai}*ni
                p1 = self.exp[0][1]
                new_exp1 = [(c,p1+p) for c, p in other.exp if p != 0]
                x1 = OrdinalNumber(new_exp1)
                x2 = OrdinalNumber([(self.exp[0][0] * m, p1)])
                new_exp2 = [(c, p) for c, p in self.exp[1:]]
                x3 = OrdinalNumber(new_exp2)
                return x1 + x2 + x3
            else:
                # sum{j=1..q-1} omega^{a1+bj}*mj
                p1 = self.exp[0][1]
                new_exp = [(c,p1+p) for c, p in other.exp if p != 0]
                return OrdinalNumber(new_exp)
        else:
            raise TypeError("other should be non-negative int or OrdinalNumber")
    
    def __rmul__(self,other):
        if type(other) == int and other >= 0:
            if other > 0:
                return OrdinalNumber(other) * self
            if other == 0:
                return OrdinalNumber(0)
            else:
                raise ValueError("Cannot multiply a non-negative integer with an infinite ordinal.")
        elif type(other) == OrdinalNumber:
            return other * self
        else:
            raise TypeError("other should be non-negative int or OrdinalNumber")

    def normaldiv(self,other):
        if type(other) == int and other >= 0:
            if other > 0:
                if self.isfinit():
                    return (OrdinalNumber(self.toint() // other), 0)
                else:
                    return self.normaldiv(OrdinalNumber(other))
            elif other == 0:
                raise ValueError("Cannot divide by zero.")
            else:
                raise ValueError("Cannot divide a non-negative integer by a negative integer.")
        if other.isfinit():
            if self.isfinit():
                return (OrdinalNumber(self.toint() // other.toint()), 0)
            else:
                p1 = other.exp[0][1]
                new_exp = [(c,p - p1) for c, p in self.exp if p > 0]
                if self.exp[-1][1] == 0:
                    new_exp.append((self.exp[-1][0] // other.toint(), 0))
                floor = OrdinalNumber(new_exp)
                mod = self - other * floor
                return (floor, mod)
        p1 = other.exp[0][1]
        c1 = other.exp[0][0]
        m = None
        if other.exp[-1][1] == 0:
            m = other.exp[-1][0]
        if m is not None:
            floor = OrdinalNumber([((c,p - p1) if p - p1 != 0 else (c//c1,0))  for c, p in self.exp if p >= p1])
            print(f'({other})*({floor}) = {other * floor}')
            print(self)
            if OrdinalNumber([(c,p) for c, p in self.exp if p < p1]) < OrdinalNumber([(c,p) for c, p in other.exp if p < p1]):
                if floor.exp[-1][1] == 0:
                    floor.exp[-1][0] = max(0, floor.exp[-1][0] - 1)
            mod = self - other * floor
            if not (0 <= mod < other):
                raise ValueError("The result of division is not in the expected range.")
            return (floor, mod)
        else:
            floor = OrdinalNumber([(c,p - p1) for c, p in self.exp if p >= p1])
            print(f'({other})*({floor}) = {other * floor}')
            print(self)
            if OrdinalNumber([(c,p) for c, p in self.exp if p < p1]) < OrdinalNumber([(c,p) for c, p in other.exp if p < p1]):
                if floor.exp[-1][1] == 0:
                    floor.exp[-1] = (max(0, floor.exp[-1][0] - 1),0)
            mod = self - other * floor
            if not (0 <= mod < other):
                raise ValueError("The result of division is not in the expected range.")
            return (floor, mod)



    def __floordiv__(self,other):
        if type(other) == int and other >= 0:
            if other > 0:
                return self.normaldiv(OrdinalNumber(other))[0]
            elif other == 0:
                raise ValueError("Cannot divide by zero.")
            else:
                raise ValueError("Cannot divide a non-negative integer by a negative integer.")
        elif type(other) == OrdinalNumber:
            if other.iszore():
                raise ValueError("Cannot divide by zero.")
            if self.iszore():
                return OrdinalNumber(0)
            return self.normaldiv(other)[0]
    
    def __rfloordiv__(self,other):
        if type(other) == int and other >= 0:
            if other > 0:
                return OrdinalNumber(other) // self
            elif other == 0:
                raise ValueError("Cannot divide by zero.")
            else:
                raise ValueError("Cannot divide a non-negative integer by a negative integer.")
        elif type(other) == OrdinalNumber:
            return other // self
        else:
            raise TypeError("other should be non-negative int or OrdinalNumber")
    
    def __mod__(self,other):
        if type(other) == int and other >= 0:
            if other > 0:
                return self.normaldiv(OrdinalNumber(other))[1]
            elif other == 0:
                raise ValueError("Cannot divide by zero.")
            else:
                raise ValueError("Cannot divide a non-negative integer by a negative integer.")
        elif type(other) == OrdinalNumber:
            if other.iszore():
                raise ValueError("Cannot divide by zero.")
            if self.iszore():
                return OrdinalNumber(0)
            return self.normaldiv(other)[1]
    
    def __rmod__(self,other):
        if type(other) == int and other >= 0:
            if other > 0:
                return OrdinalNumber(other) % self
            elif other == 0:
                raise ValueError("Cannot divide by zero.")
            else:
                raise ValueError("Cannot divide a non-negative integer by a negative integer.")
        elif type(other) == OrdinalNumber:
            return other % self
        else:
            raise TypeError("other should be non-negative int or OrdinalNumber")
    
    def __pow__(self,other):
        if type(other) == int and other >= 0:
            return self ** OrdinalNumber(other)
        elif type(other) == OrdinalNumber:
            if other.iszore():
                return OrdinalNumber(1)
            if self.iszore():
                return OrdinalNumber(0)
            if self == 1:
                return OrdinalNumber(1)
            if other.isfinit():
                # Theorem 4 (Ordinal Finite Power):
                # Let r > 1 be a natural number,
                # a = sum{i=1..k-1} omega^{ai}*ni + m
                # be a non-zero ordinal in the Cantor normal form. Then the Cantor normal form of a^r is
                # sum{i=1..k-1} omega^{a1*(r-1)+ai}*ni + sum{j=1..r-1} (omega^{a1}*(r-j)*n1*m + sum{i=2..k-1} omega^{a1*(r-j-1)+ai}*ni)
                # if m > 0, or
                # sum{i=1..k-1} omega^{a1*(r-1)+ai}*ni
                # if m = 0.
                r = other.toint()
                if r < 0:
                    raise ValueError("Cannot raise an ordinal to a negative power.")
                if r == 0:
                    return OrdinalNumber(1)
                if r == 1:
                    return OrdinalNumber(self.exp)
                if self.isfinit():
                    n = self.toint()
                    return OrdinalNumber(n ** r)
                p1 = self.exp[0][1]
                m = None
                if self.exp[-1][1] == 0:
                    m = self.exp[-1][0]
                if m is not None: # m > 0
                    new_exp1 = [] # sum{i=1..k-1} omega^{a1*(r-1)+ai}*ni
                    for c, p in self.exp:
                        if p != 0:
                            new_exp1.append((c, p1 * (r - 1) + p))
                    x1 = OrdinalNumber(new_exp1)
                    new_exp2 = []  # sum{j=1..r-1} (omega^{a1}*(r-j)*n1*m + sum{i=2..k-1} omega^{a1*(r-j-1)+ai}*ni)
                                   # ↑　これ本当か？ (omega^{a1}*(r-j)*n1*m じゃなくて omega^{a1*(r-j)}*n1*m では？)
                    for j in range(1, r):
                        new_exp3 = []
                        for c, p in self.exp[1:]:
                            if p != 0:
                                new_exp3.append((c, p1 * (r - j - 1) + p))
                        new_exp2.append(OrdinalNumber([(self.exp[0][0] * m, p1 * (r - j))])+OrdinalNumber(new_exp3))
                    x2 = 0
                    for o in new_exp2:
                        x2 += o
                    return x1 + x2 + OrdinalNumber(m)
                else: # m = 0
                    new_exp = []  # sum{i=1..k-1} omega^{a1*(r-1)+ai}*ni
                    for c, p in self.exp:
                        if p != 0:
                            new_exp.append((c, p1 * (r - 1) + p))
                    return OrdinalNumber(new_exp)
            else:
                # Theorem 5 (Ordinal Power):
                # Let
                # a = sum{i=1..k} omega^{ai}*ni,
                # b = sum{j=1..q-1} omega^{bi}*mj + m
                # be ordinals in the Cantor normal form. Then
                # a^b = omega^{a1 * sum{j=1..q-1}omega^{bi}*mj} * a^m
                # if a is infinite, or
                # a^b = omega^{sum{j=1..q-1}omega^{bi}*mj} * a^m,
                # (↑ これほんまか？　= omega^{sum{j=1..q-1}omega^{bi - 1}*mj} * a^m になるはず)
                # if a is finite. The latter case is the Cantor normal form of a^b, the former can be transformed into it with Theorems 4 and 3.
                m = 0
                p1 = self.exp[0][1]
                if other.exp[-1][1] == 0:
                    m = other.exp[-1][0]
                if self.isfinit():
                    new_exp = [((c, p - 1) if p != 1 else (c, 0)) for c, p in other.exp if p != 0] # omega^{a1 * sum{j=1..q-1}omega^{bi}*mj} * a^m
                    return OrdinalNumber([(1,OrdinalNumber(new_exp) if not OrdinalNumber(new_exp).isfinit() else OrdinalNumber(new_exp).toint())]) * self ** OrdinalNumber(m)
                else:  # self.isomegapower()
                    new_exp = [(c, p) for c, p in other.exp if p != 0] # omega^{a1 * sum{j=1..q-1}omega^{bi}*mj} * a^m
                    return OrdinalNumber([(1,p1 * OrdinalNumber(new_exp))]) * self ** OrdinalNumber(m)
        else:
            raise TypeError("other should be non-negative int or OrdinalNumber")
        
    def __rpow__(self,other):
        if type(other) == int and other >= 0:
            return OrdinalNumber(other) ** self
        elif type(other) == OrdinalNumber:
            return other ** self
        else:
            raise TypeError("other should be non-negative int or OrdinalNumber")

    def __repr__(self):
        if self.iszore():
            return "0"
        elements_modified = []
        for c, p in self.exp:
            if c == 1:
                if p == 0 or type(p) == OrdinalNumber and p.iszore():
                    elements_modified.append(("","1"))
                else:
                    if p == 1:
                        elements_modified.append(("","OrdinalNumber.omega"))
                    elif type(p) == int or p.isfinit() or p.isomegapower():
                        elements_modified.append(("","OrdinalNumber.omega**"+repr(p)))
                    else:
                        elements_modified.append(("","OrdinalNumber.omega**("+repr(p)+")"))
            else:
                if p == 0:
                    elements_modified.append((str(c),""))
                else:
                    if p == 1:
                        elements_modified.append(("*"+str(c),"OrdinalNumber.omega"))
                    elif type(p) == int or p.isomegapower():
                        elements_modified.append(("*"+str(c),"OrdinalNumber.omega**"+repr(p)))
                    else:
                        elements_modified.append(("*"+str(c),"OrdinalNumber.omega**("+repr(p)+")"))
        return " + ".join(f"{p}{c}" for c, p in elements_modified)
    
    def __str__(self):
        if self.iszore():
            return "0"
        elements_modified = []
        for c, p in self.exp:
            if c == 1:
                if p == 0 or type(p) == OrdinalNumber and p.iszore():
                    elements_modified.append(("","1"))
                else:
                    if p == 1:
                        elements_modified.append(("","ω"))
                    elif type(p) == int or p.isfinit() or p.isomegapower():
                        elements_modified.append(("","ω^"+str(p)))
                    else:
                        elements_modified.append(("","ω^("+str(p)+")"))
            else:
                if p == 0:
                    elements_modified.append((str(c),""))
                else:
                    if p == 1:
                        elements_modified.append(("*"+str(c),"ω"))
                    elif type(p) == int or p.isfinit() or p.isomegapower():
                        elements_modified.append(("*"+str(c),"ω^"+str(p)))
                    else:
                        elements_modified.append(("*"+str(c),"ω^("+str(p)+")"))
        return " + ".join(f"{p}{c}" for c, p in elements_modified)
    
    def __eq__(self,other):
        if type(other) == int:
            if self.isfinit() and other >= 0:
                return self.toint() == other
            else:
                return False
        elif type(other) == OrdinalNumber:
            if len(self.exp) != len(other.exp):
                return False
            for (c1,p1),(c2,p2) in zip(self.exp,other.exp):
                if c1 != c2 or p1 != p2:
                    return False
            return True
        else:
            raise TypeError("other should be non-negative int or OrdinalNumber")

    
    def __le__(self,other):
        if type(other) == int and other >= 0:
            if self.isfinit():
                return self.toint() <= other
            else:
                return False
        elif type(other) == OrdinalNumber:
            for (c1,p1),(c2,p2) in zip(self.exp,other.exp):
                if p1 < p2:
                    return True
                elif p1 > p2:
                    return False
                elif c1 < c2:
                    return True
                elif c1 > c2:
                    return False
            return len(self.exp) <= len(other.exp)
        else:
            raise TypeError("other should be non-negative int or OrdinalNumber")
            
    
    def __lt__(self,other):
        return self.__le__(other) and not self.__eq__(other)
    
    def __gt__(self,other):
        return not self.__le__(other)
    
    def __ge__(self,other):
        if type(other) == int and other >= 0:
            if self.isfinit():
                return self.toint() >= other
            else:
                return True
        elif type(other) == OrdinalNumber:
          return not self.__le__(other) or self.__eq__(other)
        else:
            raise TypeError("other should be non-negative int or OrdinalNumber")
    
    def __ne__(self,other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(tuple(self.exp))

    def __bool__(self):
        return not self.iszore()

OrdinalNumber.omega = OrdinalNumber("omega")


def main():
    # テストコード
    o1 = OrdinalNumber(3)
    o2 = OrdinalNumber("omega")
    o3 = OrdinalNumber([(2,1),(1,0)])
    o4 = OrdinalNumber([(1,1)])
    o5 = OrdinalNumber([(1,2),(2,1),(1,0)])
    o6 = OrdinalNumber([(1,2),(1,1),(1,0)])
    o7 = OrdinalNumber([(1,4),(1,3),(2,2),(3,1),(1,0)])
    o8 = OrdinalNumber(5)
    
    print(o1)  # 3
    print(o2)  # ω
    print(o3)  # ω*2 + 1
    print(o4)  # ω^1
    print(o5)  # ω^2 + ω*2 + 1
    print(o6)  # ω^2 + ω + 1
    print(o7)  # ω^4 + ω^3 + ω^2*2 + ω*3 + 1

    
    print(o1 < o2)  # True
    print(o2 > o3)  # False
    print(o2 == o4)  # True

    
    print(o1 + o2)  # = ω
    print(o2 + o1)  # = ω + 3
    print(o3 + o4)  # = ω*3
    print(o4 + o3)  # = ω*3 + 1

    print(o5 - o6)  # = ω + 1
    sub = o5 - o6
    print(o6 + sub)  # = ω^2 + ω*2 + 1

    print(o1 * o2)  # = ω
    print(o2 * o1)  # = ω*3
    print(o3 * o4)  # = ω^2*2
    print(o5 * o6)  # = ω^4 + ω^3 + ω^2 + ω*2 + 1

    print(o7 // o6)  # = ω^2 + ω + 1
    print(o7 % o6)   # = ω*2 + 1
    f = o7 // o6
    m = o7 % o6
    print(o6 * f + m)  # = ω^4 + ω^3 + ω^2*2 + ω*3 + 1
    print(o8.normaldiv(o1))   # = (1,2)

    print(o7.__repr__())  # = 1
    print(OrdinalNumber.omega**4)
    print(OrdinalNumber.omega**3)
    print(OrdinalNumber.omega**2 * 2)
    print(OrdinalNumber.omega**1 * 3)
    print(OrdinalNumber.omega**4 + OrdinalNumber.omega**3 + OrdinalNumber.omega**2*2 + OrdinalNumber.omega*3 + 1)
    print(o7.__str__())  # = ω^4 + ω^3 + ω^2*2 + ω*3 + 1

    print((2 ** o2).exp)  # = ω
    print(2 ** o2)  # = ω
    print(o5 ** o3) # = ω^(ω*2+2)+ω^(ω*2+1)*2+ω^(ω*2)


    # 追加テストケース
    print("=== 追加テストケース ===")
    # 基本演算
    a = OrdinalNumber(0)
    b = OrdinalNumber(1)
    c = OrdinalNumber(5)
    d = OrdinalNumber("omega")
    e = OrdinalNumber([(2,1),(3,0)])  # ω*2 + 3
    f = OrdinalNumber([(1,2),(2,1),(1,0)])  # ω^2 + ω*2 + 1
    g = OrdinalNumber([(1,d)]) # ω^ω

    # 加算
    print("加算")
    print(a + b)  # 1
    print(b + c)  # 6
    print(c + d)  # ω
    print(d + c)  # ω + 5
    print(e + f)  # ω^2 + ω*2 + 1

    # 減算
    print("減算")
    print(c - b)  # 4
    print(f - e)  # ω^2 + ω*2 + 1
    print(e - b)  # ω*2 + 3
    print(f - OrdinalNumber([(1,2)]))  # ω*2 + 1

    # 乗算
    print("乗算")
    print(b * c)  # 5
    print(c * b)  # 5
    print(d * c)  # ω*5
    print(c * d)  # ω
    print(e * b)  # ω*2 + 3
    print(e * c)  # ω*10 + 3
    print(f * b)  # ω^2 + ω*2 + 1
    print(f * d)  # ω^3

    # 除算・剰余
    print("除算・剰余")
    print(c // b)  # 5
    print(c % b)   # 0
    print(e // b)  # ω*2 + 3
    print(e % b)   # 0
    print(e // c)  # ω*2
    print(e % c)   # 3
    print(f // e)  # ω
    print(f % e)   # ω*2 + 1

    # 比較
    print("比較")
    print(a == 0)  # True
    print(b == 1)  # True
    print(c == 5)  # True
    print(d > c)   # True
    print(e < f)   # True
    print(f > e)   # True
    print(f == f)  # True
    print(f != e)  # True
    print(e <= f)  # True
    print(f >= e)  # True
    print(a < b)   # True
    print(a <= b)  # True
    print(b > a)   # True
    print(b >= a)  # True

    # 右側演算
    print("右側演算")
    print(3 + d)   # ω
    print(3 * d)   # ω
    print(3 ** b)  # 3
    print(2 ** d)  # ω
    print(d ** 2)  # ω^2
    print(d ** 3)  # ω^3
    print((d + 1) ** 2)  # ω^2 + ω + 1

    # pow の複雑なケース
    print("pow の複雑なケース")
    print(f ** b)  # ω^2 + ω*2 + 1
    print(f ** 2)  # ω^4 + ω^3*2 + ω^2 + ω*2 + 1
    print(f * f)   # ω^4 + ω^3*2 + ω^2 + ω*2 + 1
    print(e ** 2)  # ω^2*2 + ω*6 + 3
    print(e * e)   # ω^2*2 + ω*6 + 3
    print(e ** 3)  # ω^3*2 + ω^2*6 + ω*6 + 3
    print(e * e * e) # ω^3*2 + ω^2*6 + ω*6 + 3    # ω*2 + 3

    # 正規化・repr/str
    print("正規化・repr/str")
    print(repr(a))
    print(str(a))
    print(repr(d))
    print(str(d))
    print(repr(e))
    print(str(e))
    print(repr(f))
    print(str(f))

    # hash, bool
    print("hash, bool")
    print(hash(a), bool(a))
    print(hash(b), bool(b))
    print(hash(d), bool(d))

    # 0除算例外
    print("0除算例外")
    try:
        print(c // 0)
    except Exception as ex:
        print("ZeroDivisionError:", ex)
    try:
        print(c % 0)
    except Exception as ex:
        print("ZeroDivisionError:", ex)
    try:
        print(d // 0)
    except Exception as ex:
        print("ZeroDivisionError:", ex)

    # 型エラー例外
    print("型エラー例外")
    try:
        print(c + "abc")
    except Exception as ex:
        print("TypeError:", ex)
    try:
        print(d * -1)
    except Exception as ex:
        print("ValueError:", ex)

    # 変換
    print("変換")
    print(OrdinalNumber(10).toint())
    print(OrdinalNumber([(1,0)]).toint())
    try:
        print(d.toint())
    except Exception as ex:
        print("ValueError:", ex)

    # iszore, isfinit, isterm, isomegapower
    print("iszore, isfinit, isterm, isomegapower")
    print(a.iszore(), b.iszore(), d.iszore())
    print(a.isfinit(), b.isfinit(), d.isfinit())
    print(a.isterm(), b.isterm(), d.isterm())
    print(a.isomegapower(), b.isomegapower(), d.isomegapower())

    # normaldiv
    print("normaldiv")
    print(c.normaldiv(2))  # (2,1)
    print(e.normaldiv(b))  # (ω*2+3, 0)
    print(e.normaldiv(c))  # (ω*2, 3)
    print(f.normaldiv(e))  # (ω, ω*2 + 1)

    # __radd__, __rsub__, __rmul__, __rfloordiv__, __rmod__, __rpow__
    print("右側演算子")
    print(2 + d)
    print(2 * d)
    print(OrdinalNumber(10) - b)
    print(OrdinalNumber(10) // b)
    print(OrdinalNumber(10) % b)
    print(2 ** d)

    # __ne__ の確認
    print("__ne__の確認")
    print(a != b)
    print(d != d)
    print(e != f)

    # __bool__ の確認
    print("bool確認")
    print(bool(a))
    print(bool(b))
    print(bool(d))

    # __hash__ の確認
    print("__hash__の確認")
    print(hash(a))
    print(hash(d))
    print(hash(e))
    print(hash(f))

    # さらに複雑な演算
    print("さらに複雑な演算")
    print((d + 1) * (d + 2))
    print((d + 1) ** 3)
    print((d * 2 + 1) ** 2)
    print((d ** 2 + d + 1) * (d + 1))
    print((d ** 2 + d + 1) // (d + 1))
    print((d ** 2 + d + 1) % (d + 1))

    # 0, 1, ω, ω^2, ω^3, ω^4, ω^5
    print("0, 1, ω, ω^2, ω^3, ω^4, ω^5 の確認")
    print(OrdinalNumber.omega**0)
    print(OrdinalNumber.omega**1)
    print(OrdinalNumber.omega**2)
    print(OrdinalNumber.omega**3)
    print(OrdinalNumber.omega**4)
    print(OrdinalNumber.omega**5)

    # 演算と比較を含む式
    print("演算と比較を含む式")
    # 1 + ω == ω
    print(1 + d == d)
    # ω + 1 != ω
    print(d + 1 != d)
    # ω^2 > ω
    print((d**2) > d)
    # ω^2 + ω + 1 > ω^2 + 1
    print((d**2 + d + 1) > (d**2 + 1))
    # ω^2 + ω + 1 < ω^3
    print((d**2 + d + 1) < (d**3))

    # 逆順比較
    print("逆順比較")
    print(d < d + 1)
    print(d + 1 > d)
    print(d + 1 >= d)
    print(d <= d + 1)
    print(d >= d)
    print(d <= d)

    # 0の比較
    print("0の比較")
    print(a == 0)
    print(a < 1)
    print(a <= 0)
    print(a >= 0)
    #print(a > -1) ← 0は負数と比較できないため、エラーになる

    # 1項のみの順序数
    print("1項のみの順序数")
    print(OrdinalNumber([(3,0)]))
    print(OrdinalNumber([(1,3)]))
    print(OrdinalNumber([(2,2)]))
    print(OrdinalNumber([(1,1)]))
    print(OrdinalNumber([(1,0)]))

    # 2項以上の順序数
    print("2項以上の順序数")
    print(OrdinalNumber([(1,2),(2,1),(3,0)]))
    print(OrdinalNumber([(2,3),(1,2),(1,1),(1,0)]))

    # 0項
    print("0項の順序数")
    print(OrdinalNumber([]))

    # 例外系
    print("例外系")
    try:
        print(OrdinalNumber(-1))
    except Exception as ex:
        print("TypeError/ValueError:", ex)
    try:
        print(OrdinalNumber("abc"))
    except Exception as ex:
        print("TypeError:", ex)
    try:
        print(OrdinalNumber([(0,0)]))
    except Exception as ex:
        print("TypeError:", ex)

    # g = ω^ω を使ったテストケース
    print("g = ω^ω を使ったテストケース")
    print("g:", g)
    print("g + 1:", g + 1)
    print("g + d:", g + d)
    print("g * 2:", g * 2)
    print("2 * g:", 2 * g)
    print("g ** 2:", g ** 2)
    print("g > d ** 10:", g > (d ** 10))
    print("g > d ** 100:", g > (d ** 100))
    print("g < d ** g:", g < (d ** g))
    print("g == OrdinalNumber([(1,d]]):", g == OrdinalNumber([(1,d)]))
    print("g > d:", g > d)
    print("g > f:", g > f)
    print("g < g + 1:", g < g + 1)
    print("g == g:", g == g)
    print("g != g + 1:", g != g + 1)
    print("g // d:", g // d)
    print("g % d:", g % d)
    print("g + g:", g + g)
    print("g * g:", g * g)
    print("g ** b:", g ** b)
    print("g ** 0:", g ** 0)
    print("g ** 1:", g ** 1)
    print("g ** d:", g ** d)
    print("str(g):", str(g))
    print("repr(g):", repr(g))
    print("hash(g):", hash(g))
    print("bool(g):", bool(g))
    # 比較
    print("g > d ** 1000:", g > (d ** 1000))
    print("g < OrdinalNumber([(1, g)]):", g < OrdinalNumber([(1, g)]))
    print("g == OrdinalNumber([(1, d)]):", g == OrdinalNumber([(1, d)]))
    print("g != OrdinalNumber([(2, d)]):", g != OrdinalNumber([(2, d)]))
    print("g >= g:", g >= g)
    print("g <= g:", g <= g)
    print("g < g + 1:", g < g + 1)
    print("g == g - 1:", g == (g - 1))

def test():
    # 手動テスト
    omega = OrdinalNumber.omega
    print("手動テスト")
    a = omega**omega * 3 + 1
    b = omega**omega + 2
    print("a:", a) 
    print("b:", b)
    print("a // b:", a // b)
    print("a % b:", a % b)
    print("b * a // b + a % b:", b * (a // b) + (a % b))

def test_():
    # 手動テスト
    omega = OrdinalNumber.omega
    print("手動テスト")
    a = omega**omega * 4 + omega**10 * 2 + 1
    b = omega**omega * 2 + omega**12 * 8
    print("a:", a) 
    print("b:", b)
    print("a // b:", a // b)
    print("a % b:", a % b)
    print("b * a // b + a % b:", b * (a // b) + (a % b))

def test2():
    # 順序数ωの除算・剰余演算のテストケース配列
    array = [
        # ---- 基本的なケース ----
        # 被除数が有限数
        ("20", "3"),
        # ωを有限数で割る (左除算)
        ("omega", "10"),
        # ω+n / ω
        ("omega + 5", "omega"),
        # ω*m / ω*k
        ("omega * 8", "omega * 3"),
        # ω*m+n / ω*k+l
        ("omega * 5 + 10", "omega * 2 + 3"),

        # ---- 次数が関わるケース (多項式除算に類似) ----
        # ω^2 / ω
        ("omega**2", "omega"),
        # (ω^2) / (ω+n)
        ("omega**2", "omega + 5"),
        # (ω^2+n) / (ω+k)
        ("omega**2 + 10", "omega + 3"),
        # 一般的な多項式形式の除算
        ("omega**2 * 7 + omega * 3 + 2", "omega * 2 + 1"), # ユーザー提供の例
        ("omega**2 + omega * 5 + 8", "omega + 3"),
        ("omega**3 * 4 + omega * 2 + 7", "omega**2 * 2 + omega * 3 + 1"),
        
        # ---- 係数が1で、項が飛んでいるケース ----
        ("omega**3 + 2", "omega**2 + omega*5 + 1"),
        ("omega**5 + omega**2 + 100", "omega**2 + 1"),
        
        # ---- 複雑な係数や次数のケース ----
        ("omega**3 * 2 + omega**2 * 4 + omega * 6 + 8", "omega * 3 + 2"),
        ("omega**4", "omega**2 * 5 + omega * 8 + 3"),

        # ---- 指数にωが含まれる超限的なケース ----
        # ω^ω / ω^n
        ("omega**omega", "omega**100"),
        # (ω^ω + α) / β
        ("omega**omega + omega**2 * 5 + 10", "omega**3 + omega*2 + 1"),
        # (ω^ω * m + ...) / (ω^ω * k + ...)
        ("omega**omega * 5 + omega**10 * 4", "omega**omega * 2 + omega**12 * 8"),
        ("omega**omega * 3", "omega**omega + 1"),
        
        # ---- さらに複雑な指数のケース ----
        ("omega**(omega+1)", "omega**omega"),
        ("omega**(omega*2) + omega**omega * 5", "omega**(omega*2) + omega**omega * 2 + 100"),
        ("omega**(omega**2)", "omega**omega * 10"),
    ]

    omega = OrdinalNumber.omega
    for a,b in array:
        try:
            ord_a = eval(a.replace("omega", "OrdinalNumber.omega"))
            ord_b = eval(b.replace("omega", "OrdinalNumber.omega"))
            result = ord_a // ord_b
            mod = ord_a % ord_b
            print(f"{ord_a} // {ord_b} = {result}, {ord_a} % {ord_b} = {mod}")
            if ord_a == ord_b * result + mod:
                print(f"  正しい: {ord_a} = {ord_b} * {result} + {mod}")
            else:
                print(f"  誤り: {ord_a} != {ord_b} * {result} + {mod}")
        except Exception as e:
            print(f"Error for {a} // {b}: {e}")
if __name__ == "__main__":
    #test()
    test_()
