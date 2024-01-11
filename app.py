from cmd.server.create import create_server

app = create_server()

if __name__ == '__main__':
    app.run(debug=True)
