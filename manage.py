from flask_script import Manager,Server

import main


app=main.app

# Init manager object via app object
manager=Manager(main.app)

manager.add_command("server",Server(host='0.0.0.0'))


@manager.shell
def make_shell_context():
    """
    Create a python CLI
    return:Default import object
    type:Dict
    """
    return dict(app=main.app)


if __name__=="__main__":
    manager.run()