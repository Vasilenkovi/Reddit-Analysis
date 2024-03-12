import zmq
import hydra
import logging
from omegaconf import DictConfig

logging.basicConfig(filename = 'logs/db_streamer.log',
                    filemode='a',
                    format='%(asctime)s:%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)

@hydra.main(version_base = None, config_path = "conf", config_name = "db_streamer_conf.yaml")
def main(cfg : DictConfig) -> None:

    frontend_socket_adress = "tcp://{host}:{port}".format(host = cfg.frontend_socket.host, port = cfg.frontend_socket.port)
    backend_socket_adress = "tcp://{host}:{port}".format(host = cfg.backend_socket.host, port = cfg.backend_socket.port)

    try:
        context = zmq.Context(2)

        # Socket facing clients
        frontend = context.socket(zmq.PULL)
        frontend.bind(frontend_socket_adress)
        
        # Socket facing services
        backend = context.socket(zmq.PUSH)
        backend.bind(backend_socket_adress)

        zmq.device(zmq.STREAMER, frontend, backend)
    
    except Exception as e:
        logging.critical(e, exc_info=True)

    finally:
        frontend.close()
        backend.close()
        context.term()

if __name__ == "__main__":
    main()