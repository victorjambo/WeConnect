from versions import app
from flask import render_template, jsonify

@app.route('/')
def version2():
    """route for API documentation"""
    return render_template('version2.html')

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'warning': '404, Endpoint not found'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'warning': '500, Internal Server Error'}), 500
