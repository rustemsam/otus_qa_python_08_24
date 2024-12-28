import datetime
import logging
import socket
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
BUFFER_SIZE = 1024
END_OF_STREAM = '\r\n\r\n'


def setup_logger():
    """Set up a logger for the server."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger("EchoServer")


logger = setup_logger()


def build_http_response(status_code, client_headers, method, client_address) -> str:
    """
    Build an HTTP response based on the request details.

    Args:
        status_code (int): HTTP status code for the response.
        client_headers (list): Headers from the client's request.
        method (str): HTTP method used in the request.
        client_address (tuple): Client's address (IP and port).

    Returns:
        str: The complete HTTP response string.
    """
    reason_phrase = HTTPStatus(status_code).phrase

    response_headers = (
        f"HTTP/1.0 {status_code} {reason_phrase}\r\n"
        f"Content-Type: text/plain; charset=UTF-8\r\n"
        f"Server: SimplePythonServer\r\n"
        f"Date: {datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        f"\r\n"
    )

    formatted_headers = "\n".join(f"{line}" for line in client_headers if line)
    response_body = (
        f"Request Method: {method}\r\n"
        f"Request Source: {client_address}\r\n"
        f"Response Status: {status_code} {reason_phrase}\r\n"
        f"Headers:\n{formatted_headers}\r\n"
    )

    return response_headers + response_body


def parse_request(client_data) -> ():
    """
    Parse the HTTP request from the client.

    Args:
        client_data (str): Raw data received from the client.

    Returns:
        tuple: (method, path, client_headers) extracted from the request.
    """
    request_line, *header_lines = client_data.split("\r\n")
    method, path, _ = request_line.split(" ")
    client_headers = [line for line in header_lines if line]
    return method, path, client_headers


def handle_client(connection, client_address):
    """
    Handle communication with a single client.

    Args:
        connection (socket.socket): The client's connection socket.
        client_address (tuple): The client's address (IP and port).
    """
    try:
        client_data = ''
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data:
                break

            client_data += data.decode()
            if END_OF_STREAM in client_data:
                break

        method, path, client_headers = parse_request(client_data)

        parsed_url = urlparse(path)
        query_params = parse_qs(parsed_url.query)

        status_code = 200
        if 'status' in query_params:
            try:
                status_code = int(query_params['status'][0])
            except ValueError:
                logger.warning(f"Invalid status code in query: {query_params['status'][0]}")

        http_response = build_http_response(status_code, client_headers, method, client_address)
        connection.send(http_response.encode())
        logger.info(f"Processed request from {client_address} with status {status_code}")

    except Exception as e:
        logger.error(f"Error handling client {client_address}: {e}")
    finally:
        connection.close()


def start_server():
    """
    Start the HTTP server to listen for client connections.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen()
        logger.info(f"Server started at http://{SERVER_HOST}:{SERVER_PORT}")

        try:
            while True:
                client_connection, client_address = server_socket.accept()
                handle_client(client_connection, client_address)
        except KeyboardInterrupt:
            logger.info("Server is shutting down")
        except Exception as e:
            logger.error(f"Server error: {e}")


if __name__ == "__main__":
    start_server()
