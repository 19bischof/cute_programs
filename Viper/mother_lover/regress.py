from math import sqrt


class _linear_regression:
    """linear_regression parent class"""

    def __init__(self):
        self.slope = None
        self.start_y = None
        self.keys = []
        self.values = []
        self.std_deviation_x = None
        self.std_deviation_y = None
        self.mean_x = None
        self.mean_y = None
        self.co_variance = None
        self.co_relation = None

    def __repr__(self):
        print("-----------out:")
        out = ""
        if self.std_deviation_x != None != self.std_deviation_y:
            out += "std_deviation_x: {:.4f}\nstd_deviation_y: {:.4f}\n".format(
                self.std_deviation_x, self.std_deviation_y
            )

        if self.mean_x != None != self.mean_y:
            out += "x_mean: {:.4f}\ny_mean: {:.4f}\n".format(self.mean_x, self.mean_y)

        if self.co_relation != None != self.co_variance:
            out += "co_variance: {:.4f}\nco_relation: {:.4f}\n".format(
                self.co_variance, self.co_relation
            )

        if self.slope != None != self.start_y:
            out += "formulary: y = {:1.2f}x {} {:1.2f}\n".format(
                self.slope,
                "+" if self.start_y >= 0 else "-",
                abs(self.start_y),
            )
        return out

    def add_data_point(self, x, y):
        """adds data to the linear regression model
        :param x : the key
        :param y : the value"""
        self.keys.append(x)
        self.values.append(y)

    def fit(self):
        """trains the linear regression model"""
        pass

    def guess(self, key):
        """let the linear regression model make a guess"""
        if self.slope != None != self.start_y:
            value = self.slope * key + self.start_y
            return value


class simple_lin_regress(_linear_regression):
    """implementation of a simple linear regression model"""

    def fit(self):
        if len(self.keys) < 2:
            return
        length = len(self.keys)
        sum_x = sum(self.keys)
        sum_y = sum(self.values)
        self.mean_x = sum_x / length
        self.mean_y = sum_y / length

        self.std_deviation_x = sqrt(
            sum([(key - self.mean_x) ** 2 for key in self.keys]) / (length - 1)
        )
        self.std_deviation_y = sqrt(
            sum([(value - self.mean_y) ** 2 for value in self.values]) / (length - 1)
        )
        helper = [
            (key - self.mean_x) * (value - self.mean_y)
            for key, value in zip(self.keys, self.values)
        ]
        self.co_variance = sum(helper) / (length - 1)
        self.co_relation = self.co_variance / (
            self.std_deviation_x * self.std_deviation_y
        )
        self.slope = self.std_deviation_y / self.std_deviation_x * self.co_relation
        self.start_y = (sum_y - self.slope * sum_x) / length

    def show(self):
        """plot the model"""
        import matplotlib.pyplot as plt
        import numpy as np

        fig, ax = plt.subplots()

        # Plot the data
        data_line = ax.scatter(self.keys, self.values)
        # Plot the average line
        x_vals = np.array(self.keys)
        y_vals = x_vals * self.slope + self.start_y
        mean_line = ax.plot(
            x_vals,
            y_vals,
            "r",
            label="Mean",
            linestyle="-",
        )
        plt.show()

class multi_lin_regress(_linear_regression):
    #sadly i had to give up on trying to build my own multiple_lin_regress since i havent found a good formular and
    #there is an already existing module that does this exact thing but better!
    def fit(self):
        from sklearn import linear_model
        self.regr = linear_model.LinearRegression()
        self.regr.fit(self.keys,self.values)
    def guess(self,key):
        return self.regr.predict(key)
if __name__ == "__main__":
    keys = "28	23	32	35	29	30	27	34	32".split("\t")
    values = "400	60	630	560	290	620	440	610	250".split("\t")
    keys = [int(key) for key in keys] * 1000
    values = [int(value) for value in values] * 1000
    import tqdm
    import time

    t = time.perf_counter()
    for x in tqdm.tqdm(range(100)):
        r = simple_lin_regress()
        if len(keys) != len(values):
            print("bad data!!!")
            quit()
        for i in range(len(keys)):
            r.add_data_point(keys[i], values[i])
        r.fit()
    print(r)
    print((time.perf_counter() - t) * 1000, "ms")
    r.show()
