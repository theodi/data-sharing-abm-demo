import pandas as pd
import numpy as np

import plotly.graph_objs as go
from plotly import tools

scen_colours = ['#4a90e2', '#1dd3a7']
dark_scen_colours = ['#206dc5', '#18b48d']

GREY = '#eaeaea'


def plot_market_concentration(res_df_1, res_df_2):
    """
    returns a plot with the market share of the three biggest firms per category over the last year
    """
    data = [
        go.Bar(x=res_df_1.category.values.astype(int), y=res_df_1.consumer, hoverinfo='text',
               hovertext=['{}%, total {} companies'.format(x, y)
                          for x, y in zip(res_df_1.consumer, res_df_1.firms_active)],
               marker={'opacity': [1 if x > 3 else 0.5 for x in res_df_1.firms_active],
                       'color': scen_colours[0]},
               name='Scenario 1'),
        go.Bar(x=res_df_2.category.values.astype(int), y=res_df_2.consumer, hoverinfo='text',
               hovertext=['{}%, total {} companies'.format(x, y)
                          for x, y in zip(res_df_2.consumer, res_df_2.firms_active)],
               marker={'opacity': [1 if x > 3 else 0.5 for x in res_df_2.firms_active],
                       'color': scen_colours[1]},
               name='Scenario 2')
    ]
    layout = go.Layout(title='Market share of top three companies in each category',
                       yaxis={'title': 'Share of top three companies in product category'},
                       xaxis={'title': 'Product category'},
                       font={'family': 'HelveticaNeue'})
    return go.Figure(data=data, layout=layout)


def plot_firm_specialisation(df1, df2):
    """
    return a plot with the distribution of the number of categories firms
    are active in at the end of the simulation
    """
    data = [
        go.Bar(x=df1.bins, y=df1.perc, hoverinfo='text',
               hovertext=['{}%'.format(x) for x in df1.perc],
               name='Scenario 1', marker={'color': scen_colours[0]}),
        go.Bar(x=df2.bins, y=df2.perc, hoverinfo='text',
               hovertext=['{}%'.format(x) for x in df2.perc],
               name='Scenario 2', marker={'color': scen_colours[1]})
    ]
    layout = go.Layout(title='Number of product categories that companies are active in',
                       xaxis={'title': 'Number of product categories'},
                       yaxis={'title': 'Percentage of companies'},
                       font={'family': 'HelveticaNeue'})
    return go.Figure(data=data, layout=layout)


def plot_complimentarity(df1, df2):
    """
    returns a plot of the distribution of the number of different companies
    used by consumers in the last 12 ticks
    """
    data = [
        go.Bar(x=df1.bins, y=df1.perc, hoverinfo='text',
               hovertext=['{}%'.format(x) for x in df1.perc],
               name='Scenario 1', marker={'color': scen_colours[0]}),
        go.Bar(x=df2.bins, y=df2.perc, hoverinfo='text',
               hovertext=['{}%'.format(x) for x in df2.perc],
               name='Scenario 2', marker={'color': scen_colours[1]})
    ]
    layout = go.Layout(title='Number of companies used by consumers in the last year of the tick cycle',
                       xaxis={'title': 'Number of companies'},
                       yaxis={'title': 'Percentage of users'},
                       font={'family': 'HelveticaNeue'})
    return go.Figure(data=data, layout=layout)


