import matplotlib.pyplot as plt

class Report(object):

    def __init__(self, data, filters=(), show_title=True, fig_size=None):
        self.data = data
        self.filters = filters
        self.fig = None
        self.ax = None
        self.show_title = show_title

        if fig_size is not None:
            self.fig_size = fig_size

    def create_figure(self, data):
        fig, ax = self.__create_axes()
        self.plot(data, fig, ax)
        return fig, ax

    def __perpare_data(self):
        data = self.data
        for pred in self.filters:
            data = data.filter(pred)
        return data

    @property
    def figsize(self):
        return (6, 4)

    def __actual_figure_size(self):
        try:
            return self.fig_size
        except AttributeError:
            pass

    @property
    def subplots_params(self):
        return {}

    def __create_axes(self):
        size = self.__actual_figure_size()
        fig, ax = plt.subplots(figsize=size, **self.subplots_params)
        return fig, ax

    @property
    def title(self):
        return None

    def plot(self, data, fig, ax):
        pass

    @property
    def figure(self):
        if self.fig is None:
            data = self.__perpare_data()
            self.fig, self.ax = self.create_figure(data)
        return self.fig

    def __prepare_figure(self):
        fig = self.figure
        title = self.title
        if title is not None and self.show_title:
            self.ax.set_title(title)
        plt.tight_layout(pad=0.35)
        return fig

    def to_file(self, path):
        self.__prepare_figure().savefig(path)

    def show(self):
        plt.show(self.__prepare_figure())
