"""TCP server that lets a UR robot read/write a CSV file over a socket.

Protocol (one request line in, one response line out, newline-terminated):
    ROWS                      -> <int>            number of data rows (header excluded)
    COLS                      -> <int>            number of columns
    GET,<row>,<col>           -> <value>          cell value (0-based row/col)
    SET,<row>,<col>,<value>   -> OK               set cell value, then save to disk
    APPEND,<val1>,<val2>,...  -> OK               append new row with comma-separated values
    PING                      -> PONG             heartbeat / watchdog keep-alive
Errors are returned as: ERR,<message>

Notes:
  * Row 0 is the first DATA row; the header row is excluded from ROWS and from GET/SET row indexing.
  * Cell values are strings. Commas inside a value are preserved because <value> is the
    final token of a SET command, and the csv module quotes it correctly on disk.
  * Values must not contain newline characters (the protocol is line-based).
"""

import csv
import os
import socket
import socketserver
import threading

# --- Configuration (placeholder; update for your network) --------------------
HOST = "192.168.0.123"
PORT = 30000
CSV_PATH = "data.csv"

# Watchdog: max seconds a connection may stay silent before it is considered
# dead and closed. The robot's heartbeat (PING) must arrive more often than this.
CLIENT_TIMEOUT = 5.0

# Serialize all CSV access so concurrent clients can't corrupt the file.
_csv_lock = threading.Lock()


def _read_csv():
    """Return (header, rows) where rows is a list of data rows (header excluded)."""
    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
        all_rows = list(csv.reader(f))
    if not all_rows:
        return [], []
    return all_rows[0], all_rows[1:]


def _write_csv(header, rows):
    """Write header + data rows back to disk immediately."""
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def get_rows():
    """Number of data rows (header excluded)."""
    _header, rows = _read_csv()
    return len(rows)


def get_cols():
    """Number of columns (length of the header row)."""
    header, _rows = _read_csv()
    return len(header)


def get_cell(row, col):
    """Value at data row `row`, column `col` (both 0-based)."""
    _header, rows = _read_csv()
    if row < 0 or row >= len(rows):
        raise IndexError("row out of range")
    data_row = rows[row]
    if col < 0 or col >= len(data_row):
        raise IndexError("col out of range")
    return data_row[col]


def set_cell(row, col, value):
    """Set the cell at data row `row`, column `col` to `value`, then save."""
    header, rows = _read_csv()
    if row < 0 or row >= len(rows):
        raise IndexError("row out of range")
    if col < 0 or col >= len(header):
        raise IndexError("col out of range")
    # Pad short rows so the target column exists.
    data_row = rows[row]
    if len(data_row) < len(header):
        data_row.extend([""] * (len(header) - len(data_row)))
    data_row[col] = value
    rows[row] = data_row
    _write_csv(header, rows)


def append_row(values):
    """Append a new row with the given values, then save."""
    header, rows = _read_csv()
    rows.append(values)
    _write_csv(header, rows)


def handle_command(line):
    """Parse one request line and return the response line (without trailing newline)."""
    line = line.strip()
    if not line:
        return "ERR,empty command"

    parts = line.split(",")
    command = parts[0].upper()

    try:
        if command == "PING":
            return "PONG"

        if command == "ROWS":
            return str(get_rows())

        if command == "COLS":
            return str(get_cols())

        if command == "GET":
            if len(parts) != 3:
                return "ERR,GET expects GET,<row>,<col>"
            row = int(parts[1])
            col = int(parts[2])
            return get_cell(row, col)

        if command == "SET":
            # SET,<row>,<col>,<value> -- value is everything after the 3rd comma,
            # so commas inside the value are preserved.
            if len(parts) < 4:
                return "ERR,SET expects SET,<row>,<col>,<value>"
            row = int(parts[1])
            col = int(parts[2])
            value = ",".join(parts[3:])
            set_cell(row, col, value)
            return "OK"

        if command == "APPEND":
            # APPEND,<value1>,<value2>,... -- append a new row with comma-separated values.
            if len(parts) < 2:
                return "ERR,APPEND expects APPEND,<value1>,<value2>,..."
            values = parts[1:]  # All parts after "APPEND" are the cell values
            append_row(values)
            return "OK"

        return "ERR,unknown command"

    except ValueError:
        return "ERR,row/col must be integers"
    except IndexError as exc:
        return "ERR," + str(exc)
    except OSError as exc:
        return "ERR,file error: " + str(exc)


class CSVRequestHandler(socketserver.StreamRequestHandler):
    """Handles one client connection; serves multiple newline-terminated commands.

    Watchdog: the connection is given an idle timeout (CLIENT_TIMEOUT). If the
    client stops sending (e.g. its heartbeat PINGs stop), the read times out and
    the connection is reported lost and closed. TCP keep-alive is also enabled so
    abrupt network drops are detected by the OS.
    """

    def setup(self):
        super().setup()
        # Watchdog timeout: recv() raises socket.timeout after CLIENT_TIMEOUT s of silence.
        self.connection.settimeout(CLIENT_TIMEOUT)
        try:
            self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        except OSError:
            pass

    def handle(self):
        peer = self.client_address
        print("Client connected: {}".format(peer))
        try:
            for raw in self.rfile:
                line = raw.decode("utf-8", errors="replace")
                with _csv_lock:
                    response = handle_command(line)
                if line.strip().upper() != "PING":
                    print("Received command: {}".format(line.strip()))
                    print("Sending response: {}".format(response))
                self.wfile.write((response + "\n").encode("utf-8"))
                self.wfile.flush()
        except socket.timeout:
            print("Watchdog: client {} silent > {}s, closing connection".format(peer, CLIENT_TIMEOUT))
        except (ConnectionResetError, BrokenPipeError, OSError) as exc:
            print("Client {} connection error: {}".format(peer, exc))
        finally:
            print("Client disconnected: {}".format(peer))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    with ThreadedTCPServer((HOST, PORT), CSVRequestHandler) as server:
        print("CSV server listening on {}:{} (file: {})".format(HOST, PORT, CSV_PATH))
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down.")


if __name__ == "__main__":
    main()
