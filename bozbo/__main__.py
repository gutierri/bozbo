from . import app

def main():
    app_main = app()
    app_main.run(host='localhost', port=8080, reloader=True)

if __name__ == '__main__':
    main()
