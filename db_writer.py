import zmq
import hydra
import logging
import jsonpickle
from omegaconf import DictConfig
from ORM import ORM_submission, ORM_comment, ORM_subreddit, ORM_subreddit_active_users

logging.basicConfig(filename = 'logs/db_writer.log',
                    filemode='a',
                    format='%(asctime)s:%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)

@hydra.main(version_base = None, config_path = "conf", config_name = "db_writer_conf.yaml")
def main(cfg : DictConfig) -> None:
    """Keys accessed:
    db_config.user - database user with dml privileges to provided database;\n
    db_config.password - password for provided user;\n
    db_config.database - database with necessary tables;\n
    db_config.host - address for database connection;\n
    db_config.port - port for database connection;\n
    db_config.use_pure - boolean to use pure python connection instead of c implementation. True value recommended;\n"""

    backend_socket_adress = "tcp://{host}:{port}".format(host = cfg.backend_socket.host, port = cfg.backend_socket.port)

    try:
        context = zmq.Context(1)

        backend = context.socket(zmq.PULL)
        backend.connect(backend_socket_adress)
        
        poller = zmq.Poller()
        poller.register(backend, zmq.POLLIN)

        while True:
            socks = dict(poller.poll())

            if backend in socks and socks[backend] == zmq.POLLIN:
                message = backend.recv_string()

                message = jsonpickle.decode(message)

                print("Writing " + type(message))
                message.write_to_MySQL(cfg.db)
    
    except Exception as e:
        logging.critical(e, exc_info=True)

    finally:
        backend.close()
        context.term()

if __name__ == "__main__":
    main()