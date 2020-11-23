import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/contributions'),
        ('get_html', '/contributions/500'),
        ('get_html', '/contributions.geojson'),
        ('get_dt', '/contributions'),
        ('get_dt', '/languages'),
        ('get_html', '/contributions/215'),
        ('get_dt', '/values?iSortCol_0=5&sSortDir_0=asc&iSortingCols=1'),
        ('get_dt', '/values?contribution=220&iSortingCols=1&iSortCol_0=0'),
        ('get_dt', '/values?contribution=220&iSortingCols=1&iSortCol_0=2'),
        ('get_dt', '/values?contribution=220&sSearch_0=1&sSearch_2=4'),
        ('get_dt', '/values?sSearch_3=mal'),
        ('get_html', '/contributors'),
        ('get_dt', '/contributors'),
        ('get_html', '/parameters'),
        ('get_dt', '/parameters'),
        ('get_dt', '/parameters?chapter=1'),
        ('get_html', '/parameters/1-222'),
        ('get_json', '/parameters/1-222.geojson'),
        ('get_dt', '/values?parameter=1-222'),
        ('get_html', '/languages/182.snippet.html'),
        ('get_html', '/languages/128.snippet.html?parameter=962'),
        ('get_html', '/sources'),
        ('get_dt', '/sources'),
        ('get_html', '/sources/ainsworth1923'),
        ('get_html', '/sources/ainsworth1923.snippet.html'),
        ('get_html', '/valuesets/1-210-234'),
        ('get_html', '/valuesets/4-732-208'),
        ('get_html', '/values'),
        ('get_dt', '/contributions?sSearch_2=a&sSearch_3=aq'),
        ('get_dt', '/contributors?sSearch_1=Consultant'),
        ('get_html', '/chapters'),
        ('get_html', '/providers'),
        ('get_html', '/providers/ids'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
