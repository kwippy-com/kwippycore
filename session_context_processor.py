def flash(request):
    # Add the flash message from the session and clear it
    flash = ""
    if 'flash' in request.session:
        flash = request.session['flash']
        del request.session['flash']
    return {'flash': flash} 
