from algo.point import Point


class EC:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def lambda_add(self, P, Q):
        assert Q.x != 0

        factor = P.y / Q.x
        lmda = (Q.y - factor - P.x) % self.p
        return lmda

    def add(self, P, Q):
        lmda = self.lambda_add(P, Q)
        x = (pow(lmda, 2) - P.x - Q.x) % self.p
        y = (lmda * (P.x - x) - P.y) % self.p

        return Point(x, y)

    def sub(self, P, Q):
        Q.y *= -1
        return self.add(P, Q)

    def lambda_double(self, P):
        assert P.y != 0
        lmda = ((3 * pow(P.x, 2)) + (self.a / (2 * P.y))) % self.p
        return lmda

    def double(self, P):
        lmda = self.lambda_double(P)
        x = (pow(lmda, 2) - 2 * P.x) % self.p
        y = ((lmda * (P.x - x)) - P.y) % self.p

        return Point(x, y)

    def mul(self, P, n):
        R = P
        for i in range(n):
            R = self.add(R, P)

        return R
