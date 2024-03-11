from . import app  # Utilisez l'importation relative

@app.route('/about')
def about():
    return 'La page À propos'

