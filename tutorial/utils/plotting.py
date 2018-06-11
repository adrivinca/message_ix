
import matplotlib.pyplot as plt

firstyear = 2010



class Plots(object):

    def __init__(self, ds, country):
        self.ds = ds
        self.country = country

    def plot_demand(self, light_demand, elec_demand):
        fig, ax = plt.subplots()
        l = light_demand['value']
        l.plot(ax=ax, label='light')
        e = elec_demand['value']
        e.plot(ax=ax, label='elec')
        (l + e).plot(ax=ax, label='total')
        plt.ylabel('GWa')
        plt.xlabel('Year')
        plt.legend(loc='best')

    def plot_vintages(self, var, baseyear=False, subset=None):
        df = self.ds.var(var)
        if not baseyear:
            df = df[df['year_vtg'] > firstyear]
        if subset is not None:
            df = df[df['technology'].isin(subset)]
        idx = ['year_act', 'technology']
        df = df[idx + ['year_vtg', 'lvl']].groupby(idx).sum().reset_index()
        df.pivot(index='year_act', columns='technology',
                 values='lvl').plot.bar(stacked=True)

    def plot_activity(self, baseyear=False, subset=None):
        self.plot_vintages('ACT', baseyear=baseyear, subset=subset)
        plt.title('{} Energy System Activity'.format(self.country.title()))
        plt.ylabel('GWa')
        plt.xlabel('Year')
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

    def plot_capacity(self, baseyear=False, subset=None):
        self.plot_vintages('CAP', baseyear=baseyear, subset=subset)
        plt.title('{} Energy System Capacity'.format(self.country.title()))
        plt.ylabel('GWa')
        plt.xlabel('Year')
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

    def plot_no_vintage(self, var, baseyear=False, subset=None):
        df = self.ds.var(var)
        if not baseyear:
            df = df[df['year_vtg'] > firstyear]
        if subset is not None:
            df = df[df['technology'].isin(subset)]
        df.pivot(index='year_vtg', columns='technology',
                 values='lvl').plot.bar(stacked=True)

    def plot_new_capacity(self, baseyear=False, subset=None):
        self.plot_no_vintage('CAP_NEW', baseyear=baseyear, subset=subset)
        plt.title('{} Energy System New Capcity'.format(self.country.title()))
        plt.ylabel('GWa')
        plt.xlabel('Year')
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

    def plot_equ(self, equ, value, baseyear=False, subset=None):
        df = self.ds.equ(equ)
        if not baseyear:
            df = df[df['year'] > firstyear]
        if subset is not None:
            df = df[df['commodity'].isin(subset)]
        df = df.pivot(index='year', columns='commodity', values=value)
        df.plot.bar(stacked=False)

    def plot_prices(self, baseyear=False, subset=None):
        self.plot_equ('COMMODITY_BALANCE', 'mrg',
                      baseyear=baseyear, subset=subset)
        plt.title('{} Energy System Prices'.format(self.country.title()))
        plt.ylabel('$/GWa')
        plt.xlabel('Year')
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
