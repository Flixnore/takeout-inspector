"""takeout_inspector/utils.py

Utility helper functions.

Copyright (c) 2016 Christopher Charbonneau Wells

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import ConfigParser
import plotly.offline as py

__all__ = ['plotly_default_layout_options', 'plotly_output']

config = ConfigParser.ConfigParser()
config.readfp(open('settings.defaults.cfg'))
config.read(['settings.cfg'])


def plotly_default_layout_options():
    """Prepares default layout options for all graphs.
    """
    return dict(
        font=dict(
            color=config.get('color', 'text'),
            family=config.get('font', 'family'),
            size=config.get('font', 'size'),
        ),
        margin=dict(
            b=50,
            t=50,
        ),
        xaxis=dict(
            titlefont=dict(
                color=config.get('color', 'text_lighter'),
            )
        ),
        yaxis=dict(
            titlefont=dict(
                color=config.get('color', 'text_lighter'),
            ),
        ),
    )


def plotly_output(figure):
    """Plots a Plotly figure and returns a dict with html and javascript for the report.
    """
    output = py.plot(figure, output_type='div', include_plotlyjs=False,)
    div, plotly_js = output.split('<script type="text/javascript">')

    waypoints_js = '''
    new Waypoint({{
        element: document.getElementById('{div_id}'),
        handler: function() {{
            {javascript}
            this.destroy();
        }},
        offset: '100%'
    }});
    '''.format(
        div_id=div[9:45],  # String location of div ID.
        javascript=plotly_js[:-9]  # Removes </script> from the end of the string
    )

    return {'html': div, 'js': waypoints_js}