def plot_quality_difference(df1, df2):
    """
    returns a plot with the linked final qualities in each category
    """
    df = pd.merge(df1, df2, on='category', how='outer')
    data = []
    for i in range(df.shape[0]):
        if df.quality_x[i] and df.quality_y[i]:
            df_ = pd.DataFrame({
                'scen': ['Scenario 1', 'Scenario 2'],
                'qual': [df.quality_x[i], df.quality_y[i]]
            })
            data += [
                go.Scatter(
                    x=df_.scen, y=df_.qual, mode='lines', name=None, showlegend=False,
                    line={'color': GREY}, hoverinfo='skip'
                )
            ]
    data += [
        go.Scatter(
            x=['Scenario 1'] * df.loc[df.quality_x > 0].shape[0],
            y=df.loc[df.quality_x > 0].quality_x, name='Scenario 1', showlegend=False,
            hoverinfo='text',
            hovertext=['category {}, offered by {} companies'.format(x, y)
                       for x, y in zip(df.loc[df.quality_x > 0].category.values,
                                       df.loc[df.quality_x > 0].num_firms_x.values)],
            mode='markers', marker={'color': scen_colours[0]}
        ),
        go.Scatter(
            x=['Scenario 2'] * df.loc[df.quality_y > 0].shape[0],
            y=df.loc[df.quality_y > 0].quality_y, name='Scenario 2', showlegend=False,
            hoverinfo='text',
            hovertext=['category {}, offered by {} companies'.format(x, y)
                       for x, y in zip(df.loc[df.quality_y > 0].category.values,
                                       df.loc[df.quality_y > 0].num_firms_y.values)],
            mode='markers', marker={'color': scen_colours[1]}
        )
    ]
    layout = go.Layout(
        title="Highest quality per product category",
        xaxis={'showgrid': False},
        yaxis={'title': 'Quality', 'showgrid': False},
        font={'family': 'HelveticaNeue'},
        hovermode='closest'
    )
    return go.Figure(data=data, layout=layout)


def quality_distribution(df1, df2):
    """
    returns a plot of the distribution of quality at the end of the run_simulation
    only the highest quality is recording
    """
    data = [
        go.Histogram(
            x=df1.quality,
            name='Scenario 1', marker={'color': scen_colours[0]},
            histnorm='probability'
        ),
        go.Histogram(
            x=df2.quality,
            name='Scenario 2', marker={'color': scen_colours[1]},
            histnorm='probability'
        )
    ]
    layout = go.Layout(title='Distribution of maximal quality',
                       xaxis={'title': 'Maximal quality (per category)'},
                       yaxis={'title': 'Frequency'},
                       font={'family': 'HelveticaNeue'})
    return go.Figure(data=data, layout=layout)


def plot_market_entry(cat_entry_and_exit_df, cat_entry_and_exit_df_2):
    """
    returns a plot with the entry and exit of firms per category
    """
    # get the limits so everything is on the same scale
    df = pd.concat([cat_entry_and_exit_df, cat_entry_and_exit_df_2])
    limits = [-df.exit.max() - 0.3, df.entry.max() + 0.3]

    fig = tools.make_subplots(rows=1, cols=2)

    xs = cat_entry_and_exit_df.index
    new_per_cat = cat_entry_and_exit_df.entry.astype(int)
    dead_per_cat = cat_entry_and_exit_df.exit.astype(int)
    fig.append_trace(
        go.Bar(y=xs, x=new_per_cat, orientation='h', showlegend=False, hoverinfo='text',
               hovertext=['{} entries in category {}'.format(x, y)
                          for x, y in zip(new_per_cat, np.arange(len(new_per_cat)))],
               marker={'color': scen_colours[0]}), 1, 1)
    fig.append_trace(
        go.Bar(y=xs, x=-dead_per_cat, orientation='h', showlegend=False, hoverinfo='text',
               hovertext=['{} exits in category {}'.format(x, y)
                          for x, y in zip(dead_per_cat, np.arange(len(new_per_cat)))],
               marker={'color': scen_colours[0]}), 1, 1)
    fig.append_trace(
        go.Bar(y=xs, x=new_per_cat - dead_per_cat, orientation='h', showlegend=False, hoverinfo='text',
               hovertext=['{} net entries in category {}'.format(x, y)
                          for x, y in zip(new_per_cat - dead_per_cat, np.arange(len(new_per_cat)))],
               marker={'color': dark_scen_colours[0]}), 1, 1)

    xs = cat_entry_and_exit_df_2.index
    new_per_cat = cat_entry_and_exit_df_2.entry.astype(int)
    dead_per_cat = cat_entry_and_exit_df_2.exit.astype(int)
    fig.append_trace(
        go.Bar(y=xs, x=new_per_cat, orientation='h', showlegend=False, hoverinfo='text',
               hovertext=['{} entries in category {}'.format(x, y)
                          for x, y in zip(new_per_cat, np.arange(len(new_per_cat)))],
               marker={'color': scen_colours[1]}), 1, 2)
    fig.append_trace(
        go.Bar(y=xs, x=-dead_per_cat, orientation='h', showlegend=False, hoverinfo='text',
               hovertext=['{} exits in category {}'.format(x, y)
                          for x, y in zip(dead_per_cat, np.arange(len(new_per_cat)))],
               marker={'color': scen_colours[1]}), 1, 2)
    fig.append_trace(
        go.Bar(y=xs, x=new_per_cat - dead_per_cat, orientation='h', showlegend=False, hoverinfo='text',
               hovertext=['{} net entries in category {}'.format(x, y)
                          for x, y in zip(new_per_cat - dead_per_cat, np.arange(len(new_per_cat)))],
               marker={'color': dark_scen_colours[1]}), 1, 2)
    fig['layout']['xaxis2'].update(title="Number of companies", range=limits)
    fig['layout']['xaxis1'].update(title="Number of companies", range=limits)
    fig['layout']['yaxis1'].update(title="Product category")
    fig['layout'].update(title='Market entry and exit per product category')
    fig['layout']['font'].update(family='HelveticaNeue')
    fig['layout'].update(barmode='overlay')

    return fig


