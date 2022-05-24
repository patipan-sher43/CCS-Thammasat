#!/usr/bin/python
# -*- coding: utf-8 -*-

from website import create_app

app, mysql = create_app()

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)