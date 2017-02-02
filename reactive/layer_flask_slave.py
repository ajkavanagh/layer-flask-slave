from charms.reactive import when, when_not, when_file_changed, set_state
import charmhelpers.fetch as fetch
import charmhelpers.core.host as host
import charm.flask_utils as flask_utils


@when_not('layer-flask-slave.installed')
def install_flask_slave():
    fetch.apt_install(['python3-flask'])
    set_state('layer-flask-slave.installed')


@when('layer-flask-slave.installed')
@when_not('layer-flask-slave.initial_setup')
def flask_setup():
    flask_utils.setup_dirs()
    set_state('layer-flask-slave.initial_setup')


@when('layer-flask-slave.initial_setup')
def flask_complete_setup():
    flask_utils.copy_static_files()
    flask_utils.render_files()
    host.service_start(flask_utils.FLASK_SERVICE)
    set_state('layer-flask-slave.setup')


@when('layer-flask-slave.setup')
@when_file_changed([flask_utils.FLASK_SERVER,
                    flask_utils.FLASK_SERVER_CONFIG])
def restart_service():
    host.service_restart(flask_utils.FLASK_SERVICE)


@when_file_changed(flask_utils.FLASK_SYSTEMD_FILE)
def reload_systemd():
    flask_utils.reload_systemd()
