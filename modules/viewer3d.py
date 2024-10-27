# Importing modules...
import numpy as np
import plotly.graph_objects as go

class Viewer3D: 
    def __init__(self, title='', size=5, graphical=False):
        self.title = title
        self.size = size # Change graph dimensions 
        self.graphical = graphical # Toggle to activate graphical mode

        # Create Figure 
        self.figure = go.Figure(
            layout=go.Layout(
                height=700, 
                width=700,
                title=go.layout.Title(text=self.title)
            )
        )

        # Set up layout enviroment
        self.figure.update_layout(
            scene_aspectmode='cube',
            font=dict(
                family='Arial',
                size=15,
                color='black'
            ),
            scene = dict(
                xaxis_title='x'*self.graphical,
                yaxis_title='y'*self.graphical, 
                zaxis_title='z'*self.graphical, 
                xaxis=dict(
                    range=[-self.size,self.size],
                    showbackground=self.graphical,
                    showticklabels=self.graphical,
                    showaxeslabels=self.graphical,
                    showgrid=self.graphical,
                    showspikes=self.graphical
                    ),
                yaxis=dict(
                    range=[-self.size,self.size],
                    showbackground=self.graphical,
                    showticklabels=self.graphical,
                    showaxeslabels=self.graphical,
                    showgrid=self.graphical,
                    showspikes=self.graphical
                    ), 
                zaxis=dict(
                    range=[-self.size,self.size],
                    showbackground=self.graphical,
                    showticklabels=self.graphical,
                    showaxeslabels=self.graphical,
                    showgrid=self.graphical,
                    showspikes=self.graphical
                    )
            )
        )

        # Change default camera settings
        self.figure.update_layout(
            scene=dict(
                camera=dict(
                    projection=dict(
                        type='orthographic'
                    )
                )
            )
        )

    def add_frame(self, transformation, name="", axis_size=1, color=None):

        R, t = transformation[0:3, 0:3], transformation[0:3 , [-1]] 

        # Set default colors
        axis_name_list = ['x', 'y', 'z']
        axis_color_list = ['red', 'green', 'blue']

        self.figure.add_trace(
            go.Scatter3d(
                x=t[0],
                y=t[1],
                z=t[2],
                mode='markers',
                marker=dict(
                    size=4,
                    opacity=0.80,
                    color=color
                ),
                name=name,
                legendgroup='Frames',
                legendgrouptitle_text='Frames',
                showlegend=True if name else False 
            )
        )

        for axis, axis_color in enumerate(axis_color_list):

            arrow = np.hstack((t, t + R[:,axis].reshape(-1,1) * axis_size)) # Arrow of an axis

            self.figure.add_trace(
                go.Scatter3d(
                    x=arrow[0], 
                    y=arrow[1],
                    z=arrow[2], 
                    mode='lines',
                    line=dict(
                        width=2,
                        color=axis_color
                        ),
                    showlegend=False,
                    name=axis_name_list[axis]+name,
                    hoverinfo = None if self.graphical else 'skip'
                )
            )

    def add_points(self, points, name, color=None, colorscale=None, range=None, colorbar=None):
        self.figure.add_trace(
            go.Scatter3d(
                x=points[0],
                y=points[1],
                z=points[2],
                mode='markers',
                marker=dict(
                    size=3,
                    opacity=0.80,
                    color=color,
                    cmin= range[0] if colorbar is not None else None,
                    cmax= range[1] if colorbar is not None else None,
                    colorbar= dict(title=colorbar,lenmode='fraction', len=0.5) if colorbar is not None else colorbar,
                    colorscale=colorscale
                ),
                name=name,
                legendgroup='Points',
                legendgrouptitle_text='Points',
                showlegend=True
            )
        )

    def add_trace(self, points, name, color=None, colorscale=None, range=None, colorbar=None):
        self.figure.add_trace(
            go.Scatter3d(
                x=points[0],
                y=points[1],
                z=points[2],
                mode='lines',
                marker=dict(
                    size=3,
                    opacity=0.80,
                    color=color,
                    cmin= range[0] if colorbar is not None else None,
                    cmax= range[1] if colorbar is not None else None,
                    colorbar= dict(title=colorbar,lenmode='fraction', len=0.5) if colorbar is not None else colorbar,
                    colorscale=colorscale
                ),
                name=name,
                legendgroup='Traces',
                legendgrouptitle_text='Traces',
                showlegend=True
            )
        )


    def add_solid(self, vertices, name, color=None):
        self.figure.add_trace(
            go.Mesh3d(
                x=vertices[0],
                y=vertices[1],
                z=vertices[2],
                alphahull=0,
                color=color,
                flatshading=True,
                name=name,
                legendgroup='Objects',
                legendgrouptitle_text='Objects',
                showlegend=self.graphical
            )
        )

    def add_plane(self, vertices, name, color=None):
        self.figure.add_trace(
            go.Mesh3d(
                x=vertices[0],
                y=vertices[1],
                z=vertices[2],
                opacity=0.5,
                color=color,
                flatshading=True,
                name=name,
                legendgroup='References',
                legendgrouptitle_text='References',
                hoverinfo='skip',
                showlegend=True
            )
        )
    

