# Importing modules...
import plotly.graph_objects as go

class Graph: 
    def __init__(self, title='', axis_title=('x', 'y')):
        self.title = title

        # Create Figure 
        self.figure = go.Figure( 
            layout=go.Layout(
                height=700, 
                width=700, 
                title=go.layout.Title(text=self.title)
            )
        )
        
        self.figure.update_layout(
            xaxis_title=axis_title[0],
            yaxis_title=axis_title[1],
            plot_bgcolor='white',
            font=dict(
                family='Arial',
                size=15,
                color='black'
            ),
            xaxis=dict(
                gridcolor='lightgray'
            ),
            yaxis=dict(
                gridcolor='lightgray'
            )
        )

    def add_points(self, points, name, color=None, colorscale=None, range=None, colorbar=None):
        self.figure.add_trace(
            go.Scatter(
                x=points[0],
                y=points[1],
                mode='markers',
                marker=dict(
                    size=5,
                    opacity=0.80,
                    color=color,
                    cmin=range[0] if colorbar is not None else None,
                    cmax=range[1] if colorbar is not None else None,
                    colorbar=dict(title=colorbar,lenmode='fraction', len=0.5) if colorbar is not None else colorbar,
                    colorscale=colorscale
                ),
                name=name,
                legendgroup='Points',
                legendgrouptitle_text='Points'
            )
        )