def plot_new_products(counter1, counter2):
    """
    returns a line plot of the cumulative number of new products that have been
    released during the simulation; split by new and existing categories
    """
    ticks = np.arange(len(counter1)) + 1

    fig = tools.make_subplots(
        rows=2, cols=1,
        subplot_titles=[
            'Cumulative number of products being released in new categories',
            'Cumulative number of products being released in existing categories'
        ]
    )

    fig.append_trace(
        go.Scatter(x=ticks, y=np.cumsum(counter1.new), name='Scenario 1',
                   marker={'color': scen_colours[0]}, legendgroup='Scenario 1',), 1, 1
    )
    fig.append_trace(
        go.Scatter(x=ticks, y=np.cumsum(counter2.new), name='Scenario 2',
                   marker={'color': scen_colours[1]}, legendgroup='Scenario 2',), 1, 1
    )
    fig.append_trace(
        go.Scatter(x=ticks, y=np.cumsum(counter1.existing), legendgroup='Scenario 1',
                   marker={'color': scen_colours[0]}, showlegend=False), 2, 1
    )
    fig.append_trace(
        go.Scatter(x=ticks, y=np.cumsum(counter2.existing), legendgroup='Scenario 2',
                   marker={'color': scen_colours[1]}, showlegend=False), 2, 1
    )
    fig['layout']['xaxis2'].update(title='Months (ticks)')
    fig['layout']['yaxis1'].update(title='Number of products')
    fig['layout']['yaxis2'].update(title='Number of products')
    fig['layout']['font'].update(family='HelveticaNeue')
    return fig


def plot_request_distribution(df1, df2):
    """
    returns a bar plot with a histogram of the number of data requests
    that were granted, per company, in their first year
    """
    a1 = np.bincount(df1.requests.values.astype(int))
    a2 = np.bincount(df2.requests.values.astype(int))
    data = [
        go.Bar(x=np.arange(len(a1)), y=a1,
               name='Scenario 1', marker={'color': scen_colours[0]}),
        go.Bar(x=np.arange(len(a2)), y=a2,
               name='Scenario 2', marker={'color': scen_colours[1]})
    ]
    layout = go.Layout(title='Number of data requests granted to young companies in their first year',
                       xaxis={'title': 'Number of granted data requests'},
                       yaxis={'title': 'Number of companies'},
                       font={'family': 'HelveticaNeue'})
    return go.Figure(data=data, layout=layout)
