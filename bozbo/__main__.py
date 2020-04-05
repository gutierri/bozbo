from . import app

def main():
    app_main = app()
    app_main.run(host='0.0.0.0', port=8080, reloader=True, debug=True)

if __name__ == '__main__':
    main()
