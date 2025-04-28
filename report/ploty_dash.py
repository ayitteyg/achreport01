import plotly.express as px

def create_bar_chart(data, x_data, y_data, x_title, y_title, title):
    """
    Create a bar chart using Plotly for any given dataset.
    
    :param data: Data for the chart
    :param x_data: Column for x-axis
    :param y_data: Column for y-axis
    :param x_title: Title of x-axis
    :param y_title: Title of y-axis
    :param title: Title of the chart
    :return: Plotly Figure
    """
    fig = px.bar(data, x=x_data, y=y_data, title=title)
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        template="plotly_dark"
    )
    return fig




def get_bar_data(x_field, y_field, data, x_title, y_title):
    d = {
            "data": [
                {
                    "x": [item[x_field] for item in data],
                    "y": [item[y_field] for item in data],
                    "type": "bar",
                }
            ],
            "layout": {
                "xaxis": {"title": f"{x_title}"},
                "yaxis": {"title": f"{y_title}"},
            },
        }
    return d